from collections.abc import Sequence
from typing import Any, Self

__all__ = (
    'EnvCryptedError',
    'EncodingError',
    'EncryptionError',
    'DecodingError',
    'DecryptionError',
)


def _ensure_str_seq(val: Any) -> Sequence[str]:
    if isinstance(val, str):
        return [val.strip()]
    if isinstance(val, Sequence):
        return [str(v).strip() for v in val if str(v).strip()]
    return [str(val).strip()]


class EnvCryptedError(Exception):
    """Base `Exception` class from which all EnvCrypted application errors inherit."""

    def __init__(self: Self, msg: str | list[str] = '', *args: Any) -> None:
        msg = ' '.join(s for s in [*_ensure_str_seq(msg), *_ensure_str_seq(list(args))])
        super().__init__(msg)


class EncodingError(EnvCryptedError):
    """Failed to encode an object."""


class EncryptionError(EnvCryptedError):
    """Failed to encrypt an object."""


class DecodingError(EnvCryptedError):
    """Failed to decode an object."""


class DecryptionError(EnvCryptedError):
    """Failed to decrypt an object."""


class MissingDependencyError(EnvCryptedError, ImportError):
    """Unable to import a required dependency."""

    def __init__(self: Self, pkg_name: str, *args: Any) -> None:
        msg = [
            f"Unable to import required package '{pkg_name}'. ",
            'Please ensure that you are using the correct virtual ',
            'environment and that this package is installed.',
        ]
        super().__init__(msg, *args)
