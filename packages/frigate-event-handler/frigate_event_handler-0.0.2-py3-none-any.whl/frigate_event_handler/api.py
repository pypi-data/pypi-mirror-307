from __future__ import annotations

import asyncio
from dataclasses import dataclass
from http import HTTPStatus

from aiohttp.client import ClientError, ClientResponse, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET, METH_POST
import async_timeout
import orjson
from yarl import URL

from frigate_event_handler.const import LOGGER as _LOGGER
from frigate_event_handler.exceptions import (
    FrigateApiConnectionError,
    FrigateApiConnectionTimeoutError,
    FrigateApiError,
    FrigateApiNotFoundError,
    FrigateApiRateLimitError,
)
from frigate_event_handler.models import StatusResponse


@dataclass
class FrigateApiClient:
    base_url: str
    api_key: str | None = None
    session: ClientSession | None = None

    request_timeout: int = 15

    _close_session: bool = False

    def __post_init__(self):
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

    def close(self):
        if self.session and self._close_session:
            self.session.close()

    @property
    def request_header(self) -> dict[str, str]:
        """Generate a header for HTTP requests to the server."""
        return {
            "Accept": "application/json",
            "User-Agent": "FrigateEventHandler/1.0",
        }

    @staticmethod
    async def _request_check_status(response: ClientResponse):
        if response.status == HTTPStatus.TOO_MANY_REQUESTS:
            raise FrigateApiRateLimitError("Too many requests to Frigate API. Try again later.")
        if response.status == HTTPStatus.NOT_FOUND:
            raise FrigateApiNotFoundError("Resource not found")
        if response.status == HTTPStatus.BAD_REQUEST:
            raise FrigateApiError("Bad request syntax or unsupported method")
        if response.status != HTTPStatus.OK:
            raise FrigateApiError(response)

    async def _request(
        self,
        uri: str,
        method: str = METH_GET,
        **kwargs,
    ):
        url = URL(f"{self.base_url.strip('/')}/").join(URL(uri))

        headers = kwargs.get("headers")
        headers = self.request_header if headers is None else dict(headers)

        params = kwargs.get("params")
        if params is not None:
            kwargs.update(params={k: v for k, v in params.items() if v is not None})

        _LOGGER.debug(
            "Executing %s API request to %s.",
            method,
            url.with_query(kwargs.get("params")),
        )

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    **kwargs,
                    headers=headers,
                    raise_for_status=self._request_check_status,
                )
        except asyncio.TimeoutError as exception:
            raise FrigateApiConnectionTimeoutError(
                "Timeout occurred while connecting to NRK API"
            ) from exception
        except (
            ClientError,
            ClientResponseError,
        ) as exception:
            msg = f"Error occurred while communicating with NRK API: {exception}"
            raise FrigateApiConnectionError(msg) from exception

        if response.status in [HTTPStatus.NO_CONTENT, HTTPStatus.ACCEPTED]:
            return None
        content_type = response.headers.get("Content-Type", "")
        if "video" in content_type or "image" in content_type:
            return await response.read()

        text = await response.text()
        if "application/json" not in content_type:
            msg = "Unexpected response from the NRK API"
            raise FrigateApiError(
                msg,
                {"Content-Type": content_type, "response": text},
            )
        return orjson.loads(text)

    async def event_clip(self, event_id: str) -> bytes | None:
        try:
            return await self._request(f"events/{event_id}/clip.mp4")
        except FrigateApiNotFoundError:
            return None

    async def event_snapshot(self, event_id: str) -> bytes | None:
        try:
            return await self._request(f"events/{event_id}/snapshot.jpg")
        except FrigateApiNotFoundError:
            return None

    async def set_event_description(self, event_id: str, description: str) -> StatusResponse:
        result = await self._request(
            f"events/{event_id}/description",
            method=METH_POST,
            json={
                "description": description,
            },
        )

        return StatusResponse.from_dict(result)

    async def set_event_sub_label(
        self,
        event_id: str,
        label: str,
        score: float | None = None,
    ) -> StatusResponse:
        data = {
            "subLabel": label,
        }
        if score is not None:
            data["subLabelScore"] = score

        result = await self._request(
            f"events/{event_id}/sub_label",
            method=METH_POST,
            json=data,
        )
        return StatusResponse.from_dict(result)
