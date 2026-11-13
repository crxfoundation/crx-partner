# CRX Partner SDK

Call the CRX Manage API from Python. The SDK is for operators.

## Quickstart

The same three steps as the API page's Quickstart in the operator console.

### 1. Make a key

Create an API key: API, Quickstart, Create a key. Name it and pick its permissions: each permission is one set of calls, and a call outside the key's set answers 403. The browser makes the key and shows it once, under the key's row on the API access list. Copy it and save it as a file named `partner.key`. CRX stores the public key only. The key id is `mk_` and 16 hex characters.

### 2. Install the SDK

Install the SDK on Python 3.10 or later.

```bash
pip install "git+https://github.com/crxfoundation/crx-partner@v0.3.1"
```

Point the SDK at your key: the key id shown with the key, and the path of `partner.key`, the key you saved. Keep the key file readable by you alone.

```bash
export CRX_PARTNER_KEY_ID="mk_<16 hex characters>"
export CRX_PARTNER_KEY_FILE="$HOME/partner.key"
chmod 600 "$CRX_PARTNER_KEY_FILE"
```

### 3. First call

Read your firm with the key.

```python
import crx_partner

m = crx_partner.Manage()  # reads CRX_PARTNER_KEY_ID and CRX_PARTNER_KEY_FILE
print(m.me())             # {'operator': ..., 'name': ..., 'role': 'viewer', 'via': 'api', ...}
```

The same call from the shell: `python -m crx_partner me`.

## Client

`crx_partner.Manage(key_id=None, key_file=None, base_url=None, timeout=30)`.

| Argument | Setting | Default |
|---|---|---|
| `key_id` | `CRX_PARTNER_KEY_ID` | None |
| `key_file` | `CRX_PARTNER_KEY_FILE` | None |
| `base_url` | `CRX_PARTNER_BASE_URL` | `https://manage.crxfx.com/api/v1` |
| `timeout` | | 30 seconds |

The key file is the PKCS#8 PEM file of the key's private key. When other users can open the file and it is yours, the SDK sets it to owner-only (0600) and prints `set partner.key to owner-only (0600)`. It refuses a key file of another user. The SDK never prints or logs the key. With no key, only the public call works (`openapi()`).

## Calls

Each method calls one route. Path parameters are positional, in path order. Query and body fields are keyword arguments in snake_case (`firm_name` sends `firmName`); a field given as None is left out. A JSON answer returns a dict, a CSV answer a str, an image a bytes.

```python
import crx_partner

m = crx_partner.Manage()
for c in m.clients()["clients"]:
    print(c["firmId"], c["name"])

inv = m.invite(kind="firm", firm_name="Acme Ltd", contact_email="ops@acme.example", contact_name="Ann Lee")
print(inv["invite"]["id"])

csv_text = m.audit(from_="2026-11-01T00:00:00Z", format="csv")
```

Each call is signed with the key (Ed25519, headers CRX-Key-Id, CRX-Timestamp, CRX-Nonce, CRX-Signature). A key takes 60 requests a minute.

A write sends an `Idempotency-Key`. The API keeps it 24 hours: the same key and body answer the first answer again. A write is sent once. When it gets no answer (`NetworkError`), send it again with the same `idempotency_key=`. A read with no answer, or a 502, 503 or 504, is sent once more after a random pause of 0.5 to 1 s.

<!-- methods:start (generated from openapi/manage.json) -->

### Manage

| Method | Route | Returns | Does |
|---|---|---|---|
| `me()` | `GET /me` | dict | Read the operator and the caller. |
| `team()` | `GET /team` | dict | List the operator's members. |
| `set_team_role(email=, role=)` | `POST /team/role` | dict | Set a member's console role. The last admin keeps the admin role. |
| `clients()` | `GET /clients` | dict | List client firms. |
| `client(firm_id)` | `GET /clients/{firmId}` | dict | Read one client's KYB file. |
| `client_accounts(firm_id)` | `GET /clients/{firmId}/accounts` | dict | Read one client's account summary. |
| `client_balances(firm_id)` | `GET /clients/{firmId}/balances` | dict | Read one client's balances. |
| `client_trades(firm_id, status=, since=, limit=, cursor=)` | `GET /clients/{firmId}/trades` | dict | List one client's trades, newest first. |
| `invites()` | `GET /invites` | dict | List invites. |
| `invite(kind=, firm_name=, contact_email=, contact_name=, firm_id=, email=, name=)` | `POST /invites` | dict | Invite a client firm or a person of a client firm. |
| `resend_invite(id)` | `POST /invites/{id}/resend` | dict | Issue a new link. The previous link stops working. |
| `revoke_invite(id)` | `POST /invites/{id}/revoke` | dict | Revoke an invite. Its link stops working. |
| `kyb_fields()` | `GET /kyb/fields` | dict | List the fields and documents a KYB case takes, and the countries CRX onboards. |
| `kyb_cases(after=, limit=)` | `GET /kyb/cases` | dict | List the KYB cases you opened through the API, newest first. |
| `kyb_create_case(external_id=, firm_name=, country=, lei=, registration_number=, contact=)` | `POST /kyb/cases` | dict | Open a KYB case for a client firm. |
| `kyb_case(case_id)` | `GET /kyb/cases/{caseId}` | dict | Read one KYB case: its state, its steps, what is due, its people and its documents. |
| `kyb_save_answers(case_id, fields=)` | `POST /kyb/cases/{caseId}/answers` | dict | Save answers on a case. A field given as null is cleared. |
| `kyb_confirm_section(case_id, section)` | `POST /kyb/cases/{caseId}/sections/{section}/confirm` | dict | Confirm a section of a case: business, eligibility, people or ownership. |
| `kyb_upload_document(case_id, data=, content_type=, filename=, requirement=)` | `POST /kyb/cases/{caseId}/documents` | dict | Upload one document to a case: PDF, PNG or JPEG, at most 10 MB. |
| `kyb_remove_document(case_id, document_id)` | `POST /kyb/cases/{caseId}/documents/{documentId}/remove` | dict | Remove a document from a case. CRX keeps the file on record. |
| `kyb_documents_done(case_id)` | `POST /kyb/cases/{caseId}/documents/done` | dict | Mark the documents step of a case done. |
| `kyb_id_check_link(case_id, person_key)` | `POST /kyb/cases/{caseId}/people/{personKey}/id-check-link` | dict | Get a link to a person's ID check, on a CRX page. The person's previous link stops working. |
| `kyb_set_wallet(case_id, type=, custody=, custodian=)` | `POST /kyb/cases/{caseId}/wallet` | dict | Answer the wallet step of a case: the client adds its wallet in Discover. |
| `kyb_submit(case_id)` | `POST /kyb/cases/{caseId}/submit` | dict | Send a case to CRX for review. |
| `kyb_withdraw(case_id)` | `POST /kyb/cases/{caseId}/withdraw` | dict | Withdraw a case before CRX decides. |
| `webhooks()` | `GET /webhooks` | dict | List webhook endpoints. |
| `add_webhook(url=, events=, description=)` | `POST /webhooks` | dict | Add a webhook endpoint. |
| `delete_webhook(id)` | `POST /webhooks/{id}/delete` | dict | Delete a webhook endpoint. Pending retries stop. |
| `test_webhook(id)` | `POST /webhooks/{id}/test` | dict | Send a ping event to one endpoint, once. |
| `webhook_deliveries(id)` | `GET /webhooks/{id}/deliveries` | dict | List an endpoint's delivery attempts, newest first. |
| `audit(from_=, to=, action=, actor=, format=, limit=)` | `GET /audit` | dict; str for format='csv' | Read the activity log. |
| `openapi()` | `GET /openapi.json` | dict | Read this API as an OpenAPI 3.1 document. Served on the manage host alone. |

<!-- methods:end -->

`client_balances`, `client_trades` and the `trade.opened` and `trade.closed` webhook events answer 404 (events: 400) until CRX opens client balances and trades for your firm.

## Errors

A refused or failed call raises `crx_partner.ApiError`. Branch on `code`.

```python
try:
    m.client("unknown-firm")
except crx_partner.ApiError as e:
    print(e.status, e.code, e.message, e.field)  # 404 not_found No client firm with this id. None
```

| Attribute | Holds |
|---|---|
| `status` | The HTTP status, or None when no answer came. |
| `code` | `bad_request`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `rate_limited` or `unavailable`; the SDK's own `config`, `network` or `bad_answer`. |
| `message` | The API's message. |
| `field` | The body field the error is about, or None. |
| `request_id` | The answer's CRX-Request-Id, or None. |
| `reason` | Why a KYB conflict refused the write: `missing_requirements`, `case_locked`, `duplicate_external_id`, `case_exists`, `duplicate_document`, `link_unavailable` or `no_wallet_step`; else None. |
| `details` | The KYB fields of the refusal, as the API sent them: `missing` (the items still due), `caseId` or `documentId`. Empty for none. |

`crx_partner.ConfigError` (code `config`: a missing or bad key, key id or base URL; nothing was sent) and `crx_partner.NetworkError` (code `network`: no answer) are kinds of `ApiError`.

## Webhooks

A Manage API webhook delivery carries `CRX-Webhook-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256 of "<t>.<body>">`, keyed by the endpoint's `whsec_` secret. Check it on the body exactly as received:

```python
from crx_partner import verify_webhook

if not verify_webhook(secret, request.headers.get("CRX-Webhook-Signature"), request.get_data()):
    return "", 400
```

`verify_webhook(secret, signature_header, body, tolerance=300)` returns False when the signature does not match or its time is more than `tolerance` seconds from now.

## Command line

| Command | Does |
|---|---|
| `python -m crx_partner keygen --out partner.key` | Writes a new private key (PKCS#8 PEM, mode 0600) and prints its public key. Never writes over a file. The console makes each key in the browser and takes no public key: a key from this command cannot call the API. |
| `python -m crx_partner me` | Reads the caller with the key in `CRX_PARTNER_KEY_ID` and `CRX_PARTNER_KEY_FILE`. `--base-url` sets another base. |

