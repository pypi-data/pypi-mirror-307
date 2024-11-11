from __future__ import annotations

import asyncio
from asyncio.exceptions import CancelledError
from dataclasses import dataclass, field
import json
import signal
from typing import TYPE_CHECKING

from aiohttp import ClientSession
import aiomqtt
from video_clip_describer import VisionAgent

from frigate_event_handler.api import FrigateApiClient
from frigate_event_handler.const import LOGGER as _LOGGER
from frigate_event_handler.models import EventMessage

if TYPE_CHECKING:
    from frigate_event_handler.config import Config, FrigateConfig, MQTTConfig, VisionAgentConfig


@dataclass
class Daemon:
    mqtt_config: MQTTConfig | None = None
    frigate_config: FrigateConfig | None = None
    vision_config: VisionAgentConfig | None = None

    api: FrigateApiClient | None = field(init=False)
    vision_agent: VisionAgent | None = field(init=False)

    _running = False
    _session: ClientSession | None = None
    _task: asyncio.Task | None = None

    @classmethod
    def from_config(cls, config: Config) -> Daemon:
        _LOGGER.info(f"Constructing daemon with config: {config.to_dict()}")
        return cls(
            mqtt_config=config.mqtt,
            frigate_config=config.frigate,
            vision_config=config.vision_agent,
        )

    def __post_init__(self):
        self._running = True
        self._session = ClientSession()
        self.api = FrigateApiClient(
            base_url=self.frigate_config.base_url,
            api_key=self.frigate_config.api_key,
            session=self._session,
        )
        self.vision_agent = VisionAgent(
            **self._vision_agent_params(),
        )

    def _mqtt_connect_params(self):
        return {
            "hostname": self.mqtt_config.host,
            "port": self.mqtt_config.port,
            # "identifier": self.mqtt_client_id,
            "username": self.mqtt_config.username,
            "password": self.mqtt_config.password,
        }

    def _vision_agent_params(self):
        params = {
            "api_base_url": self.vision_config.api_base_url,
            "api_key": self.vision_config.api_key,
            "vision_model": self.vision_config.vision_model,
            "refine_model": self.vision_config.refine_model,
            "vision_prompt": self.vision_config.vision_prompt,
            "refine_prompt": self.vision_config.refine_prompt,
            "prompt_context": self.vision_config.prompt_context,
            "resize_video": self.vision_config.resize_video,
            "stack_grid": self.vision_config.stack_grid,
            "stack_grid_size": self.vision_config.stack_grid_size,
            "remove_similar_frames": self.vision_config.remove_similar_frames,
            "hashing_max_frames": self.vision_config.hashing_max_frames,
            "hash_size": self.vision_config.hash_size,
        }
        return {k: v for k, v in params.items() if v is not None}

    async def process_message(self, message):
        """Process the received MQTT message."""
        try:
            payload = message.payload.decode()
            try:
                data = EventMessage.from_json(payload)
                await self.handle_event(data)
            except json.JSONDecodeError:
                _LOGGER.warning(f"Received message is not valid JSON: {payload}")

        except Exception as e:  # noqa: BLE001
            _LOGGER.error(f"Error processing message: {e!s}")

    async def handle_event(self, data: EventMessage):
        """Handle the event data."""
        _LOGGER.info(f"Processing {data.type} message")

        if data.type == "end":
            event = data.after
            camera = event.camera
            event_id = event.id
            if event.has_clip:
                clip = await self.api.event_clip(event.id)
                _LOGGER.info(f"Saving clip for event {event_id} from camera {camera}")
                description = await self.generate_clip_description(clip)

                _LOGGER.debug("Updating event description")
                await self.api.set_event_description(event_id, description)

    async def generate_clip_description(self, clip: bytes):
        """Generate clip description."""
        _LOGGER.debug(f"Generating clip description for {len(clip)} bytes of video")
        description = await self.vision_agent.run(
            video_data=clip,
        )
        _LOGGER.info(f"Generated description: {description}")
        return description

    async def mqtt_listener(self):
        """MQTT listener loop."""

        while self._running:
            try:
                async with aiomqtt.Client(**self._mqtt_connect_params()) as client:
                    _LOGGER.info(f"Connected to MQTT broker at {self.mqtt_config.host}")

                    await client.subscribe(self.mqtt_config.topic)
                    _LOGGER.info(f"Subscribed to topic: {self.mqtt_config.topic}")

                    async for message in client.messages:
                        await self.process_message(message)
            except aiomqtt.MqttError as err:
                _LOGGER.error(f"MQTT connection error: {err!s}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except CancelledError:
                pass

    async def handle_shutdown(self):
        """Handle shutdown signals."""
        _LOGGER.info("Received shutdown signal")
        self._running = False
        await self._session.close()
        self._task.cancel()

    async def run(self):
        """Run the daemon."""
        loop = asyncio.get_event_loop()
        for sig_name in ("SIGINT", "SIGTERM"):
            # noinspection PyTypeChecker
            loop.add_signal_handler(
                getattr(signal, sig_name),
                lambda: asyncio.create_task(self.handle_shutdown()),
            )

        self._task = loop.create_task(self.mqtt_listener())
        try:
            await self._task
        except Exception as e:  # noqa: BLE001
            _LOGGER.error(f"Error in main loop: {e!s}")
        finally:
            _LOGGER.info("Daemon shutting down")
