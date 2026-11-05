"""Independent fixture oracle: literal scalar bytes, stdlib framing, OpenSSL SHA.

Prints expectations for inspection; never imports either Rootprint implementation
or rewrites committed vectors. Numeric spellings come from RFC 8785 section 3.2.2.3.
"""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


def sha(preimage):
    data = preimage.encode("utf-8")
    expected = hashlib.sha256(data).hexdigest()
    actual = subprocess.run(
        ["openssl", "dgst", "-sha256", "-binary"], input=data,
        capture_output=True, check=True,
    ).stdout.hex()
    assert actual == expected
    return expected


def vectors():
    scalar_cases = [
        ("null", "null"), ("false", "false"), ("true", "true"),
        ("0", "0"), ("-0", "0"), ('"0"', '"0"'),
        ("1.0", "1"), ("1e0", "1"),
        ("333333333.33333329", "333333333.3333333"),
        ("1E30", "1e+30"), ("4.50", "4.5"), ("2e-3", "0.002"),
        ("1e-27", "1e-27"), ("9007199254740993", "9007199254740992"),
        ("5e-324", "5e-324"), ("1e-400", "0"),
        ('"é"', '"é"'), ('"é"', '"é"'),
        ('"\\n\\t\\u000f\\\\\\\""', '"\\n\\t\\u000f\\\\\\\""'),
    ]
    result = []
    for source, canonical in scalar_cases:
        preimage = '["rootprint-v1","value",' + canonical + ']'
        result.append({"json": source, "preimage": preimage, "digest": sha(preimage)})

    def add(source, tag, children):
        preimage = json.dumps(["rootprint-v1", tag, children], ensure_ascii=False, separators=(",", ":"))
        result.append({"json": source, "preimage": preimage, "digest": sha(preimage)})
        return result[-1]["digest"]

    one = result[6]["digest"]
    two = sha('["rootprint-v1","value",2]')
    add("[]", "array", [])
    add("{}", "object", [])
    add("[1,2]", "array", [one, two])
    add("[2,1]", "array", [two, one])
    pairs = [["a", one], ["b", two]]
    add('{"b":2,"a":1}', "object", pairs)
    add('{"a":1,"b":2}', "object", pairs)
    # U+1F600 sorts before U+E000 in UTF-16, unlike scalar-value/UTF-8 order.
    add('{"\ue000":2,"😀":1}', "object", [["😀", one], ["\ue000", two]])
    array_digest = add('[1,{"a":1,"b":2}]', "array", [one, result[-3]["digest"]])
    add('{"nested":[1,{"b":2,"a":1}]}', "object", [["nested", array_digest]])
    return result


if __name__ == "__main__":
    expected = vectors()
    if "--check" in sys.argv:
        committed = json.loads((Path(__file__).resolve().parents[1] / "conformance/v1/vectors.json").read_text(encoding="utf-8"))
        assert committed["valid"] == expected
        custom_preimages = ['["rootprint-v1","value",1]', '["rootprint-v1","value",2]']
        children = [f"{sum(p.encode('utf-8')) % 256:02x}" for p in custom_preimages]
        custom_preimages.append(json.dumps(["rootprint-v1", "array", children], separators=(",", ":")))
        assert committed["custom"]["preimages"] == custom_preimages
        assert committed["custom"]["digest"] == f"{sum(custom_preimages[-1].encode('utf-8')) % 256:02x}"
        print(f"Verified {len(expected)} committed vectors against literal preimages and OpenSSL")
        print("Verified sum8 preimages and digest against independent byte sums")
    else:
        print(json.dumps(expected, ensure_ascii=False, indent=2))
