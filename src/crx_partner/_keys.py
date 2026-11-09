"""The API key: an Ed25519 key pair. The private key stays in a PKCS#8 PEM file on the caller's side."""

from __future__ import annotations

import base64
import os
import stat
import sys
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .errors import ConfigError

OPEN_TO_OTHERS = "the key file is open to other users; run chmod 600 on it"


def public_key_b64(key: Ed25519PrivateKey) -> str:
    """Return the public key as base64 of its 32 raw bytes, the form the console takes."""
    raw = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def pem_of(key: Ed25519PrivateKey) -> bytes:
    """Return the private key as a PKCS#8 PEM, the form the console's browser key pair saves."""
    return key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                             serialization.NoEncryption())


def make_key_file(path: str | os.PathLike) -> str:
    """Write a new key pair's private key to ``path`` (mode 0600, never over an existing file).
    Return the public key, base64 of its 32 raw bytes."""
    key = Ed25519PrivateKey.generate()
    p = Path(path).expanduser()
    try:
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o600)
    except FileExistsError:
        raise ConfigError(f"{os.fspath(path)} exists; choose another path") from None
    except OSError as e:
        raise ConfigError(f"{os.fspath(path)} cannot be written ({e.strerror})") from None
    with os.fdopen(fd, "wb") as f:
        f.write(pem_of(key))
    return public_key_b64(key)


def owner_only(fd: int, st: os.stat_result, path: os.PathLike | str) -> bool:
    """Make the open file ``fd`` (``st`` is its fstat) owner-only. True when it is owner-only now.

    POSIX only. A regular file that group or other users can open is set to 0600 when the current user
    owns it, and one line goes to stderr. False when another user owns it, when it is no regular file, or
    when its mode does not change.
    """
    if os.name != "posix" or not st.st_mode & (stat.S_IRWXG | stat.S_IRWXO):
        return True
    if st.st_uid != os.getuid() or not stat.S_ISREG(st.st_mode):
        return False
    done = False
    try:
        os.fchmod(fd, 0o600)
        done = not os.fstat(fd).st_mode & (stat.S_IRWXG | stat.S_IRWXO)
    except OSError:
        pass
    if done:
        print(f"set {os.fspath(path)} to owner-only (0600)", file=sys.stderr)
    return done


def load_key_file(path: str | os.PathLike) -> Ed25519PrivateKey:
    """Read the Ed25519 private key from a PKCS#8 PEM file. The mode check and the read use one open file."""
    p = Path(path).expanduser()
    try:
        fd = os.open(p, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_BINARY", 0))
    except OSError:
        fd = None
    if fd is None:
        raise ConfigError("the key file cannot be read")
    data = None
    private = None
    try:
        private = owner_only(fd, os.fstat(fd), p)
        if private:
            with os.fdopen(fd, "rb", closefd=False) as f:
                data = f.read(16_384)
    except OSError:
        pass
    finally:
        os.close(fd)
    if private is False:
        raise ConfigError(OPEN_TO_OTHERS)
    if data is None:
        raise ConfigError("the key file cannot be read")
    key = None
    try:
        key = serialization.load_pem_private_key(data, password=None)
    except Exception:  # noqa: BLE001 - the original exception can quote the file; it is dropped
        pass
    data = None
    if not isinstance(key, Ed25519PrivateKey):
        raise ConfigError("the key file holds no Ed25519 private key in PKCS#8 PEM form")
    return key
