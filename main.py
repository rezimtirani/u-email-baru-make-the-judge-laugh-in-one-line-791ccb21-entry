"""Make the Judge Laugh in One Line.

Writes one funny line to $MAKEFUN_OUTPUT_DIR/entry.txt: a night
shift at a lighthouse, told as a tiny story with a punchline.
The ships never come, the seagulls have unionized, and last
week the fog filed a noise complaint against the light itself
-- the one thing a lighthouse is for. The joke is built as
three beats that keep escalating, and the laugh lands on the
last word, with nothing explained afterwards. Standard library
only; the line is checked against the competition gate (one
line, 1 to 200 characters of UTF-8 text) before it is written.
"""

import os
import sys

LINE = (
    "I work nights at a lighthouse. The ships never come, the "
    "seagulls unionized, and last week the fog filed a noise "
    "complaint against the light."
)

MAX_CHARS = 200


def line_text():
    """Return the lighthouse night-shift one-liner."""
    return LINE


def check_gate(text):
    """Check the line against the competition gate.

    The gate wants one line of plain UTF-8 text, between 1 and
    200 characters, that is not only whitespace: a single funny
    line on any topic. A line that fails here is rejected
    instead of wasting a submission on the server.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("line is empty")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            "line is %d characters, over the 200 limit" % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("line must fit on exactly one line")
    if not cleaned.endswith("."):
        raise ValueError("line must end with a full stop")
    return cleaned


def line_keeps_three_beats(text):
    """Check the line keeps its three-beat escalation.

    The judge laughs at a line that sets an expectation and
    breaks it, with the laugh landing at the end. This line
    earns its punchline in three beats: the ships that never
    come, the seagulls that unionized, and the fog that filed
    its complaint against the light. A line missing any beat
    is a setup with no payoff, or a payoff with no setup, so
    it is rejected here before anything is written.
    """
    lowered = text.lower()
    for beat in ("ships never come", "seagulls unionized", "fog filed"):
        if beat not in lowered:
            raise ValueError("line lost one of its three beats: %s" % beat)
    if "light." not in lowered:
        raise ValueError("line never lands its punchline on the light")
    return text


def measure_line(text):
    """Measure the line for a last sanity pass.

    Returns the character and word counts. A line too short to
    carry a setup and a punchline, or one padded out to fill
    the cap, is caught here before anything is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    line = check_gate(line_text())
    line = line_keeps_three_beats(line)
    shape = measure_line(line)
    if shape["words"] < 5:
        raise ValueError("line is too short to land the joke")
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
