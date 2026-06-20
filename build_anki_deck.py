"""Build Anki .apkg from FLASHCARDS_LIFE_EVENTS.md"""
import hashlib
import re
import genanki

FLASHCARDS_PATH = r"c:\Users\ruben\OneDrive\Desktop\LifeEvertsLauraExamen\FLASHCARDS_LIFE_EVENTS.md"
OUTPUT_PATH = r"c:\Users\ruben\OneDrive\Desktop\LifeEvertsLauraExamen\Life_Events_Examen.apkg"

DECK_ID = 2059400110
MODEL_ID = 1607392319

model = genanki.Model(
    MODEL_ID,
    "Life Events Basic",
    fields=[
        {"name": "Front"},
        {"name": "Back"},
        {"name": "Section"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<div class="section">{{Section}}</div>{{Front}}',
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
        }
    ],
    css="""
.card { font-family: arial; font-size: 18px; text-align: left; color: black; background-color: white; }
.section { font-size: 12px; color: #666; margin-bottom: 12px; }
""",
)

deck = genanki.Deck(DECK_ID, "Life Events Examen")

section_pattern = re.compile(r"^## (.+)$")
q_pattern = re.compile(r"^\*\*Q:\*\* (.+)$")
a_pattern = re.compile(r"^\*\*A:\*\* (.+)$")

current_section = "Algemeen"
notes = []

with open(FLASHCARDS_PATH, encoding="utf-8") as f:
    pending_q = None
    for line in f:
        line = line.rstrip("\n")
        m_sec = section_pattern.match(line)
        if m_sec:
            current_section = m_sec.group(1).strip()
            continue
        m_q = q_pattern.match(line)
        if m_q:
            pending_q = m_q.group(1).strip()
            continue
        m_a = a_pattern.match(line)
        if m_a and pending_q:
            answer = m_a.group(1).strip()
            # Subdeck name from section
            subdeck = current_section
            if subdeck.startswith("Hoorcollege"):
                deck_name = f"Life Events Examen::{subdeck}"
            elif subdeck == "Digitale Tools (snel)":
                deck_name = "Life Events Examen::Digitale Tools"
            elif subdeck == "Gemengde examenvragen":
                deck_name = "Life Events Examen::Gemengde examenvragen"
            else:
                deck_name = f"Life Events Examen::{subdeck}"

            tag = re.sub(r"[^\w]", "_", subdeck.lower())[:30]
            note = genanki.Note(
                model=model,
                fields=[pending_q, answer, subdeck],
                tags=["life_events", tag],
            )
            note.guid = genanki.guid_for(pending_q, answer, subdeck)
            notes.append((deck_name, note))
            pending_q = None

def stable_id(text: str) -> int:
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


# Group notes into subdecks
decks = {}
for deck_name, note in notes:
    if deck_name not in decks:
        d = genanki.Deck(stable_id(deck_name), deck_name)
        d.add_model(model)
        decks[deck_name] = {"deck": d, "count": 0}
    decks[deck_name]["deck"].add_note(note)
    decks[deck_name]["count"] += 1

package = genanki.Package([d["deck"] for d in decks.values()])
package.write_to_file(OUTPUT_PATH)

print(f"Created: {OUTPUT_PATH}")
print(f"Total cards: {len(notes)}")
for name in sorted(decks):
    print(f"  - {name}: {decks[name]['count']} cards")
