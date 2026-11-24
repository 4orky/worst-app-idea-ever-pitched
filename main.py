# The Worst App Idea Ever Pitched — make.fun bounty
# u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23
#
# The program writes one pitch (one sentence, 1-240 characters) to
# /output/entry.txt. Candidates were drafted against the judge's brief,
# in order of weight:
#   1. names a specific app and what it uselessly does, in one sentence
#      pitched as the worst idea imaginable
#   2. makes the uselessness funny through absurd logic, deadpan
#      confidence, or a perfect mismatch between a problem nobody has
#      and the app that solves it
#   3. sounds like a real pitch, with a product name and a clear
#      statement of what the app does and who it is for
#   4. uses the 240 characters well: one clean sentence, no padding,
#      no second idea crowding it
#   5. leaves a vivid, specific picture of the app in the reader's head
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: specific 10, funny 10, real pitch 10, tight 9,
    # vivid 9 = 48. The founder's certainty is the joke: every napkin
    # deserves a Series A, and the VCs never asked for any of it.
    ("Introducing Napkin: an app that photographs your cocktail-napkin "
     "doodles, turns each one into a 40-page investor deck, and emails "
     "it to VCs who never asked, because every napkin deserves a "
     "Series A",
     48),
    # score: specific 10, funny 10, real pitch 9, tight 9,
    # vivid 9 = 47. The app optimises the one thing nobody wants
    # more of: waiting in line, with live updates on the slowness.
    ("Pitch: QueuePal finds the longest queue in your city, reserves "
     "your spot in it, and texts you live updates on how slowly it is "
     "moving, so you never miss a single minute of waiting",
     47),
    # score: specific 10, funny 9, real pitch 9, tight 9,
    # vivid 9 = 46. The AI is confident and wrong on purpose: it
    # reunites you with socks that were never yours.
    ("Meet SockMatch: AI that photographs your single socks, "
     "cross-references two million lost socks worldwide, and "
     "confidently reunites you with socks that were never yours to "
     "begin with",
     46),
    # score: specific 10, funny 9, real pitch 9, tight 8,
    # vivid 9 = 45. The app tells you where you are while you are
    # already there: inside the elevator, waiting to arrive.
    ("Introducing Elevator: an app that tells you which floor the "
     "elevator is on, in real time, from inside the elevator, so you "
     "always know exactly where you are while you wait to arrive",
     45),
    # score: specific 9, funny 9, real pitch 9, tight 8,
    # vivid 9 = 44. A push notification for a cloud that stopped
    # looking like a duck: the alert nobody could ever act on.
    ("Meet CloudWatcher: an app that identifies every cloud above you "
     "by name, tracks the ones that look like animals, and alerts you "
     "the moment a cloud that looked like a duck stops looking like "
     "a duck",
     44),
    # score: specific 9, funny 9, real pitch 9, tight 8,
    # vivid 8 = 43. Sadness-rated leftovers, reported every morning:
    # a daily briefing on food you should have thrown out in 2019.
    ("Pitch: FridgeMirror photographs your leftovers, rates each one "
     "by sadness, and sends a push notification every morning "
     "reminding you the yogurt expired in 2019 and you still have "
     "not thrown it out",
     43),
    # score: specific 9, funny 8, real pitch 9, tight 8,
    # vivid 8 = 42. The thrill of answering your own door, scored
    # out of ten, without ever leaving the couch.
    ("Meet Doorbell: an app that rings your own doorbell from the "
     "couch so you can feel the thrill of answering the door without "
     "getting up, then rates your walk to the door out of ten",
     42),
    # score: specific 9, funny 8, real pitch 8, tight 8,
    # vivid 8 = 41. It charges you monthly to state the obvious one
    # minute too late: the umbrella is at home, and so are you.
    ("Introducing Umbrella: an app that checks the weather, confirms "
     "it is raining, then charges $4.99 a month to remind you that "
     "you left your umbrella at home again, with push notifications",
     41),
]

# The gate requires 1-240 characters of non-whitespace UTF-8 text,
# one sentence.
BANNED_GENERIC_MOVES = ("as an ai language model", "best app ever",
                        "revolutionary")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 240, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        assert text.count(".") <= 2, "candidate must be one sentence"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_GENERIC_MOVES), \
            f"candidate uses a generic move: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def audit_output(line, path="/output/entry.txt"):
    """Second-pass output audit, added after the first draft.

    Re-reads the file the gate will read and checks it three ways
    against values recorded when the winning pitch was drafted:
      * the byte length of the file (197) — a silent edit that adds
        or drops a word changes this;
      * a byte-sum checksum, sum of the UTF-8 bytes mod 9973 (8188) —
        a same-length edit that swaps a word changes this;
      * the file must start with the product intro the winner was
        drafted with ("Introducing Napkin:") and end with its last
        words ("Series A").
    Any mismatch fails loudly instead of shipping a changed pitch.
    """
    with open(path, "rb") as f:
        raw = f.read()
    assert len(raw) == 197, f"entry.txt byte length changed: {len(raw)}"
    assert sum(raw) % 9973 == 8188, \
        f"entry.txt checksum changed: {sum(raw) % 9973}"
    text = raw.decode("utf-8")
    assert text == line, "entry.txt differs from the chosen pitch"
    assert text.startswith("Introducing Napkin:"), \
        "entry.txt lost its product intro"
    assert text.endswith("Series A"), "entry.txt lost its last words"
    assert text == text.strip(), "entry.txt has stray whitespace"


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= 240, "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    audit_output(line)
    print(line)


if __name__ == "__main__":
    main()
