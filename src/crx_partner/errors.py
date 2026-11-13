"""Errors the SDK raises. Branch on ``err.code``, which is stable across releases."""

from __future__ import annotations

from typing import Any

# The error fields a KYB refusal may add beside ``reason``, kept in ``ApiError.details``.
DETAIL_FIELDS = ("missing", "caseId", "documentId")

# The code of a refusal with no readable error body, by HTTP status.
STATUS_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    429: "rate_limited",
}


def clean(value: Any, limit: int = 300) -> str:
    """Return ``value`` as one printable line of at most ``limit`` characters."""
    return "".join(ch if ch.isprintable() else " " for ch in str(value))[:limit]


class ApiError(Exception):
    """A refused or failed call.

    Attributes:
        status: The HTTP status, or None when no answer came.
        code: The API's error code (``bad_request``, ``unauthorized``, ``forbidden``, ``not_found``,
            ``conflict``, ``rate_limited``, ``unavailable``), or the SDK's own (``config``, ``network``,
            ``bad_answer``).
        message: The API's message.
        field: The body field the error is about, or None.
        request_id: The CRX-Request-Id of the answer, or None.
        reason: Why a KYB conflict refused the write (``missing_requirements``, ``case_locked``,
            ``duplicate_external_id``, ``case_exists``, ``duplicate_document``, ``link_unavailable``,
            ``no_wallet_step``), or None.
        details: The KYB fields of the refusal as the API sent them: ``missing`` (the items still due),
            ``caseId`` or ``documentId``. Empty for none.
    """

    def __init__(
        self, status: int | None, code: str, message: str, field: str | None = None, request_id: str | None = None,
        reason: str | None = None, details: dict[str, Any] | None = None,
    ) -> None:
        self.status = status
        self.code = clean(code, 64)
        self.message = clean(message, 500)
        self.field = None if field is None else clean(field, 100)
        self.request_id = None if request_id is None else clean(request_id, 64)
        self.reason = None if reason is None else clean(reason, 64)
        self.details = dict(details or {})
        super().__init__(f"{self.code}: {self.message}")

    def __repr__(self) -> str:
        return (f"{type(self).__name__}(status={self.status!r}, code={self.code!r}, message={self.message!r}, "
                f"field={self.field!r})")


class ConfigError(ApiError):
    """The client setup is not valid: a missing or bad key, key id or base URL. Nothing was sent."""

    def __init__(self, message: str) -> None:
        super().__init__(None, "config", message)


class NetworkError(ApiError):
    """The API did not answer. Read the state before you send a write again, or resend it with the same
    ``idempotency_key``."""

    def __init__(self, message: str) -> None:
        super().__init__(None, "network", message)
