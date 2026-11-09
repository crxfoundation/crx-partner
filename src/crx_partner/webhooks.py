"""Webhook signature check."""

from __future__ import annotations

import hashlib
import hmac
import time

HEADER = "CRX-Webhook-Signature"


def verify_webhook(secret: str, signature_header: str | None, body: str | bytes, tolerance: float = 300) -> bool:
    """Return True when ``signature_header`` signs ``body`` with ``secret`` and its time is within
    ``tolerance`` seconds of now.

    ``secret`` is the endpoint's full ``whsec_`` secret. ``signature_header`` is the value of the
    CRX-Webhook-Signature header: ``t=<unix seconds>,v1=<hex HMAC-SHA256 of "<t>.<body>">``. ``body`` is
    the request body exactly as received, before any JSON parse.
    """
    if not isinstance(secret, str) or not secret or not isinstance(signature_header, str):
        return False
    raw = body.encode("utf-8") if isinstance(body, str) else bytes(body)
    t = None
    sigs: list[str] = []
    for part in signature_header.split(","):
        name, _, value = part.strip().partition("=")
        if name == "t" and value.isascii() and value.isdigit() and len(value) <= 12:
            t = value
        elif name == "v1" and value and value.isascii():
            sigs.append(value.lower())
    if t is None or not sigs or abs(time.time() - int(t)) > tolerance:
        return False
    want = hmac.new(secret.encode("utf-8"), t.encode() + b"." + raw, hashlib.sha256).hexdigest()
    return any(hmac.compare_digest(want, s) for s in sigs)
