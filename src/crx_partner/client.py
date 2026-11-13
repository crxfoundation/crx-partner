"""The client: Manage, the Manage API for operators."""

from __future__ import annotations

import os
import re
from typing import Any, Mapping

import requests

from ._http import Transport, host_of
from ._keys import load_key_file, public_key_b64
from ._ops import ManageDeprecatedOps, ManageOps
from .errors import ConfigError

ENV_KEY_ID = "CRX_PARTNER_KEY_ID"
ENV_KEY_FILE = "CRX_PARTNER_KEY_FILE"
ENV_BASE_URL = "CRX_PARTNER_BASE_URL"


class _Client:
    """A signed client of one realm's API."""

    realm = ""
    api_name = ""
    default_base_url: str  # the realm's facts come from the generated ops class
    key_id_prefix: str
    signing_prefix: str

    def __init__(
        self, key_id: str | None = None, key_file: str | os.PathLike | None = None, base_url: str | None = None,
        timeout: float = 30, *, session: requests.Session | None = None,
    ) -> None:
        """Make a client.

        Args:
            key_id: The API key id. Default: ``CRX_PARTNER_KEY_ID``.
            key_file: The PKCS#8 PEM file of the key's private key. Default: ``CRX_PARTNER_KEY_FILE``.
            base_url: The API base. Default: ``CRX_PARTNER_BASE_URL``, else the production base.
            timeout: Seconds each call waits for an answer.
            session: A ``requests.Session`` to send with.

        With no key id and no key file, only the public calls work. A key file the current user owns and
        other users can open is set to owner-only (0600); one owned by another user is refused.
        """
        key_id = key_id or os.environ.get(ENV_KEY_ID) or None
        key_file = key_file or os.environ.get(ENV_KEY_FILE) or None
        base_url = base_url or os.environ.get(ENV_BASE_URL) or self.default_base_url
        if (key_id is None) != (key_file is None):
            raise ConfigError(f"set both the key id ({ENV_KEY_ID}) and the key file ({ENV_KEY_FILE}), or neither")
        if key_id is not None and not re.fullmatch(re.escape(self.key_id_prefix) + "[0-9a-f]{16}", key_id):
            raise ConfigError(f"the key id is not a {self.api_name} key id: {self.key_id_prefix} and 16 hex characters")
        key = load_key_file(key_file) if key_file is not None else None
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not 0 < timeout <= 600:
            raise ConfigError("timeout is a number of seconds above 0, at most 600")
        self._t = Transport(base_url, self.signing_prefix, key_id, key, float(timeout), session)
        self.public_key = public_key_b64(key) if key is not None else None

    def __repr__(self) -> str:
        return f"{type(self).__name__}({host_of(self._t.base_url)}, key_id={self._t.key_id!r})"

    def __getstate__(self) -> Any:
        raise TypeError("a client holds a key and cannot be pickled or copied")

    @property
    def base_url(self) -> str:
        return self._t.base_url

    @property
    def key_id(self) -> str | None:
        return self._t.key_id

    def _call(
        self, method: str, route: str, *, params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None, headers: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None, data: bytes | None = None, content_type: str | None = None,
        auth: bool = True, idempotency_key: str | None = None,
    ) -> Any:
        return self._t.call(method, route, params=params, query=query, headers=headers, body=body, data=data,
                            content_type=content_type, auth=auth, idempotency_key=idempotency_key)


class Manage(_Client, ManageOps, ManageDeprecatedOps):
    """The Manage API: the operator console's clients, invites, KYB cases, team, webhooks and audit log."""

    realm = "manage"
    api_name = "Manage API"

