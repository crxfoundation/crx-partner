"""The approved end-user methods of crx_partner.Manage, in Python names.

Each end user is your firm's own customer, approved by your firm, under your own customer ID
(``external_customer_id``): 1 to 128 printable ASCII characters, kept as given. These methods take
and send that name; the API's field is ``externalCustomerId``. They take the place of the generated
``end_users``, ``add_end_users`` and ``remove_end_users`` and accept the same keyword arguments.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping


class EndUserOps:
    """The approved end-user methods of crx_partner.Manage."""

    _call: Any

    def end_users(self, status: str | None = None, *, external_customer_id: str | None = None) -> Any:
        """List your approved end users, newest first.

        Answer (dict): ``endUsers``: each with externalCustomerId, label, status (``active`` or
        ``removed``), addedAt, addedBy, removedAt and removedBy (times in Unix milliseconds).

        Args:
            status: ``"active"`` or ``"removed"``. Default: both.
            external_customer_id: One end user's ID: that end user alone, else ApiError 404.
        """
        return self._call("GET", "/end-users", query={"status": status, "externalCustomerId": external_customer_id})

    def end_user(self, external_customer_id: str) -> dict:
        """Read one approved end user by your customer ID.

        Answer (dict): the end user: externalCustomerId, label, status, addedAt, addedBy, removedAt and
        removedBy. An ID not on your list raises ApiError 404.
        """
        return self.end_users(external_customer_id=external_customer_id)["endUsers"][0]

    def add_end_users(self, users: Iterable[Mapping[str, Any]], *, idempotency_key: str | None = None) -> Any:
        """Add approved end users, 1 to 1,000 in one call.

        An active ID stays as it is (kept); a removed ID is active again (reactivated). A bad row refuses
        the whole call: ApiError 400, its ``field`` names the row, for example
        ``users[2].externalCustomerId``. More than 10,000 active end users raises ApiError 409.

        Answer (dict): added, kept and reactivated: the number of end users in each.

        Args:
            users: Each a dict with ``external_customer_id`` and an optional ``label`` (at most 80
                characters). The API's names (``externalCustomerId``) are taken too.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        rows: list[Any] = []
        for u in users:
            if not isinstance(u, Mapping):
                rows.append(u)  # sent as given: the API refuses the row with its field
                continue
            ext = u.get("external_customer_id", u.get("externalCustomerId"))
            row: dict[str, Any] = {"externalCustomerId": ext}
            if u.get("label") is not None:
                row["label"] = u["label"]
            rows.append(row)
        return self._call("POST", "/end-users", body={"users": rows}, idempotency_key=idempotency_key)

    def remove_end_users(self, external_customer_ids: Iterable[str], *, idempotency_key: str | None = None) -> Any:
        """Remove approved end users, 1 to 1,000 IDs in one call.

        A removed end user stays on the list with status ``removed``; ``add_end_users`` makes it active
        again. An ID not on the list, or already removed, counts as absent.

        Answer (dict): removed and absent: the number of IDs in each.

        Args:
            external_customer_ids: Your customer IDs.
            idempotency_key: The Idempotency-Key. The same key and body within 24 hours answer the first
                answer again. Default: a new key.
        """
        ids = [external_customer_ids] if isinstance(external_customer_ids, str) else list(external_customer_ids)
        return self._call("POST", "/end-users/remove", body={"externalCustomerIds": ids},
                          idempotency_key=idempotency_key)
