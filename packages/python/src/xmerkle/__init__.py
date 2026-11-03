"""Deterministic JSON Merkle hashing. See docs/protocol.md for the byte contract."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import re

import rfc8785

PROTOCOL = "xmerkle-v1"


class InputError(ValueError):
    """Input is not supported JSON or record metadata is invalid."""


class AlgorithmError(ValueError):
    """Hash provider configuration or output is invalid."""


@dataclass(frozen=True)
class HashProvider:
    algorithm: str
    digest_length: int
    hash: Callable[[bytes], bytes]


SHA256 = HashProvider("sha256", 32, lambda data: hashlib.sha256(data).digest())


def _string(value):
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise InputError("Unpaired Unicode surrogate") from exc


def parse_json(text: str):
    """Parse strict text without discarding duplicate decoded member names."""
    if type(text) is not str:
        raise InputError("JSON text must be a string")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InputError("Duplicate object key")
            result[key] = value
        return result

    def invalid_constant(_):
        raise InputError("Non-JSON number")

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_int=float,
                          parse_float=float, parse_constant=invalid_constant)
    except (ValueError, RecursionError) as exc:
        raise InputError("Invalid JSON or unsupported nesting") from exc


def digest(value, provider: HashProvider = SHA256) -> str:
    """Compute a full lowercase hex root digest, without clock metadata."""
    if (not isinstance(provider, HashProvider)
            or type(provider.algorithm) is not str
            or not re.fullmatch(r"[a-z0-9]+", provider.algorithm)
            or type(provider.digest_length) is not int or provider.digest_length < 1
            or not callable(provider.hash)):
        raise AlgorithmError("Invalid hash provider")
    ancestors = set()

    def node(item, depth):
        if depth > 256:
            raise InputError("JSON nesting exceeds supported depth")
        kind = type(item)
        if item is None or kind is bool or kind is str:
            if kind is str:
                _string(item)
            representation = [PROTOCOL, "value", item]
        elif kind in (int, float):
            try:
                number = float(item)
            except OverflowError as exc:
                raise InputError("Number exceeds finite binary64") from exc
            if not math.isfinite(number):
                raise InputError("Number must be finite binary64")
            representation = [PROTOCOL, "value", number]
        elif kind in (list, dict):
            identity = id(item)
            if identity in ancestors:
                raise InputError("Cyclic input")
            ancestors.add(identity)
            try:
                if kind is list:
                    representation = [PROTOCOL, "array", [node(v, depth + 1) for v in item]]
                else:
                    for key in item:
                        if type(key) is not str:
                            raise InputError("Object keys must be strings")
                        _string(key)
                    keys = sorted(item, key=lambda key: key.encode("utf-16-be"))
                    representation = [PROTOCOL, "object", [[k, node(item[k], depth + 1)] for k in keys]]
            finally:
                ancestors.remove(identity)
        else:
            raise InputError("Unsupported non-JSON value")
        preimage = rfc8785.dumps(representation)
        try:
            output = provider.hash(preimage)
        except Exception as exc:
            raise AlgorithmError("Hash provider failed") from exc
        if type(output) is not bytes or len(output) != provider.digest_length:
            raise AlgorithmError("Hash provider returned invalid bytes or digest length")
        return output.hex()

    return node(value, 0)


def hash_value(value, *, provider: HashProvider = SHA256, prefix_length: int | None = None,
               clock: Callable[[], datetime] | None = None) -> dict:
    """Return deterministic identity and a UTC root-completion display label."""
    full = digest(value, provider)
    length = min(16, len(full)) if prefix_length is None else prefix_length
    if type(length) is not int or not 1 <= length <= len(full):
        raise InputError("Invalid prefix length")
    now = clock() if clock is not None else datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise InputError("Clock must return a timezone-aware datetime")
    try:
        now = now.astimezone(timezone.utc).replace(microsecond=0)
    except (OverflowError, ValueError) as exc:
        raise InputError("Clock must be a UTC instant in years 0001–9999") from exc
    date = f"{now.year:04d}{now.month:02d}{now.day:02d}"
    time = f"{now.hour:02d}{now.minute:02d}{now.second:02d}"
    return {
        "protocol": PROTOCOL,
        "algorithm": provider.algorithm,
        "digest": full,
        "calculatedAt": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "label": f"{date}_{time}-{provider.algorithm}-{full[:length]}",
    }


def hash_json(text: str, **options) -> dict:
    """Hash strict JSON text, detecting duplicates before they can be lost."""
    return hash_value(parse_json(text), **options)
