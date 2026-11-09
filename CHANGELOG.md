# Changelog

## 0.1.0 (9 Nov 2026)

- First release. `crx_partner.Manage` calls the Manage API: one method per API route, made from the API's OpenAPI document.
- Each call is signed with the API key: Ed25519 over the method, the path with its query, the timestamp, the nonce and the SHA-256 of the body. The key file is the PKCS#8 PEM file the console saves.
- A write sends an Idempotency-Key, or the `idempotency_key=` given.
- A refusal raises `crx_partner.ApiError` with `status`, `code`, `message` and `field`.
- `crx_partner.verify_webhook` checks the CRX-Webhook-Signature header of a webhook delivery.
- `python -m crx_partner keygen` makes a key pair; `python -m crx_partner me` reads the caller.
