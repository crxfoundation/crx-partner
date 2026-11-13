"""Transport: one signed HTTP call and its answer."""

from __future__ import annotations

import base64
import hashlib
import json
import random
import secrets
import threading
import time
import uuid
from typing import Any, Mapping
from urllib.parse import quote, urlencode, urlsplit

import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .errors import DETAIL_FIELDS, STATUS_CODES, ApiError, ConfigError, NetworkError, clean

USER_AGENT = "crx-partner-python"
GET_RETRY_PAUSE = (0.5, 1.0)  # seconds: the single GET retry waits a random time in this range
GET_RETRIED = (502, 503, 504)  # statuses that send a GET once more
_STAMP_LOCK = threading.Lock()
_last_stamp = 0


def stamp(now_ms: int) -> int:
    """Return a Unix time in milliseconds above the last one in this process."""
    global _last_stamp
    with _STAMP_LOCK:
        _last_stamp = max(int(now_ms), _last_stamp + 1)
        return _last_stamp


def signing_message(prefix: str, method: str, path_with_query: str, ts: str, nonce: str, body: bytes) -> str:
    """The six lines a key call signs, joined by a line feed, with no line feed at the end."""
    return "\n".join([prefix, method.upper(), path_with_query, ts, nonce, hashlib.sha256(body).hexdigest()])


def host_of(url: str) -> str:
    """Return the host only, so a secret in the path, query or userinfo never prints."""
    return clean(urlsplit(url).hostname or "?", 100)


def check_base_url(base_url: str) -> str:
    u = urlsplit(base_url)
    local = u.hostname in ("localhost", "127.0.0.1", "::1")
    if u.scheme != "https" and not (u.scheme == "http" and local):
        raise ConfigError("the base URL must be https (http only for localhost)")
    if u.username or u.password or u.query or u.fragment:
        raise ConfigError("the base URL must carry no credentials, query or fragment")
    return base_url.rstrip("/")


def _query_pairs(query: Mapping[str, Any] | None) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for name, value in (query or {}).items():
        values = value if isinstance(value, (list, tuple)) else [value]
        for v in values:
            if v is None:
                continue
            pairs.append((name, ("true" if v else "false") if isinstance(v, bool) else str(v)))
    return pairs


class Transport:
    """Signs and sends calls to one realm's API."""

    def __init__(
        self, base_url: str, prefix: str, key_id: str | None, private: Ed25519PrivateKey | None, timeout: float,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = check_base_url(base_url)
        self.prefix = prefix
        self.key_id = key_id
        self._key = private
        self.timeout = timeout
        self.session = session or requests.Session()
        self.clock = time.time
        self.sleep = time.sleep

    def __repr__(self) -> str:
        return f"Transport({host_of(self.base_url)})"

    def __getstate__(self) -> Any:
        raise TypeError("a client holds a key and cannot be pickled or copied")

    def url(self, route: str, params: Mapping[str, Any] | None, query: Mapping[str, Any] | None) -> str:
        """The full URL: path parameters percent-encoded, None query values left out."""
        path = route
        for name, value in (params or {}).items():
            if value is None or value == "":
                raise ConfigError(f"the path parameter {name} is missing")
            path = path.replace("{" + name + "}", quote(str(value), safe=""))
        pairs = _query_pairs(query)
        return self.base_url + path + ("?" + urlencode(pairs, quote_via=quote) if pairs else "")

    def sign(self, prepared: requests.PreparedRequest) -> None:
        """Add the four key headers, signed over the path and query as sent and the exact body bytes."""
        if self._key is None or self.key_id is None:
            raise ConfigError("this call needs a key: set CRX_PARTNER_KEY_ID and CRX_PARTNER_KEY_FILE")
        body = prepared.body if isinstance(prepared.body, bytes) else (prepared.body or "").encode()
        ts = str(stamp(int(self.clock() * 1000)))
        nonce = secrets.token_urlsafe(24)
        message = signing_message(self.prefix, prepared.method or "GET", prepared.path_url, ts, nonce, body)
        signature = base64.b64encode(self._key.sign(message.encode())).decode()
        prepared.headers.update({
            "CRX-Key-Id": self.key_id, "CRX-Timestamp": ts, "CRX-Nonce": nonce, "CRX-Signature": signature,
        })

    def _send(
        self, method: str, url: str, raw: bytes | None, auth: bool, idem: str | None, kind: str = "application/json",
        extra: Mapping[str, str] | None = None,
    ) -> requests.Response:
        headers = {"Accept": "application/json", "User-Agent": USER_AGENT, **(extra or {})}
        if raw is not None:
            headers["Content-Type"] = kind
        if idem is not None:
            headers["Idempotency-Key"] = idem
        prepared = self.session.prepare_request(requests.Request(method, url, headers=headers, data=raw))
        if auth:
            self.sign(prepared)
        settings = self.session.merge_environment_settings(prepared.url, {}, None, None, None)
        failed = None
        try:
            # No redirects: signed headers go to this host only.
            return self.session.send(prepared, timeout=self.timeout, allow_redirects=False, **settings)
        except requests.RequestException as e:
            failed = type(e).__name__
        # Raised outside the except block: no context carries the URL.
        raise NetworkError(f"{host_of(self.base_url)} did not answer ({failed})")

    def call(
        self, method: str, route: str, *, params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None, headers: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None, data: bytes | None = None, content_type: str | None = None,
        auth: bool = True, idempotency_key: str | None = None,
    ) -> Any:
        """Send one call and return its answer: a dict for JSON, str for CSV or text, bytes for a file.

        ``body`` is sent as JSON with its None fields left out; with no ``body``, nothing is sent. ``data`` is
        sent as it is, with ``content_type``: a file upload; the signature hashes those bytes. ``headers`` adds
        request headers; a missing one raises ConfigError. A GET with no answer, or a 502, 503 or 504, is sent
        once more after a random pause of 0.5 to 1 s. A write is sent once, with an Idempotency-Key
        (``idempotency_key``, or a new one).
        """
        method = method.upper()
        url = self.url(route, params, query)
        extra: dict[str, str] = {}
        for name, value in (headers or {}).items():
            if value is None or value == "":
                raise ConfigError(f"the header {name} is missing")
            extra[name] = str(value)
        raw = None
        kind = "application/json"
        if data is not None:
            if not isinstance(data, (bytes, bytearray)) or not content_type:
                raise ConfigError("an upload needs data as bytes and its content_type")
            raw, kind = bytes(data), str(content_type)
        elif body is not None:
            raw = json.dumps({k: v for k, v in body.items() if v is not None},
                             separators=(",", ":")).encode()
        write = method != "GET"
        idem = (idempotency_key or uuid.uuid4().hex) if write else None
        tries = 1 if write else 2
        for attempt in range(tries):
            last = attempt == tries - 1
            try:
                r = self._send(method, url, raw, auth, idem, kind, extra)
            except NetworkError:
                if last:
                    raise
                self.sleep(random.uniform(*GET_RETRY_PAUSE))
                continue
            if r.status_code in GET_RETRIED and not last:
                self.sleep(random.uniform(*GET_RETRY_PAUSE))
                continue
            return answer_of(r)
        raise AssertionError("unreachable")


def answer_of(r: requests.Response) -> Any:
    """Return a 2xx answer by its type, or raise ApiError."""
    request_id = r.headers.get("crx-request-id")
    kind = (r.headers.get("content-type") or "").split(";")[0].strip().lower()
    if 200 <= r.status_code < 300:
        if kind == "application/json" or kind.endswith("+json"):
            try:
                return r.json()
            except ValueError:
                raise ApiError(r.status_code, "bad_answer", "the answer is not valid JSON",
                               request_id=request_id) from None
        if kind.startswith("text/"):
            r.encoding = r.encoding or "utf-8"
            return r.text
        return r.content
    err: Any = None
    if kind == "application/json":
        try:
            err = r.json().get("error")
        except (ValueError, AttributeError):
            err = None
    if isinstance(err, dict) and isinstance(err.get("code"), str):
        field = err.get("field")
        reason = err.get("reason")
        details = {k: err[k] for k in DETAIL_FIELDS if k in err}
        raise ApiError(r.status_code, err["code"], str(err.get("message") or ""),
                       field if isinstance(field, str) else None, request_id,
                       reason if isinstance(reason, str) else None, details)
    code = STATUS_CODES.get(r.status_code, "unavailable" if r.status_code >= 500 else "bad_answer")
    raise ApiError(r.status_code, code, f"HTTP {r.status_code} from {host_of(r.url or '')}", request_id=request_id)
