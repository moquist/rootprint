# Xmerkle for Python

Requires Python 3.11+. Every Merkle node uses RFC 8785 canonical bytes.

```python
from xmerkle import digest, hash_json, hash_value

record = hash_value({"b": 2, "a": 1})
print(record["label"])   # UTC calculation label with a 16-hex prefix
print(record["digest"])  # full deterministic root digest
assert hash_json('{"a":1,"b":2}')["digest"] == record["digest"]
assert digest({"a": 1, "b": 2}) == record["digest"]
```

Custom provider:

```python
import hashlib
from xmerkle import HashProvider, hash_value

provider = HashProvider("sha512", 64, lambda data: hashlib.sha512(data).digest())
print(hash_value([1, 2], provider=provider, prefix_length=24))
```

`hash_value`/`hash_json` accept `clock` returning a timezone-aware `datetime` for
reproducibility. `digest` returns full root hex. `parse_json` rejects duplicate
keys; ordinary `json.loads` cannot recover duplicates already discarded.
`InputError` and `AlgorithmError` subclass `ValueError`.

CLI after installation: `xmerkle [--prefix-length N] [FILE|-]`, also available
through `python -m xmerkle`. Defaults to stdin/SHA-256; emits one JSON record.

Numbers (including Python integers) normalize to finite binary64, so large
integers can round. Encode exact arbitrary-precision data as strings. Only native
`None`, `bool`, `int`, `float`, `str`, `list`, and string-keyed `dict` are supported;
subclasses and custom serializers are not used. Arrays retain order and object
keys sort by unsigned UTF-16 units. Strings are not normalized. Nesting is limited
to 256 container edges. Full identity is protocol + algorithm + full digest;
labels may collide and are not identity or authenticated time.
This package is not yet published; project license selection is pending.
