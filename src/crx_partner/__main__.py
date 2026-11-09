"""Command line: ``python -m crx_partner keygen --out partner.key`` and ``python -m crx_partner me``."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from ._keys import make_key_file
from .client import Manage
from .errors import ApiError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m crx_partner", description=f"CRX Partner SDK {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    keygen = sub.add_parser("keygen", help="make a key pair; print the public key")
    keygen.add_argument("--out", required=True, help="the private key file to write (PKCS#8 PEM, mode 0600)")
    me = sub.add_parser("me", help="read the caller with the key in CRX_PARTNER_KEY_ID and CRX_PARTNER_KEY_FILE")
    me.add_argument("--realm", choices=("manage",), default="manage", help="the API: manage")
    me.add_argument("--base-url", default=None, help="the API base; default CRX_PARTNER_BASE_URL or production")
    args = parser.parse_args(argv)
    try:
        if args.command == "keygen":
            public_key = make_key_file(args.out)
            print(f"Private key written to {args.out}. Paste this public key under API keys: Create a key, Paste a public key.", file=sys.stderr)
            print(public_key)
            return 0
        client = Manage(base_url=args.base_url)
        print(json.dumps(client.me(), indent=2))
        return 0
    except ApiError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
