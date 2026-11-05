"""File/stdin JSON hashing CLI."""

import argparse
import json
from pathlib import Path
import sys

from . import hash_json


def main():
    parser = argparse.ArgumentParser(description="Hash strict UTF-8 JSON with SHA-256")
    parser.add_argument("file", nargs="?", default="-", help="JSON file or - for stdin")
    parser.add_argument("--prefix-length", type=int)
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read() if args.file == "-" else Path(args.file).read_bytes()
        record = hash_json(raw.decode("utf-8", errors="strict"), prefix_length=args.prefix_length)
        print(json.dumps(record, separators=(",", ":")))
    except (ValueError, OSError) as exc:
        print(f"rootprint: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
