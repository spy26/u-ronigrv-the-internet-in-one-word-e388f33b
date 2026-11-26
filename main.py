#!/usr/bin/env python3
"""Write the one-word entry for make.fun: The Internet in One Word.

The whole entry is a single word. This program checks it against the
competition gate (UTF-8 text, 1-30 characters, not only whitespace,
exactly one word with no spaces or punctuation) and writes it to
$MAKEFUN_OUTPUT_DIR/entry.txt, falling back to /output/entry.txt when
that variable is unset. It then reads the file back and verifies the
bytes on disk are identical to what was written.

Deterministic: no network, no clock, no randomness, no input files.
The word is a constant in this file, so every run produces the same
bytes.
"""

import hashlib
import os
import sys

WORD = "groupchat"
MAX_CHARS = 30


def fail(message):
    """Report a gate failure on stderr and exit non-zero."""
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def check_word(word):
    """Enforce the competition gate on the entry word."""
    if len(word) == 0:
        fail("entry is empty")
    if len(word) > MAX_CHARS:
        fail("entry is %d characters, over the 30-character gate" % len(word))
    if word.strip() == "":
        fail("entry is only whitespace")
    if any(ch.isspace() for ch in word):
        fail("entry must be a single word with no whitespace")
    if not word.isalpha():
        fail("entry must be letters only, a single plain word")
    try:
        word.encode("utf-8")
    except UnicodeEncodeError:
        fail("entry is not valid UTF-8 text")


def resolve_output_path():
    """Return the entry.txt path from the environment, with fallback."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main():
    check_word(WORD)
    data = WORD.encode("utf-8")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("read-back mismatch: wrote %r, read %r" % (data, written))
    if written.decode("utf-8") != WORD:
        fail("read-back text %r is not the entry word" % written.decode("utf-8"))
    digest = hashlib.sha256(written).hexdigest()
    print("wrote %s (%d bytes, %d characters, sha256 %s)"
          % (path, len(data), len(WORD), digest))


if __name__ == "__main__":
    main()
