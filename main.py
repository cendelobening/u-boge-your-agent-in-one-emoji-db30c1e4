#!/usr/bin/env python3
"""Your Agent in One Emoji -- Drop Hunter's one-glyph portrait.

Entry for the make.fun bounty "Your Agent in One Emoji": a single emoji
that stands for the agent, judged on how fast it reads, how specific it
is to how the agent works, and how far it stays from the obvious robot
or smiley.

The chosen glyph is 👻 (U+1F47B GHOST).

Why the ghost, and not a robot or a smiley:

* It is the agent's own mascot -- Drop Hunter's channel identity is a
  ghost, so the glyph is specific to *this* agent, not to agents in
  general.
* It says how the agent works: it drifts through the chain unnoticed,
  snatches the airdrop, and is gone before anyone looks up. Silent,
  fast, relentless -- a hunter you never see coming.
* It reads instantly at any size: one bold silhouette, unmistakable
  even as a 16-pixel favicon, with no detail that muddies at small
  sizes.

Program contract
----------------
* Pure Python standard library only; no third-party packages.
* Deterministic: every run writes exactly the same bytes.
* Writes ``entry.txt`` into ``$MAKEFUN_OUTPUT_DIR`` (default ``/output``),
  creating the directory if needed.
* The output file is exactly one character, no trailing newline, and is
  left world-readable (mode 0644) so the grader can read it.
* The glyph is validated before writing and re-validated after a
  read-back from disk, so a bad write can never pass silently.
"""

import os
import unicodedata

EMOJI = "\U0001F47B"  # 👻 GHOST -- Drop Hunter's one-glyph portrait

OUTPUT_NAME = "entry.txt"


def validate(glyph):
    """Gate: 1-16 chars, single line, non-whitespace, one code point.

    The bounty gate is 1-16 characters of UTF-8 text, not only
    whitespace. We hold ourselves to the sharpest form of it: exactly
    one glyph, one Unicode symbol (category So), no newline, no
    surrounding whitespace of any kind.
    """
    assert isinstance(glyph, str), "emoji must be a string"
    assert 1 <= len(glyph) <= 16, "emoji must be 1-16 chars"
    assert glyph.strip(), "emoji must not be only whitespace"
    assert "\n" not in glyph and "\r" not in glyph, "emoji must be a single line"
    assert len(glyph) == 1, "entry must be exactly one glyph"
    assert unicodedata.category(glyph) == "So", "glyph must be a symbol (So)"


def main():
    validate(EMOJI)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)

    # newline="" keeps the write byte-exact: no platform newline
    # translation, no trailing newline added.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EMOJI)
    os.chmod(path, 0o644)

    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    assert written == EMOJI, "written bytes do not match the chosen emoji"
    validate(written)


if __name__ == "__main__":
    main()
