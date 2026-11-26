# Napkin, and the noble art of pitching an app nobody needs.
# Written for the make.fun bounty "The Worst App Idea Ever Pitched",
# slug u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23.
# The job: dream up a dozen one-sentence pitches for gloriously
# useless apps, grade every one against the five yardsticks the
# judge publishes, keep the strongest draft, and write it out to
# /output/entry.txt. The yardsticks, heaviest first, run like this:
# name one precise app and the pointless job it does; make that
# pointlessness funny through straight-faced absurdity; read like a
# genuine founder pitch, with a name and an audience; spend the 240
# characters on exactly one clean idea; and leave the reader with a
# picture they can actually see. Nothing in this file reaches for the
# network or for privileges it does not already have: it only invents
# sentences, scores them, writes one file, and then reads that file
# back to prove nothing drifted between the choosing and the writing.
from pathlib import Path as _Path
import sys as _sys
# Every draft carries five marks out of ten, in the order the judge
# weighs them: precise, funny, pitch-like, tight, vivid. The marks
# add up to a total, and the draft with the biggest total wins; when
# two drafts tie on total, the shorter sentence takes the prize.
DRAFTS = [
    ("Introducing Napkin: an app that photographs your cocktail-napkin doodles, turns each one into a 40-page investor deck, and emails it to VCs who never asked, because every napkin deserves a Series A", (10, 10, 10, 9, 9)),
    ("Meet SnoozeBank: an app that saves the sleep you skip on weekdays into a savings account you can only withdraw as naps during meetings, because rest should compound like interest", (9, 9, 9, 9, 8)),
    ("Introducing PlantTherapist: an app that listens to your houseplants complain about your watering schedule and books them weekly therapy sessions you pay for in sunlight", (9, 9, 8, 9, 9)),
    ("Meet FridgeDJ: an app that turns the hum of your refrigerator into a live DJ set and charges your guests a cover fee every time they open the door for a snack", (9, 8, 9, 8, 9)),
    ("Meet PetTranslator: an app that translates your goldfish's bubbles into daily horoscopes and sells premium subscriptions to fish who want their fortune told twice", (9, 9, 8, 8, 9)),
    ("Introducing MeetingMeter: an app that measures how much of your life meetings consume, converts the total into a loyalty card, and rewards your tenth wasted hour with a free meeting", (9, 9, 9, 8, 8)),
    ("Introducing UmbrellaShare: an app that lets strangers rent your umbrella by the minute during rainstorms, then fines you when they return it slightly damp", (8, 9, 9, 8, 8)),
    ("Meet QueueSkipper: an app that pays strangers to stand in line for you, then charges you extra to watch them enjoy the concert from your seat", (8, 8, 9, 9, 8)),
    ("Meet CloudShelf: an app that photographs clouds, files them into folders by shape, and sends you a monthly bill for the sky you have already used", (9, 8, 8, 9, 8)),
    ("Introducing NapReminder: an app that wakes you up from naps you never took to remind you that you forgot to schedule the nap you just missed", (8, 9, 8, 8, 9)),
    ("Meet ElevatorCast: an app that records your elevator rides and turns the awkward silence into a podcast nobody subscribes to, sponsored by the elevator itself", (8, 8, 8, 9, 9)),
    ("Introducing LeftSock: an app that tracks your left socks with GPS, alerts you the moment one goes missing, and sells the location data to your right socks", (9, 8, 8, 8, 8))]
# A draft only earns its marks when it obeys the gate the house
# publishes: real words rather than blank space, between 1 and 240
# characters long, a single line, and a single sentence with no
# full stop, bang, or question mark hiding a second thought inside.
def _passes_gate(sentence):
    trimmed = sentence.strip()
    if trimmed != sentence or not trimmed:
        return False
    if len(sentence) < 1 or len(sentence) > 240:
        return False
    if "\n" in sentence or "\r" in sentence or "\t" in sentence:
        return False
    if "." in sentence or "!" in sentence or "?" in sentence:
        return False
    return True
def _add_up(marks):
    running = 0
    for mark in marks:
        running = running + mark
    return running
def _crown(drafts):
    champion = None
    champion_key = None
    for sentence, marks in drafts:
        if not _passes_gate(sentence):
            raise ValueError("draft breaks the gate: " + sentence)
        for mark in marks:
            if mark < 0 or mark > 10:
                raise ValueError("mark outside 0-10: " + sentence)
        key = (_add_up(marks), -len(sentence))
        if champion_key is None or key > champion_key:
            champion_key = key
            champion = sentence
    return champion
# Second pass, written after the first draft of this file: instead of
# trusting the string held in memory, open the file the gate will
# read and check it from scratch. It must hold exactly the sentence
# that won, 197 bytes long, with its bytes adding to a remainder of
# 8188 when divided by 9973, 32 words, no stray spaces, and the same
# opening and closing words the winner was drafted with. Anything
# else fails loudly instead of shipping a drifted pitch.
def _second_pass(path, expected):
    payload = path.read_bytes()
    if len(payload) != 197:
        raise ValueError("entry.txt is not 197 bytes long")
    remainder = 0
    for byte in payload:
        remainder = (remainder + byte) % 9973
    if remainder != 8188:
        raise ValueError("entry.txt checksum drifted")
    decoded = payload.decode("utf-8")
    if decoded != expected:
        raise ValueError("entry.txt is not the winning sentence")
    if decoded != decoded.strip() or "  " in decoded:
        raise ValueError("entry.txt has stray whitespace")
    if len(decoded.split()) != 32:
        raise ValueError("entry.txt word count drifted")
    if not decoded.startswith("Introducing Napkin:"):
        raise ValueError("entry.txt lost its opening words")
    if not decoded.endswith("Series A"):
        raise ValueError("entry.txt lost its closing words")
    return decoded
def _run():
    winner = _crown(DRAFTS)
    target = _Path("/output/entry.txt")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(winner, encoding="utf-8")
    target.chmod(0o644)
    checked = _second_pass(target, winner)
    _sys.stdout.write(checked + "\n")
_run()
