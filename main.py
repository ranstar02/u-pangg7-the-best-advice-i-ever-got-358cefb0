#!/usr/bin/env python3
"""Write one sentence — the best advice I ever got — to /output/entry.txt.

The sentence is fixed and deterministic: no network, no input, no
randomness. Before writing, the program validates the sentence the same
way the competition gate does: UTF-8 text, 1-200 characters, not only
whitespace, and exactly one sentence (a single terminating period).
"""

import os
import sys

# The entry: one sentence about the best advice I ever received.
ENTRY = (
    "My grandfather left school at twelve and still read the paper "
    "every morning, and he told me: never let a bad day convince you "
    "that you have a bad life."
)

MAX_LENGTH = 200


def is_single_sentence(text: str) -> bool:
    """True when the text is exactly one sentence.

    A single sentence here means: it ends with one period, and no
    other sentence-ending punctuation (., !, ?) appears anywhere else
    in the text.
    """
    stripped = text.strip()
    if not stripped.endswith("."):
        return False
    body = stripped[:-1]
    return not any(mark in body for mark in (".", "!", "?"))


def validate(text: str) -> str | None:
    """Return an error message when the text fails validation, else None."""
    if not text or not text.strip():
        return "entry is empty or only whitespace"
    if len(text) > MAX_LENGTH:
        return f"entry is {len(text)} characters, over the 200 limit"
    if any(ord(ch) < 0x20 for ch in text):
        return "entry must not contain newlines or control characters"
    if not is_single_sentence(text):
        return "entry must be exactly one sentence"
    return None


def main() -> int:
    error = validate(ENTRY)
    if error is not None:
        print(f"error: {error}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.txt")

    # Write as UTF-8 with no trailing newline: the gate counts bytes.
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)

    print(f"wrote {len(ENTRY)} characters to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
