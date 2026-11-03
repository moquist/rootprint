from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import unittest

from xmerkle import AlgorithmError, HashProvider, InputError, SHA256, digest, hash_json, hash_value

VECTORS = json.loads((Path(__file__).resolve().parents[3] / "conformance/v1/vectors.json").read_text(encoding="utf-8"))
INSTANT = datetime(2026, 11, 2, 9, 4, 5, 987000, tzinfo=timezone.utc)


class Conformance(unittest.TestCase):
    def test_shared_vectors(self):
        for vector in VECTORS["valid"]:
            with self.subTest(source=vector["json"]):
                calls = []

                def capture(data):
                    calls.append(data.decode("utf-8"))
                    return SHA256.hash(data)

                record = hash_json(vector["json"], provider=HashProvider("sha256", 32, capture), clock=lambda: INSTANT)
                self.assertEqual(record["digest"], vector["digest"])
                self.assertEqual(calls[-1], vector["preimage"])
        for source in VECTORS["invalid"]:
            with self.subTest(source=source), self.assertRaises(InputError):
                hash_json(source)

    def test_native_validation_and_no_mutation(self):
        cycle = []
        cycle.append(cycle)
        for value in [float("inf"), float("nan"), 10**10000, {1: "x"}, set(), (1, 2),
                      object(), b"x", "\ud800", {"\udfff": 1}, cycle]:
            with self.subTest(kind=type(value)), self.assertRaises(InputError):
                digest(value)
        child = {"b": 2, "a": 1}
        self.assertEqual(digest([child, child]), digest([{"a": 1, "b": 2}] * 2))
        self.assertEqual(list(child), ["b", "a"])
        self.assertNotEqual(digest(False), digest(0))
        self.assertEqual(digest(9007199254740993), hash_json("9007199254740993")["digest"])
        deep = None
        for _ in range(257):
            deep = [deep]
        with self.assertRaises(InputError):
            digest(deep)

    def test_custom_providers(self):
        calls = []

        def sum8(data):
            calls.append(data.decode("utf-8"))
            return bytes([sum(data) % 256])

        record = hash_json(VECTORS["custom"]["json"], provider=HashProvider("sum8", 1, sum8), clock=lambda: INSTANT)
        self.assertEqual(record["digest"], VECTORS["custom"]["digest"])
        self.assertEqual(record["label"], "20261102_090405-sum8-18")
        self.assertEqual(calls, VECTORS["custom"]["preimages"])
        self.assertEqual(len(digest(None, HashProvider("sha512", 64, lambda b: hashlib.sha512(b).digest()))), 128)
        for provider in [HashProvider("sha-256", 1, sum8), HashProvider("ok", 0, sum8),
                         HashProvider("ok", True, sum8), HashProvider("ok", 1, lambda _: "aa"),
                         HashProvider("ok", 1, lambda _: b""), HashProvider("ok", 1, lambda _: b"aa")]:
            with self.assertRaises(AlgorithmError):
                digest(None, provider)

        def broken(_):
            raise RuntimeError("provider failed")

        with self.assertRaises(AlgorithmError):
            digest(None, HashProvider("broken", 1, broken))

    def test_records(self):
        fixed = HashProvider("fixed", 16, lambda _: bytes.fromhex("0123456789abcdef0123456789abcdef"))
        record = hash_value(None, provider=fixed, clock=lambda: INSTANT)
        self.assertEqual(record["label"], "20261102_090405-fixed-0123456789abcdef")
        self.assertEqual(record["calculatedAt"], "2026-11-02T09:04:05Z")
        local = INSTANT.astimezone(timezone(timedelta(hours=-7)))
        self.assertEqual(record, hash_value(None, provider=fixed, clock=lambda: local))
        self.assertEqual(len(hash_value(None, provider=fixed, prefix_length=24)["label"].split("-")[-1]), 24)
        for length in [0, -1, 1.5, 65, True, float("nan")]:
            with self.assertRaises(InputError):
                hash_value(None, prefix_length=length)
        for clock in [lambda: datetime(2026, 1, 1), lambda: None]:
            with self.assertRaises(InputError):
                hash_value(None, clock=clock)
        early = hash_value(None, clock=lambda: datetime(1, 1, 1, tzinfo=timezone.utc))
        self.assertEqual(early["calculatedAt"], "0001-01-01T00:00:00Z")
        later = hash_value(None, provider=fixed, clock=lambda: INSTANT + timedelta(seconds=1))
        self.assertLess(record["label"], later["label"])
        other = HashProvider("fixed", 16, lambda _: bytes.fromhex("0123456789abcdef1123456789abcdef"))
        collision = hash_value(None, provider=other, clock=lambda: INSTANT)
        self.assertEqual(record["label"], collision["label"])
        self.assertNotEqual(record["digest"], collision["digest"])


if __name__ == "__main__":
    unittest.main()
