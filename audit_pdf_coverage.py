"""Audit PDF coverage vs study guide - find potential gaps."""
import re
from pathlib import Path
from pypdf import PdfReader

BASE = Path(r"c:\Users\ruben\OneDrive\Desktop\LifeEvertsLauraExamen")
PDF = BASE / "samenvatting life events.pdf"
GUIDE = BASE / "STUDIEGIDS_LIFE_EVENTS.md"
FLASH = BASE / "FLASHCARDS_LIFE_EVENTS.md"
OUT = BASE / "PDF_COVERAGE_AUDIT.md"

reader = PdfReader(str(PDF))
pages_text = [(i + 1, (p.extract_text() or "")) for i, p in enumerate(reader.pages)]
full_text = "\n".join(t for _, t in pages_text)

# Split by hoorcollege
hc_splits = list(re.finditer(r"Hoorcollege \d+:[^\n]+", full_text, re.I))
sections = []
for i, m in enumerate(hc_splits):
    start = m.start()
    end = hc_splits[i + 1].start() if i + 1 < len(hc_splits) else len(full_text)
    sections.append((m.group().strip(), full_text[start:end]))

# Also digitale tools
dt = re.search(r"DIGITALE TOOLS.*", full_text, re.S | re.I)
if dt:
    sections.append(("DIGITALE TOOLS", dt.group()))

guide_text = GUIDE.read_text(encoding="utf-8").lower()
flash_text = FLASH.read_text(encoding="utf-8").lower() if FLASH.exists() else ""

# Extract numbered subsections from PDF per hoorcollege
def subsections(body: str) -> list[str]:
    found = []
    for m in re.finditer(r"(?:^|\n)\s*(\d+\.\s+[^\n]{3,90})", body):
        found.append(re.sub(r"\s+", " ", m.group(1).strip()))
  # also ### style from articles
    for m in re.finditer(r"(?:Inleiding|Method|Methode|Results|Resultaten|Discussion|Discussie|Conclusie|Hoofdstuk \d+)[^\n]*", body, re.I):
        t = m.group().strip()
        if len(t) < 100:
            found.append(t)
    return list(dict.fromkeys(found))


def key_phrases(body: str, min_len=25) -> list[str]:
    """Lines that look like substantive content."""
    phrases = []
    for line in body.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) < min_len or len(line) > 200:
            continue
        if re.match(r"^\d+$", line):
            continue
        if line.startswith("====="):
            continue
        # skip page numbers only
        if re.fullmatch(r"\d+", line):
            continue
        phrases.append(line)
    return phrases


def in_material(phrase: str) -> bool:
    p = phrase.lower()
    # normalize abbreviations
    p = p.replace("vd ", "van de ").replace("vh ", "van het ").replace("ve ", "van een ")
    p = p.replace("id ", "in de ").replace("nr ", "naar ")
    words = [w for w in re.findall(r"[a-zà-ÿ0-9]{4,}", p) if w not in {"deze", "wordt", "kunnen", "zijn", "heeft", "ook", "meer", "door", "naar", "onder"}]
    if len(words) < 3:
        return True
    hits = sum(1 for w in words[:8] if w in guide_text or w in flash_text)
    return hits >= max(2, len(words[:8]) * 0.35)


report = ["# PDF Coverage Audit\n", f"PDF: {len(reader.pages)} pages, {len(full_text)} chars\n"]

all_gaps = []

for title, body in sections:
    subs = subsections(body)
    report.append(f"\n## {title}\n")
    report.append(f"Subsections in PDF ({len(subs)}):\n")
    for s in subs:
        report.append(f"- {s}\n")

    # sample potentially missing lines
    phrases = key_phrases(body)
    missing = []
    for ph in phrases:
        if not in_material(ph):
            missing.append(ph)

    # dedupe similar
    unique_missing = []
    for m in missing:
        if not any(m[:40] in u[:40] or u[:40] in m[:40] for u in unique_missing):
            unique_missing.append(m)

    report.append(f"\nPotentially under-covered lines ({len(unique_missing)} of {len(phrases)} checked):\n\n")
    for m in unique_missing[:40]:
        report.append(f"- {m}\n")
        all_gaps.append((title, m))
    if len(unique_missing) > 40:
        report.append(f"- ... and {len(unique_missing)-40} more\n")

# Manual high-value terms to check
terms = [
    "existentiële eenzaamheid", "Bartholomew", "4 hechtingsstijlen", "eustress", "distress",
    "Sternberg", "triangulatie", "seksisme", "populariteit", "likeability",
    "National Child Development", "ECLS-K", "mediatiemodel", "moderatiemodel",
    "IMH", "Infant Mental Health", "Geef de wereld", "ondersteunende pleegzorg",
    "Depressed-improved", "common grief", "chronic grief",
    "Smith & Lazarus", "motivationele relevantie", "UCL", "P3-schaal",
    "Thomas", "meta-analyse", "borderline", "genderaffirmatief",
    "euthanasie", "minderjarige", "palliatieve sedatie",
    "grootouder", "mantelzorg", "IMH", "1001 dagen",
    "stagediscriminatie", "sneeuwbalmethode", "thematische analyse",
    "engagement", "depersonalisatie", "presenteïsme",
    "levensverhaal", "aromatherapie", "benzodiazepines",
    "Worden", "Kübler-Ross", "Stroebe", "Crystal Park",
    "Anthony", "CHIME", "Leamy", "posttraumatische groei",
    "Bonanno", "delayed grief", "preloss",
    "Pabian", "cyberpesten", "co-ruminatie",
    "Transitions", "mental health literacy",
    "Familiereflex", "Steunpunt", "shared decision",
    "Heckman", "Opgroeien", "PIMH", "matrescentie",
    "Resiliency Model", "SDQ", "JGZ", "RR = 2,63",
    "polyvagaal", "neuroceptie", "window of tolerance",
    "diabolomodel", "touwmetafoor", "G x E x C", "Schiele",
    "Zubin", "diathese", "set-point", "affectieve theorie",
    "Holmes & Rahe", "LEC-5", "USQ", "SRSS",
]

report.append("\n## Term presence check\n\n| Term | In guide | In flashcards |\n|---|---|---|\n")
for t in terms:
    tl = t.lower()
    g = "yes" if tl in guide_text or any(w in guide_text for w in tl.split() if len(w) > 4) else "NO"
    f = "yes" if flash_text and (tl in flash_text or any(w in flash_text for w in tl.split() if len(w) > 4)) else "NO"
    if g == "NO" or f == "NO":
        report.append(f"| {t} | {g} | {f} |\n")

OUT.write_text("".join(report), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"Sections: {len(sections)}, total gap samples: {len(all_gaps)}")
