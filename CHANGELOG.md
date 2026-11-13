# Changelog

## 0.3.2 (13 Nov 2026)

- Added the approved end-user methods: `end_users(status=None)`, `end_user(external_customer_id)`, `add_end_users(users)` (each `{"external_customer_id": ..., "label": ...}`) and `remove_end_users(external_customer_ids)`. Each end user is your own customer, under your own customer ID.
- Added `balance()`: your firm's account balance.
- `audit()` takes `external_customer_id`: the rows of one end user.
- Every other method, argument and answer is unchanged.

## 0.3.1 (12 Nov 2026)

- A read with no answer, or a 502, 503 or 504, is sent once more after a random pause of 0.5 to 1 s. Before, the pause was 0.5 s. A read still goes at most twice, and a write once.
- Deprecated: `brand()`, `logo()`, `published_logo()`, `save_brand()`, `upload_logo()` and `publish_brand()`, removed in 0.2.0 and 0.3.0, are back with their 0.1.0 arguments. Each calls its 0.1.0 route. `published_logo()` reads a published logo. The API refuses the other five: each raises `ApiError`, as on 0.1.0.

## 0.3.0 (10 Nov 2026)

- Removed `brand()`, `logo()` and `published_logo()`: the API no longer serves the brand to API keys.
- Added the KYB methods, one per KYB route: `kyb_fields`, `kyb_cases`, `kyb_create_case`, `kyb_case`, `kyb_save_answers`, `kyb_confirm_section`, `kyb_upload_document`, `kyb_remove_document`, `kyb_documents_done`, `kyb_id_check_link`, `kyb_set_wallet`, `kyb_submit` and `kyb_withdraw`. `kyb_upload_document` sends the file's bytes with `content_type`; the signature hashes those bytes.
- `ApiError` adds `reason` and `details` (`missing`, `caseId`, `documentId`) for a KYB refusal.

## 0.2.0 (10 Nov 2026)

- Removed `save_brand`, `upload_logo` and `publish_brand` (`PUT /brand`, `POST /brand/logo`, `POST /brand/publish`). CRX sets the brand of your clients' onboarding screens: contact CRX to change it.
- `brand()` answers `published` and `publishedAt`. The `draft` field is gone.
- A brand holds no `colors` and no `font`: every client onboarding screen keeps CRX's colours and font.
- `logo(id=)` reads the published logo alone.
- `python -m crx_partner keygen` has no use in the console: the console makes each key in the browser and takes no public key.

## 0.1.0 (9 Nov 2026)

- First release. `crx_partner.Manage` calls the Manage API: one method per API route, made from the API's OpenAPI document.
- Each call is signed with the API key: Ed25519 over the method, the path with its query, the timestamp, the nonce and the SHA-256 of the body. The key file is the PKCS#8 PEM file the console saves.
- A write sends an Idempotency-Key, or the `idempotency_key=` given.
- A refusal raises `crx_partner.ApiError` with `status`, `code`, `message` and `field`.
- `crx_partner.verify_webhook` checks the CRX-Webhook-Signature header of a webhook delivery.
- `python -m crx_partner keygen` makes a key pair; `python -m crx_partner me` reads the caller.
