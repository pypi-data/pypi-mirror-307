"""frigate-event-handler exceptions."""


class FrigateApiError(Exception):
    """Generic Frigate exception."""


class FrigateApiNotFoundError(FrigateApiError):
    """Frigate not found exception."""


class FrigateApiConnectionError(FrigateApiError):
    """Frigate connection exception."""


class FrigateApiConnectionTimeoutError(FrigateApiConnectionError):
    """Frigate connection timeout exception."""


class FrigateApiRateLimitError(FrigateApiConnectionError):
    """Frigate Rate Limit exception."""


class FrigateApiAuthenticationError(FrigateApiError):
    """Frigate authentication exception."""


class FrigateApiAuthorizationError(FrigateApiError):
    """Frigate authorization error."""


class FrigateApiAccessDeniedError(FrigateApiError):
    """Frigate access denied error."""
