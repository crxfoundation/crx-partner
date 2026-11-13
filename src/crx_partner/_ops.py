# Generated from openapi/manage.json. Do not edit.
"""The API methods: one per operation of each OpenAPI document."""

from __future__ import annotations

from typing import Any


class ManageOps:
    """The Manage API methods of crx_partner.Manage."""

    default_base_url = "https://manage.crxfx.com/api/v1"
    key_id_prefix = "mk_"
    signing_prefix = "CRX-MANAGE-V1"
    _call: Any

    def me(self) -> Any:
        """Read the operator and the caller.

        Answer (dict): Operator id and name, the caller, and the caller's role.
        """
        return self._call("GET", "/me")

    def balance(self) -> Any:
        """Read your firm's account balance.

        Answer (dict): asOf: the time of the balance; readAt: the time it was read; collateral, free and
        locked: USDC amounts as strings. Locked is held as margin. A firm with no account answers 404; a
        balance that cannot be read, 503.
        """
        return self._call("GET", "/balance")

    def team(self) -> Any:
        """List the operator's members.

        Answer (dict): Members: email, name, member role, console role, idCheck (`passed`, `pending`, `failed`
        or `none`) and screen (`clear`, `hold` or `pending`); both null when they cannot be read; screen null
        unless the caller is an admin.
        """
        return self._call("GET", "/team")

    def set_team_role(
        self, *, email: Any = None, role: Any = None, idempotency_key: str | None = None
    ) -> Any:
        """Set a member's console role. The last admin keeps the admin role.

        Answer (dict): The member with the new console role.

        Args:
            email: The member's email.
            role: `admin`, `reviewer` or `viewer`.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/team/role",
            body={"email": email, "role": role},
            idempotency_key=idempotency_key,
        )

    def end_users(self, *, status: Any = None, external_customer_id: Any = None) -> Any:
        """List your approved end users, newest first.

        Answer (dict): endUsers: externalCustomerId, label (null for none), status (`active` or `removed`),
        addedAt and removedAt (Unix milliseconds; removedAt null while active), addedBy and removedBy (an
        email or an API key ID).

        Args:
            status: `active` or `removed`. Default: both.
            external_customer_id: One end user's ID: that end user alone, else 404. In a raw URL, encode it,
                and `+` as `%2B`.
        """
        return self._call(
            "GET",
            "/end-users",
            query={"status": status, "externalCustomerId": external_customer_id},
        )

    def add_end_users(self, *, users: Any = None, idempotency_key: str | None = None) -> Any:
        """Add approved end users, each by your firm's own customer ID.

        Answer (dict): added, kept and reactivated: the number of end users in each.

        Args:
            users: 1 to 1,000 end users. Each: externalCustomerId, your firm's own customer ID, kept as given
                (1 to 128 printable ASCII characters); label, optional, at most 80 characters.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call("POST", "/end-users", body={"users": users}, idempotency_key=idempotency_key)

    def remove_end_users(
        self, *, external_customer_ids: Any = None, idempotency_key: str | None = None
    ) -> Any:
        """Remove approved end users.

        Answer (dict): removed and absent: the number of IDs in each.

        Args:
            external_customer_ids: 1 to 1,000 IDs of your end users.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/end-users/remove",
            body={"externalCustomerIds": external_customer_ids},
            idempotency_key=idempotency_key,
        )

    def clients(self) -> Any:
        """List client firms.

        Answer (dict): Clients: firmId, name, KYB state, current step, who acts next, since, updatedAt.
        """
        return self._call("GET", "/clients")

    def client(self, firm_id: str) -> Any:
        """Read one client's KYB file.

        Answer (dict): KYB steps (key, label, status, who), people checks and invites.
        """
        return self._call("GET", "/clients/{firmId}", params={"firmId": firm_id})

    def client_accounts(self, firm_id: str) -> Any:
        """Read one client's account summary.

        Answer (dict): `{available: true}` with seats, desk status, balances summary, trades summary and open
        positions. A client whose account data is not open to the operator answers `{available: false}` and no
        other field.
        """
        return self._call("GET", "/clients/{firmId}/accounts", params={"firmId": firm_id})

    def client_balances(self, firm_id: str) -> Any:
        """Read one client's balances.

        Answer (dict): `{available: true}` with asOf and balances: asset, free and locked. Locked is held as
        margin. A client whose account data is not open to the operator answers `{available: false}` and no
        other field.
        """
        return self._call("GET", "/clients/{firmId}/balances", params={"firmId": firm_id})

    def client_trades(
        self, firm_id: str, *, status: Any = None, since: Any = None, limit: Any = None, cursor: Any = None
    ) -> Any:
        """List one client's trades, newest first.

        Answer (dict): `{available: true}` with trades and `next`, the cursor of the next page or null. A
        trade: id, pair, side, notional, notionalCurrency, rate, valueDate, status (`pending`, `open`,
        `closed` or `refused`), openedAt, closedAt, and pnlUsd, the result the client's desk shows or null.
        Null where the client's account holds no value: side (a leg whose side the account does not show),
        rate, valueDate (a refused trade), openedAt (a trade still being sent), closedAt (not closed),
        notionalCurrency (a pair that does not parse), pnlUsd (an open trade, or no fixing yet). The list
        holds every open and pending trade and the most recent closed trades. `truncated` is true when older
        closed trades exist and are not listed. A client whose account data is not open to the operator
        answers `{available: false}` and no other field.

        Args:
            status: `open`, `closed` or `all`. Default: `all`. `open` leaves out `pending` and `closed` leaves
                out `refused`: both come with `all` alone.
            since: ISO time with `Z` or an offset: trades opened at or after it. In a raw URL, encode `+` as
                `%2B`.
            limit: The most trades to answer, 1 to 200. Default: 50.
            cursor: The `next` value of the previous answer: the page after it.
        """
        return self._call(
            "GET",
            "/clients/{firmId}/trades",
            params={"firmId": firm_id},
            query={"status": status, "since": since, "limit": limit, "cursor": cursor},
        )

    def invites(self) -> Any:
        """List invites.

        Answer (dict): Invites with their state.
        """
        return self._call("GET", "/invites")

    def invite(
        self, *, kind: Any = None, firm_name: Any = None, contact_email: Any = None, contact_name: Any = None,
        firm_id: Any = None, email: Any = None, name: Any = None, idempotency_key: str | None = None
    ) -> Any:
        """Invite a client firm or a person of a client firm.

        Answer (dict): The invite. A person invite carries its link.

        Args:
            kind: `firm` or `person`.
            firm_name: Firm invite: the client firm's name.
            contact_email: Firm invite: the contact's email.
            contact_name: Firm invite: the contact's name.
            firm_id: Person invite: the client firm.
            email: Person invite: the person's email.
            name: Person invite: the person's name.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/invites",
            body={
                "kind": kind,
                "firmName": firm_name,
                "contactEmail": contact_email,
                "contactName": contact_name,
                "firmId": firm_id,
                "email": email,
                "name": name,
            },
            idempotency_key=idempotency_key,
        )

    def resend_invite(self, id: str, *, idempotency_key: str | None = None) -> Any:
        """Issue a new link. The previous link stops working.

        Answer (dict): The invite. A person invite carries its new link.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call("POST", "/invites/{id}/resend", params={"id": id}, idempotency_key=idempotency_key)

    def revoke_invite(self, id: str, *, idempotency_key: str | None = None) -> Any:
        """Revoke an invite. Its link stops working.

        Answer (dict): The revoked invite.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call("POST", "/invites/{id}/revoke", params={"id": id}, idempotency_key=idempotency_key)

    def kyb_fields(self) -> Any:
        """List the fields and documents a KYB case takes, and the countries CRX onboards.

        Answer (dict): `fields`: key, section, type (`string`, `boolean`, `number` or `choice`) and label,
        with choices (each a `value` and its `label`), maxLength, format and help (when the field applies)
        where they apply. `sections`: business, eligibility, people, ownership and documents, in order.
        `countries`: the countries a case may name, ISO 3166-1 alpha-2. `documents`: each document a case may
        ask: key (the CRX-Requirement value of its upload), label and help (when CRX asks it).
        """
        return self._call("GET", "/kyb/fields")

    def kyb_cases(self, *, after: Any = None, limit: Any = None) -> Any:
        """List the KYB cases you opened through the API, newest first.

        Answer (dict): `data`: one item a case: caseId, externalId, firmId, state, version, returns and
        updatedAt. `hasMore`, and `nextCursor`: the cursor of the next page, or null. GET /kyb/cases/{caseId}
        reads a case in full.

        Args:
            after: The `nextCursor` value of the previous answer: the page after it.
            limit: The most cases to answer, 1 to 100. Default: 20.
        """
        return self._call("GET", "/kyb/cases", query={"after": after, "limit": limit})

    def kyb_create_case(
        self, *, external_id: Any = None, firm_name: Any = None, country: Any = None, lei: Any = None,
        registration_number: Any = None, contact: Any = None, idempotency_key: str | None = None
    ) -> Any:
        """Open a KYB case for a client firm.

        Answer (dict): The case.

        Args:
            external_id: Optional. Your own id for the client, unique among your cases, at most 100
                characters.
            firm_name: The client firm's legal name.
            country: The country of registration: ISO 3166-1 alpha-2, one of `countries` of GET /kyb/fields,
                for example `GB`.
            lei: Optional. The firm's LEI: 20 characters.
            registration_number: Optional. The firm's registration number.
            contact: The client's contact: `name` and `email`, a company address. The client firm is the
                address's firm.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases",
            body={
                "externalId": external_id,
                "firmName": firm_name,
                "country": country,
                "lei": lei,
                "registrationNumber": registration_number,
                "contact": contact,
            },
            idempotency_key=idempotency_key,
        )

    def kyb_case(self, case_id: str) -> Any:
        """Read one KYB case: its state, its steps, what is due, its people and its documents.

        Answer (dict): The case: caseId, externalId, firmId (the client firm, as GET /clients/{firmId} names
        it, or null), state (`preparing`, `in_progress`, `with_crx`, `approved`, `declined` or `closed`;
        `invited` for clients CRX invites: an API case goes from `preparing` to `in_progress`), version,
        returns (the count of CRX's requests for more information so far), createdAt, updatedAt, firmName,
        country, steps (key, and state: `not_started`, `current`, `waiting` or `done`), requirements (`due`:
        key, section, code and message, and sections on `crx_request`; `waiting`: who, code and message, and
        personKey when the item names a person), people (personKey, roles, the ID check's state and the
        signature's state), documents, and decision (outcome and decidedAt, or null). `version` rises by 1 at
        each change of the case.
        """
        return self._call("GET", "/kyb/cases/{caseId}", params={"caseId": case_id})

    def kyb_save_answers(
        self, case_id: str, *, fields: Any = None, idempotency_key: str | None = None
    ) -> Any:
        """Save answers on a case. A field given as null is cleared.

        Answer (dict): The case.

        Args:
            fields: An object: a field key of GET /kyb/fields → its value, or null to clear it. None leaves
                the field out; pass '' (an empty string) for none.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/answers",
            params={"caseId": case_id},
            body={"fields": fields},
            idempotency_key=idempotency_key,
        )

    def kyb_confirm_section(self, case_id: str, section: str, *, idempotency_key: str | None = None) -> Any:
        """Confirm a section of a case: business, eligibility, people or ownership.

        Answer (dict): The case.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/sections/{section}/confirm",
            params={"caseId": case_id, "section": section},
            idempotency_key=idempotency_key,
        )

    def kyb_upload_document(
        self, case_id: str, *, data: bytes, content_type: str, filename: str, requirement: str,
        idempotency_key: str | None = None
    ) -> Any:
        """Upload one document to a case: PDF, PNG or JPEG, at most 10 MB.

        Answer (dict): The document: documentId, requirement, filename, contentType, size, sha256 and
        uploadedAt.

        Args:
            data: The file's bytes.
            content_type: The file's type: application/pdf, image/png or image/jpeg.
            filename: The file name: 1 to 200 characters, with no / or \\.
            requirement: The requirement the file meets: the `key` of a document item the case lists as due.
                `documents` of GET /kyb/fields names each.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/documents",
            params={"caseId": case_id},
            headers={"CRX-Filename": filename, "CRX-Requirement": requirement},
            data=data,
            content_type=content_type,
            idempotency_key=idempotency_key,
        )

    def kyb_remove_document(
        self, case_id: str, document_id: str, *, idempotency_key: str | None = None
    ) -> Any:
        """Remove a document from a case. CRX keeps the file on record.

        Answer (dict): The case.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/documents/{documentId}/remove",
            params={"caseId": case_id, "documentId": document_id},
            idempotency_key=idempotency_key,
        )

    def kyb_documents_done(self, case_id: str, *, idempotency_key: str | None = None) -> Any:
        """Mark the documents step of a case done.

        Answer (dict): The case.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/documents/done",
            params={"caseId": case_id},
            idempotency_key=idempotency_key,
        )

    def kyb_id_check_link(self, case_id: str, person_key: str, *, idempotency_key: str | None = None) -> Any:
        """Get a link to a person's ID check, on a CRX page. The person's previous link stops working.

        Answer (dict): `url`, the link, and `expiresAt`.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/people/{personKey}/id-check-link",
            params={"caseId": case_id, "personKey": person_key},
            idempotency_key=idempotency_key,
        )

    def kyb_set_wallet(
        self, case_id: str, *, type: Any = None, custody: Any = None, custodian: Any = None,
        idempotency_key: str | None = None
    ) -> Any:
        """Answer the wallet step of a case: the client adds its wallet in Discover.

        Answer (dict): The case.

        Args:
            type: `none`: no wallet address on the case; the client adds the wallet in Discover.
            custody: Optional. How the client holds its assets: `fireblocks`, `bitgo`, `other` (with
                custodian) or `self_hosted`.
            custodian: Optional. With custody `other`: the custodian's name.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/wallet",
            params={"caseId": case_id},
            body={"type": type, "custody": custody, "custodian": custodian},
            idempotency_key=idempotency_key,
        )

    def kyb_submit(self, case_id: str, *, idempotency_key: str | None = None) -> Any:
        """Send a case to CRX for review.

        Answer (dict): The case.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/submit",
            params={"caseId": case_id},
            idempotency_key=idempotency_key,
        )

    def kyb_withdraw(self, case_id: str, *, idempotency_key: str | None = None) -> Any:
        """Withdraw a case before CRX decides.

        Answer (dict): The case.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/kyb/cases/{caseId}/withdraw",
            params={"caseId": case_id},
            idempotency_key=idempotency_key,
        )

    def webhooks(self) -> Any:
        """List webhook endpoints.

        Answer (dict): Endpoints: id, url, events, description, keyId (the API key the endpoint belongs to,
        else null), createdAt, by.
        """
        return self._call("GET", "/webhooks")

    def add_webhook(
        self, *, url: Any = None, events: Any = None, description: Any = None,
        idempotency_key: str | None = None
    ) -> Any:
        """Add a webhook endpoint.

        Answer (dict): The endpoint and its signing secret. The secret is in this answer only.

        Args:
            url: An https URL on a public address. Redirects are not followed.
            events: One or more of invite.sent, invite.resent, invite.revoked, kyb.case.updated,
                kyb.case.created, kyb.case.changed, kyb.case.returned, kyb.case.decided, kyb.person.updated,
                trade.opened, trade.closed, ping.
            description: Optional, at most 120 characters.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/webhooks",
            body={"url": url, "events": events, "description": description},
            idempotency_key=idempotency_key,
        )

    def delete_webhook(self, id: str, *, idempotency_key: str | None = None) -> Any:
        """Delete a webhook endpoint. Pending retries stop.

        Answer (dict): The deleted endpoint's id.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call("POST", "/webhooks/{id}/delete", params={"id": id}, idempotency_key=idempotency_key)

    def test_webhook(self, id: str, *, idempotency_key: str | None = None) -> Any:
        """Send a ping event to one endpoint, once.

        Answer (dict): The delivery attempt.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call("POST", "/webhooks/{id}/test", params={"id": id}, idempotency_key=idempotency_key)

    def webhook_deliveries(self, id: str) -> Any:
        """List an endpoint's delivery attempts, newest first.

        Answer (dict): Deliveries: id, eventId, type, attempt, status, responseStatus, error, at,
        nextAttemptAt.
        """
        return self._call("GET", "/webhooks/{id}/deliveries", params={"id": id})

    def audit(
        self, *, from_: Any = None, to: Any = None, action: Any = None, actor: Any = None, format: Any = None,
        limit: Any = None, external_customer_id: Any = None
    ) -> Any:
        """Read the activity log.

        Answer (dict; str for format='csv'): Rows: at, actor, via, action, target, result, detail. A row whose
        target is an end user's adds externalCustomerId, the exact ID, when it resolves.

        Args:
            from_: ISO time, inclusive.
            to: ISO time, exclusive.
            action: One action. Repeat it to read several.
            actor: One actor.
            format: `csv` for a CSV file.
            limit: The most rows to answer, 1 to 5000. Default: 500.
            external_customer_id: One end user's ID: the rows of that end user alone. In a raw URL, encode it,
                and `+` as `%2B`.
        """
        return self._call(
            "GET",
            "/audit",
            query={
                "from": from_,
                "to": to,
                "action": action,
                "actor": actor,
                "format": format,
                "limit": limit,
                "externalCustomerId": external_customer_id,
            },
        )

    def openapi(self) -> Any:
        """Read this API as an OpenAPI 3.1 document. Served on the manage host alone.

        Answer (dict): The OpenAPI document.
        """
        return self._call("GET", "/openapi.json", auth=False)


class ManageDeprecatedOps:
    """The deprecated 0.1.0 methods of crx_partner.Manage: each calls its 0.1.0 route."""

    _call: Any

    def brand(self) -> Any:
        """Deprecated. Read the brand. The API refuses this call: the method raises ApiError."""
        return self._call("GET", "/brand")

    def save_brand(
        self, *, display_name: Any = None, colors: Any = None, font: Any = None, sender_name: Any = None,
        support_email: Any = None, texts: Any = None, logo: Any = None, idempotency_key: str | None = None
    ) -> Any:
        """Deprecated. Save the brand draft. The API refuses this call: the method raises ApiError.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "PUT",
            "/brand",
            body={
                "displayName": display_name,
                "colors": colors,
                "font": font,
                "senderName": sender_name,
                "supportEmail": support_email,
                "texts": texts,
                "logo": logo,
            },
            idempotency_key=idempotency_key,
        )

    def upload_logo(self, *, type: Any = None, data: Any = None, idempotency_key: str | None = None) -> Any:
        """Deprecated. Upload a logo. The API refuses this call: the method raises ApiError.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call(
            "POST",
            "/brand/logo",
            body={"type": type, "data": data},
            idempotency_key=idempotency_key,
        )

    def logo(self, *, id: Any = None) -> Any:
        """Deprecated. Read a logo of the operator. The API refuses this call: the method raises ApiError."""
        return self._call("GET", "/brand/logo", query={"id": id})

    def published_logo(self, id: str) -> Any:
        """Deprecated. Read a published logo by its id, the brand's logo field.

        Answer (bytes): The image file.
        """
        return self._call("GET", "/brand/logo/{id}", params={"id": id}, auth=False)

    def publish_brand(self, *, idempotency_key: str | None = None) -> Any:
        """Deprecated. Publish the brand draft. The API refuses this call: the method raises ApiError.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call("POST", "/brand/publish", idempotency_key=idempotency_key)
