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

    def team(self) -> Any:
        """List the operator's members.

        Answer (dict): Members: email, name, member role, console role.
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
        notionalCurrency (a pair that does not parse), pnlUsd (an open trade, or no fixing yet). A client
        whose account data is not open to the operator answers `{available: false}` and no other field.

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

        Answer (dict): The invite with its new link.

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

    def brand(self) -> Any:
        """Read the draft and the published brand.

        Answer (dict): Draft, published and publishedAt.
        """
        return self._call("GET", "/brand")

    def save_brand(
        self, *, display_name: Any = None, colors: Any = None, font: Any = None, sender_name: Any = None,
        support_email: Any = None, texts: Any = None, logo: Any = None, idempotency_key: str | None = None
    ) -> Any:
        """Save the brand draft.

        Answer (dict): The saved draft.

        Args:
            display_name: At most 60 characters.
            colors: primary, primaryText, background, text, accent: hex colours. Text contrast is at least
                4.5:1.
            font: Inter.
            sender_name: At most 60 characters.
            support_email: An email address, or null for none. An empty string also reads as none. None leaves
                the field out; pass '' (an empty string) for none.
            texts: welcomeTitle (60), welcomeBody (300), helpLine (200), doneBody (300).
            logo: Optional. A stored logo id (the brand's logo field), or null or an empty string for no logo.
                Absent: the draft keeps its current logo. None leaves the field out; pass '' (an empty string)
                for none.
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
        """Upload the logo: PNG, JPEG or WebP, at most 200 KB and 1024 px. The body is JSON with Content-Type
        application/json, at most 300 KB.

        Answer (dict): The logo id, type, width and height, and the draft with the new logo.

        Args:
            type: `image/png`, `image/jpeg` or `image/webp`. The file's own bytes decide its type.
            data: The image file in base64.
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
        """Read one of the operator's logos: the draft's, the published one's or the last upload.

        Answer (bytes): The image file.

        Args:
            id: The logo id, the brand's logo field.
        """
        return self._call("GET", "/brand/logo", query={"id": id})

    def published_logo(self, id: str) -> Any:
        """Read a published logo by its id, the brand's logo field.

        Answer (bytes): The image file.
        """
        return self._call("GET", "/brand/logo/{id}", params={"id": id}, auth=False)

    def publish_brand(self, *, idempotency_key: str | None = None) -> Any:
        """Publish the draft.

        Answer (dict): The published brand and publishedAt.

        Args:
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        return self._call("POST", "/brand/publish", idempotency_key=idempotency_key)

    def webhooks(self) -> Any:
        """List webhook endpoints.

        Answer (dict): Endpoints: id, url, events, description, createdAt, by.
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
            events: One or more of invite.sent, invite.resent, invite.revoked, kyb.case.updated, trade.opened,
                trade.closed, ping.
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
        limit: Any = None
    ) -> Any:
        """Read the audit log.

        Answer (dict; str for format='csv'): Rows: at, actor, via, action, target, result, detail.

        Args:
            from_: ISO time, inclusive.
            to: ISO time, exclusive.
            action: One action. Repeat it to read several.
            actor: One actor.
            format: `csv` for a CSV file.
            limit: The most rows to answer, 1 to 5000. Default: 500.
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
            },
        )

    def openapi(self) -> Any:
        """Read this API as an OpenAPI 3.1 document. Served on the manage host alone.

        Answer (dict): The OpenAPI document.
        """
        return self._call("GET", "/openapi.json", auth=False)
