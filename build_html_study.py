"""Generate self-contained Life Events study HTML page."""
import hashlib
import json
import re
from pathlib import Path

from exam_questions_data import EXAM_SECTION_RECON, all_exam_questions
from mindmaps_data import MINDMAPS

try:
    import markdown
    from markdown.extensions.tables import TableExtension
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "markdown", "-q"])
    import markdown
    from markdown.extensions.tables import TableExtension

BASE = Path(r"c:\Users\ruben\OneDrive\Desktop\LifeEvertsLauraExamen")
GUIDE_PATH = BASE / "STUDIEGIDS_LIFE_EVENTS.md"
FLASHCARDS_PATH = BASE / "FLASHCARDS_LIFE_EVENTS.md"
OUTPUT_PATH = BASE / "life_events_study.html"
INDEX_OUTPUT_PATH = BASE / "index.html"


def parse_flashcards(path: Path) -> list[dict]:
    section_re = re.compile(r"^## (.+)$")
    q_re = re.compile(r"^\*\*Q:\*\* (.+)$")
    a_re = re.compile(r"^\*\*A:\*\* (.+)$")
    cards = []
    section = "Algemeen"
    pending_q = None
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if m := section_re.match(line):
                section = m.group(1).strip()
                continue
            if m := q_re.match(line):
                pending_q = m.group(1).strip()
                continue
            if m := a_re.match(line):
                if pending_q:
                    cid = hashlib.md5(f"{section}|{pending_q}".encode()).hexdigest()[:12]
                    cards.append({
                        "id": cid,
                        "section": section,
                        "q": pending_q,
                        "a": m.group(1).strip(),
                    })
                    pending_q = None
    return cards


def add_heading_ids(html: str) -> str:
    def slugify(title: str) -> str:
        title = re.sub(r"<[^>]+>", "", title)
        title = title.replace("&amp;", "and").lower()
        title = re.sub(r"[^a-z0-9\s-]", "", title)
        return re.sub(r"\s+", "-", title.strip())

    def repl(m: re.Match) -> str:
        inner = m.group(1)
        sid = slugify(inner)
        return f'<h2 id="{sid}">{inner}</h2>'

    return re.sub(r"<h2>(.*?)</h2>", repl, html)


def md_to_html(text: str) -> str:
    # Split off checklist for custom rendering
    parts = text.split("## Snelle examenchecklist")
    main_md = parts[0]
    checklist_md = parts[1] if len(parts) > 1 else ""

    html = markdown.markdown(
        main_md,
        extensions=[TableExtension(), "nl2br", "sane_lists"],
    )
    html = add_heading_ids(html)

    checklist_items = []
    if checklist_md:
        for line in checklist_md.splitlines():
            m = re.match(r"^- \[ \] (.+)$", line.strip())
            if m:
                checklist_items.append(m.group(1))

    return html, checklist_items


def section_slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def build_exam_sections(questions: list[dict]) -> list[str]:
    sections = sorted({q["section"] for q in questions})
    if EXAM_SECTION_RECON in sections:
        sections.remove(EXAM_SECTION_RECON)
        sections.insert(0, EXAM_SECTION_RECON)
    return sections


def build_section_nav() -> list[dict]:
    return [
        {"id": "hc1", "label": "HC1: Inleiding", "anchor": "1-hoorcollege-1-inleiding"},
        {"id": "hc2", "label": "HC2: Ouderschap", "anchor": "2-hoorcollege-2-ouderschap"},
        {"id": "hc3", "label": "HC3: Relaties", "anchor": "3-hoorcollege-3-relaties"},
        {"id": "hc4", "label": "HC4: School & Werk", "anchor": "4-hoorcollege-4-school-and-werk"},
        {"id": "hc5", "label": "HC5: Verlies", "anchor": "5-hoorcollege-5-verlies"},
        {"id": "hc6", "label": "HC6: Omgaan met LE", "anchor": "6-hoorcollege-6-omgaan-met-life-events"},
        {"id": "tools", "label": "Digitale Tools", "anchor": "7-digitale-tools"},
    ]


def build_mindmap_sidebar() -> str:
    groups: dict[str, list] = {}
    for m in MINDMAPS:
        groups.setdefault(m["group"], []).append(m)
    parts = []
    for group, items in groups.items():
        parts.append(f'<div class="mm-group-label">{group}</div>')
        for m in items:
            parts.append(
                f'<button type="button" class="filter-btn mm-nav-btn" data-mm-id="{m["id"]}">'
                f'{m["title"]}</button>'
            )
    return "".join(parts)


def build_mindmap_panels() -> str:
    parts = []
    for m in MINDMAPS:
        parts.append(
            f'<div class="mm-panel" id="mm-{m["id"]}" data-mm-id="{m["id"]}" style="display:none">'
            f'<h2>{m["title"]}</h2>'
            f'<p class="mm-subtitle">{m["subtitle"]}</p>'
            f'<div class="mm-diagram-wrap"><pre class="mermaid mm-source">{m["diagram"]}</pre></div>'
            f"</div>"
        )
    return "".join(parts)


guide_text = GUIDE_PATH.read_text(encoding="utf-8")
guide_html, checklist = md_to_html(guide_text)
cards = parse_flashcards(FLASHCARDS_PATH)
sections = sorted({c["section"] for c in cards})
nav = build_section_nav()
mc_questions = all_exam_questions()
exam_sections = build_exam_sections(mc_questions)

html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>
    (function() {{
      try {{
        var t = localStorage.getItem('life_events_theme');
        if (!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        if (t === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
      }} catch (e) {{}}
    }})();
  </script>
  <title>Life Events — Studiegids & Flashcards</title>
  <style>
    :root {{
      --bg: #f4f6f9;
      --surface: #ffffff;
      --text: #1a2332;
      --muted: #5c6b7a;
      --accent: #2563eb;
      --accent-soft: #dbeafe;
      --border: #e2e8f0;
      --success: #059669;
      --warning: #d97706;
      --danger: #b91c1c;
      --danger-soft: #fef2f2;
      --danger-border: #fca5a5;
      --success-soft: #ecfdf5;
      --error: #ef4444;
      --confirm: #0d9488;
      --strong: #0f172a;
      --header-bg: rgba(255, 255, 255, 0.92);
      --shadow: 0 4px 24px rgba(15, 23, 42, 0.08);
      --tab-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
      --on-accent: #ffffff;
      --toast-bg: #0f172a;
      --toast-fg: #ffffff;
      --weak-bg: #fff7ed;
      --weak-border: #fed7aa;
      --weak-title: #9a3412;
      --weak-text: #7c2d12;
      --weak-item-bg: #ffffff;
      --weak-item-border: #fdba74;
      --weak-item-hover: #ea580c;
      --weak-badge-bg: #ffedd5;
      --weak-badge-fg: #c2410c;
      --fc-back-bg: #f8fafc;
      --radius: 12px;
      --sidebar-w: 260px;
    }}
    [data-theme="dark"] {{
      color-scheme: dark;
      --bg: #0f1419;
      --surface: #1a2332;
      --text: #e8edf4;
      --muted: #94a3b8;
      --accent: #3b82f6;
      --accent-soft: #1e3a5f;
      --border: #2d3a4d;
      --success: #34d399;
      --warning: #fbbf24;
      --danger: #f87171;
      --danger-soft: #3f1d1d;
      --danger-border: #7f1d1d;
      --success-soft: #064e3b;
      --error: #f87171;
      --confirm: #2dd4bf;
      --strong: #f1f5f9;
      --header-bg: rgba(26, 35, 50, 0.92);
      --shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
      --tab-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
      --toast-bg: #334155;
      --toast-fg: #f8fafc;
      --weak-bg: #2a1f14;
      --weak-border: #7c4a1a;
      --weak-title: #fdba74;
      --weak-text: #fcd9b8;
      --weak-item-bg: #1a2332;
      --weak-item-border: #9a3412;
      --weak-item-hover: #ea580c;
      --weak-badge-bg: #431407;
      --weak-badge-fg: #fdba74;
      --fc-back-bg: #151d2b;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }}
    .app-header {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--header-bg);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border);
      padding: 0.75rem 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
    }}
    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }}
    .theme-toggle {{
      border: 1px solid var(--border);
      background: var(--surface);
      border-radius: 999px;
      width: 2.35rem;
      height: 2.35rem;
      cursor: pointer;
      font-size: 1.05rem;
      line-height: 1;
      flex-shrink: 0;
    }}
    .app-header h1 {{
      margin: 0;
      font-size: 1.15rem;
      font-weight: 700;
    }}
    .tabs {{
      display: flex;
      gap: 0.35rem;
      background: var(--bg);
      padding: 0.25rem;
      border-radius: 999px;
      border: 1px solid var(--border);
    }}
    .tab {{
      border: none;
      background: transparent;
      padding: 0.45rem 1rem;
      border-radius: 999px;
      cursor: pointer;
      font-size: 0.9rem;
      color: var(--muted);
      font-weight: 600;
    }}
    .tab.active {{
      background: var(--surface);
      color: var(--accent);
      box-shadow: var(--tab-shadow);
    }}
    .layout {{
      display: grid;
      grid-template-columns: var(--sidebar-w) 1fr;
      min-height: calc(100vh - 60px);
    }}
    .sidebar {{
      position: sticky;
      top: 60px;
      height: calc(100vh - 60px);
      overflow-y: auto;
      padding: 1rem;
      border-right: 1px solid var(--border);
      background: var(--surface);
    }}
    .sidebar h2 {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      margin: 0 0 0.75rem;
    }}
    .sidebar a, .sidebar button.filter-btn {{
      display: block;
      width: 100%;
      text-align: left;
      padding: 0.5rem 0.65rem;
      margin-bottom: 0.2rem;
      border-radius: 8px;
      color: var(--text);
      text-decoration: none;
      font-size: 0.88rem;
      border: none;
      background: transparent;
      cursor: pointer;
    }}
    .sidebar a:hover, .sidebar button.filter-btn:hover {{
      background: var(--bg);
    }}
    .sidebar a.active, .sidebar button.filter-btn.active {{
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 600;
    }}
    .main {{
      padding: 1.5rem 2rem 3rem;
      max-width: 920px;
    }}
    .panel {{ display: none; }}
    .panel.active {{ display: block; }}

    /* Study guide */
    .guide-content h2 {{
      margin-top: 2.5rem;
      padding-top: 1rem;
      border-top: 2px solid var(--border);
      scroll-margin-top: 80px;
    }}
    .guide-content h2:first-child {{ border-top: none; margin-top: 0; }}
    .guide-content h3 {{ color: var(--accent); margin-top: 1.5rem; }}
    .guide-content table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 0.92rem;
      background: var(--surface);
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: var(--shadow);
    }}
    .guide-content th, .guide-content td {{
      border: 1px solid var(--border);
      padding: 0.6rem 0.75rem;
      text-align: left;
    }}
    .guide-content th {{ background: var(--accent-soft); }}
    .guide-content ul {{ padding-left: 1.25rem; }}
    .guide-content strong {{ color: var(--strong); }}
    .guide-content img {{
      display: block;
      max-width: 100%;
      height: auto;
      margin: 1.25rem auto;
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}
    .guide-content blockquote {{
      margin: 0 0 1.5rem;
      padding: 0.75rem 1rem;
      background: var(--accent-soft);
      border-left: 4px solid var(--accent);
      border-radius: 0 var(--radius) var(--radius) 0;
      color: var(--muted);
    }}

    /* Flashcards */
    .fc-toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      margin-bottom: 1.25rem;
    }}
    .fc-toolbar select, .fc-toolbar button {{
      padding: 0.5rem 0.85rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      font-size: 0.9rem;
      cursor: pointer;
    }}
    .fc-toolbar button.primary {{
      background: var(--accent);
      color: var(--on-accent);
      border-color: var(--accent);
      font-weight: 600;
    }}
    .fc-progress {{
      font-size: 0.85rem;
      color: var(--muted);
      margin-bottom: 1rem;
    }}
    .fc-progress-bar {{
      height: 6px;
      background: var(--border);
      border-radius: 999px;
      overflow: hidden;
      margin-top: 0.35rem;
    }}
    .fc-progress-fill {{
      height: 100%;
      background: var(--success);
      width: 0%;
      transition: width 0.3s;
    }}
    .fc-progress-fill.confirm {{
      background: linear-gradient(90deg, var(--warning), var(--success));
    }}
    .fc-session-stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem 1.25rem;
      font-size: 0.82rem;
      color: var(--muted);
      margin-bottom: 0.75rem;
    }}
    .fc-session-stats strong {{ color: var(--text); }}
    .fc-stage {{
      position: relative;
    }}
    .fc-stage-toolbar {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 0.5rem;
    }}
    .fc-stage-toolbar button {{
      padding: 0.45rem 0.85rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      cursor: pointer;
      font-size: 0.85rem;
    }}
    .fc-stage.fullscreen {{
      position: fixed;
      inset: 0;
      z-index: 2000;
      background: var(--bg);
      display: flex;
      flex-direction: column;
      padding: 1.5rem 2rem 2rem;
      overflow: auto;
    }}
    .fc-fullscreen-progress {{
      display: none;
      flex: 1;
      min-width: 0;
    }}
    .fc-fullscreen-progress .fc-progress-bar {{
      margin-top: 0.35rem;
      margin-bottom: 0.5rem;
    }}
    .fc-stage.fullscreen .fc-stage-toolbar {{
      max-width: 960px;
      width: 100%;
      margin: 0 auto 0.75rem;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
    }}
    .fc-stage.fullscreen .fc-fullscreen-progress {{
      display: block;
    }}
    .fc-stage.fullscreen .flashcard-wrap {{
      max-width: 960px;
      width: 100%;
      margin: auto;
      flex: 1;
      display: flex;
      align-items: center;
    }}
    .fc-stage.fullscreen .flashcard {{
      width: 100%;
      min-height: min(52vh, 520px);
    }}
    .fc-stage.fullscreen .fc-question {{ font-size: clamp(1.35rem, 2.5vw, 1.85rem); }}
    .fc-stage.fullscreen .fc-answer {{ font-size: clamp(1.15rem, 2vw, 1.45rem); }}
    .fc-stage.fullscreen .fc-hint,
    .fc-stage.fullscreen .fc-actions {{
      max-width: 960px;
      width: 100%;
      margin-left: auto;
      margin-right: auto;
    }}
    .fc-stage-toolbar-actions {{
      display: flex;
      gap: 0.5rem;
      flex-shrink: 0;
    }}
    .fc-fullscreen-editor {{
      display: none;
      max-width: 960px;
      width: 100%;
      margin: auto;
      flex: 1;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
    }}
    .fc-fullscreen-editor h3 {{
      margin: 0 0 1rem;
      font-size: 1rem;
    }}
    .fc-fullscreen-editor label {{
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      margin: 0.75rem 0 0.35rem;
      color: var(--muted);
    }}
    .fc-fullscreen-editor input,
    .fc-fullscreen-editor textarea {{
      width: 100%;
      padding: 0.6rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--bg);
      font: inherit;
      box-sizing: border-box;
    }}
    .fc-fullscreen-editor textarea {{
      min-height: 90px;
      resize: vertical;
    }}
    .fc-fullscreen-editor-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1rem;
    }}
    .fc-fullscreen-editor-actions button {{
      padding: 0.5rem 1rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      cursor: pointer;
      font-size: 0.9rem;
    }}
    .fc-fullscreen-editor-actions button.primary {{
      background: var(--accent);
      color: var(--on-accent);
      border-color: var(--accent);
      font-weight: 600;
    }}
    .fc-stage.fullscreen.fc-editing .fc-fullscreen-editor {{
      display: block;
    }}
    .fc-stage.fullscreen.fc-editing .flashcard-wrap,
    .fc-stage.fullscreen.fc-editing .fc-hint,
    .fc-stage.fullscreen.fc-editing .fc-actions {{
      display: none;
    }}
    .flashcard-wrap {{
      perspective: 1200px;
      margin: 0 auto 1.5rem;
      max-width: 640px;
    }}
    .flashcard {{
      position: relative;
      min-height: 280px;
      cursor: pointer;
      transform-style: preserve-3d;
      transition: transform 0.45s ease;
    }}
    .flashcard.flipped {{ transform: rotateY(180deg); }}
    .fc-face {{
      position: absolute;
      inset: 0;
      backface-visibility: hidden;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 1.75rem;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .fc-back {{ transform: rotateY(180deg); background: var(--fc-back-bg); }}
    .fc-section {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent);
      font-weight: 700;
      margin-bottom: 0.75rem;
    }}
    .fc-question {{
      font-size: 1.2rem;
      font-weight: 600;
      line-height: 1.45;
    }}
    .fc-answer {{
      font-size: 1.05rem;
      line-height: 1.55;
    }}
    .fc-hint {{
      text-align: center;
      font-size: 0.8rem;
      color: var(--muted);
      margin-top: 0.5rem;
    }}
    .fc-hint kbd {{
      display: inline-block;
      padding: 0.1rem 0.4rem;
      border: 1px solid var(--border);
      border-radius: 4px;
      background: var(--surface);
      font-size: 0.75rem;
      font-family: inherit;
    }}
    .fc-status-badge {{
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--warning);
      margin-top: 0.75rem;
      min-height: 1.25rem;
    }}
    .fc-status-badge.confirm {{ color: var(--confirm); }}
    .fc-actions {{
      display: flex;
      justify-content: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }}
    .fc-actions button {{
      padding: 0.65rem 1.25rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      cursor: pointer;
      font-weight: 600;
    }}
    .fc-actions button.known {{ border-color: var(--success); color: var(--success); }}
    .fc-actions button.unknown {{ border-color: var(--warning); color: var(--warning); }}
    .fc-weak-panel {{
      margin-top: 2.5rem;
      padding: 1.25rem 1.5rem;
      background: var(--weak-bg);
      border: 1px solid var(--weak-border);
      border-radius: var(--radius);
    }}
    .fc-weak-panel h3 {{
      margin: 0 0 0.35rem;
      font-size: 1.1rem;
      color: var(--weak-title);
    }}
    .fc-weak-panel > p {{
      margin: 0 0 1rem;
      font-size: 0.9rem;
      color: var(--weak-text);
    }}
    .fc-weak-list {{
      display: grid;
      gap: 0.5rem;
      margin-bottom: 1rem;
      max-height: 320px;
      overflow-y: auto;
    }}
    .fc-weak-item {{
      background: var(--weak-item-bg);
      border: 1px solid var(--weak-item-border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      font-size: 0.9rem;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 0.75rem;
    }}
    .fc-weak-item:hover {{ border-color: var(--weak-item-hover); }}
    .fc-weak-item .fail-count {{
      flex-shrink: 0;
      background: var(--weak-badge-bg);
      color: var(--weak-badge-fg);
      font-weight: 700;
      font-size: 0.75rem;
      padding: 0.2rem 0.5rem;
      border-radius: 999px;
    }}
    .fc-weak-empty {{
      font-size: 0.9rem;
      color: var(--muted);
      font-style: italic;
    }}
    .fc-list {{
      display: grid;
      gap: 0.5rem;
      margin-top: 2rem;
    }}
    .fc-list-item {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      font-size: 0.9rem;
      cursor: pointer;
    }}
    .fc-list-item.done {{ opacity: 0.55; text-decoration: line-through; }}
    .fc-list-item .tag {{
      font-size: 0.7rem;
      color: var(--muted);
      display: block;
      margin-bottom: 0.2rem;
    }}

    /* Checklist */
    .checklist {{
      background: var(--surface);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: var(--shadow);
    }}
    .checklist label {{
      display: flex;
      gap: 0.75rem;
      padding: 0.6rem 0;
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      align-items: flex-start;
    }}
    .checklist label:last-child {{ border-bottom: none; }}
    .checklist input {{ margin-top: 0.25rem; accent-color: var(--accent); }}
    .checklist input:checked + span {{ color: var(--success); text-decoration: line-through; }}

    /* Editor */
    .editor-intro {{
      color: var(--muted);
      margin: 0 0 1.25rem;
      font-size: 0.95rem;
    }}
    .editor-toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }}
    .editor-toolbar button, .editor-toolbar label.btn-file {{
      padding: 0.5rem 0.85rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      font-size: 0.88rem;
      cursor: pointer;
      font-weight: 600;
    }}
    .editor-toolbar button.primary {{
      background: var(--accent);
      color: var(--on-accent);
      border-color: var(--accent);
    }}
    .editor-toolbar button.danger {{
      border-color: var(--danger-border);
      color: var(--danger);
    }}
    .editor-toolbar label.btn-file input {{ display: none; }}
    .editor-layout {{
      display: grid;
      grid-template-columns: 1fr 1.1fr;
      gap: 1.25rem;
      align-items: start;
    }}
    .editor-search {{
      width: 100%;
      padding: 0.6rem 0.85rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 0.75rem;
      font-size: 0.95rem;
      background: var(--surface);
      color: var(--text);
    }}
    .editor-list {{
      max-height: 70vh;
      overflow-y: auto;
      display: grid;
      gap: 0.4rem;
      padding-right: 0.25rem;
    }}
    .editor-list-item {{
      text-align: left;
      padding: 0.65rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      cursor: pointer;
      font-size: 0.88rem;
    }}
    .editor-list-item:hover {{ background: var(--bg); }}
    .editor-list-item.active {{
      border-color: var(--accent);
      background: var(--accent-soft);
    }}
    .editor-list-item .tag {{
      display: block;
      font-size: 0.68rem;
      color: var(--muted);
      margin-bottom: 0.2rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .editor-form {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.25rem;
      box-shadow: var(--shadow);
      position: sticky;
      top: 80px;
    }}
    .editor-form h3 {{ margin: 0 0 1rem; font-size: 1rem; }}
    .editor-form label {{
      display: block;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--muted);
      margin: 0.75rem 0 0.35rem;
    }}
    .editor-form label:first-of-type {{ margin-top: 0; }}
    .editor-form input, .editor-form select, .editor-form textarea {{
      width: 100%;
      padding: 0.6rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      font: inherit;
      font-size: 0.95rem;
      background: var(--surface);
      color: var(--text);
    }}
    .editor-form textarea {{ min-height: 100px; resize: vertical; }}
    .editor-form-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1.25rem;
    }}
    .editor-form-actions button {{
      padding: 0.55rem 1rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg);
      cursor: pointer;
      font-weight: 600;
    }}
    .editor-form-actions button.primary {{
      background: var(--accent);
      color: var(--on-accent);
      border-color: var(--accent);
    }}
    .editor-form-actions button.danger {{
      color: var(--danger);
      border-color: var(--danger-border);
    }}
    .editor-empty {{
      color: var(--muted);
      font-style: italic;
      padding: 2rem;
      text-align: center;
    }}
    .save-toast {{
      position: fixed;
      bottom: 1.25rem;
      right: 1.25rem;
      background: var(--toast-bg);
      color: var(--toast-fg);
      padding: 0.65rem 1rem;
      border-radius: 8px;
      font-size: 0.9rem;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s;
      z-index: 200;
    }}
    .save-toast.show {{ opacity: 1; }}

    /* Oefenexamen */
    .exam-intro {{
      color: var(--muted);
      margin: 0 0 1.25rem;
      font-size: 0.95rem;
    }}
    .exam-setup {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: var(--shadow);
      margin-bottom: 1.5rem;
    }}
    .exam-setup h2 {{ margin: 0 0 1rem; font-size: 1.1rem; }}
    .exam-setup-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      align-items: flex-end;
      margin-bottom: 1rem;
    }}
    .exam-setup label {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--muted);
    }}
    .exam-setup select {{
      padding: 0.55rem 0.75rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      font: inherit;
      min-width: 160px;
    }}
    .exam-setup button.primary {{
      padding: 0.6rem 1.25rem;
      border-radius: 8px;
      border: none;
      background: var(--accent);
      color: var(--on-accent);
      font-weight: 600;
      cursor: pointer;
    }}
    .exam-progress {{
      font-size: 0.88rem;
      color: var(--muted);
      margin-bottom: 1rem;
    }}
    .exam-question-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: var(--shadow);
      margin-bottom: 1rem;
    }}
    .exam-question-card .exam-q-num {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent);
      font-weight: 700;
      margin-bottom: 0.5rem;
    }}
    .exam-question-card .exam-q-text {{
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 1.25rem;
      line-height: 1.45;
    }}
    .exam-options {{
      display: grid;
      gap: 0.5rem;
    }}
    .exam-option {{
      display: flex;
      gap: 0.75rem;
      align-items: flex-start;
      padding: 0.75rem 1rem;
      border: 2px solid var(--border);
      border-radius: 10px;
      cursor: pointer;
      background: var(--surface);
      transition: border-color 0.15s, background 0.15s;
    }}
    .exam-option:hover {{ background: var(--bg); }}
    .exam-option input {{ margin-top: 0.2rem; accent-color: var(--accent); }}
    .exam-option.selected {{ border-color: var(--accent); background: var(--accent-soft); }}
    .exam-option.correct {{ border-color: var(--success); background: var(--success-soft); }}
    .exam-option.wrong {{ border-color: var(--error); background: var(--danger-soft); }}
    .exam-option.missed {{ border-color: var(--success); background: var(--success-soft); opacity: 0.85; }}
    .exam-nav-btns {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 1.25rem;
    }}
    .exam-nav-btns button {{
      padding: 0.6rem 1.1rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface);
      cursor: pointer;
      font-weight: 600;
    }}
    .exam-nav-btns button.primary {{
      background: var(--accent);
      color: var(--on-accent);
      border-color: var(--accent);
    }}
    .exam-nav-btns button.success {{
      background: var(--success);
      color: var(--on-accent);
      border-color: var(--success);
    }}
    .exam-results {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: var(--shadow);
      margin-bottom: 1.5rem;
    }}
    .exam-score-big {{
      font-size: 2.5rem;
      font-weight: 800;
      color: var(--accent);
      line-height: 1.1;
    }}
    .exam-score-sub {{ color: var(--muted); margin-top: 0.35rem; }}
    .exam-review-item {{
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1rem;
      margin-top: 0.75rem;
      font-size: 0.92rem;
    }}
    .exam-review-item.wrong {{ border-left: 4px solid #ef4444; }}
    .exam-review-item.right {{ border-left: 4px solid var(--success); }}
    .exam-history-list {{
      display: grid;
      gap: 0.5rem;
    }}
    .exam-history-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 0.85rem 1rem;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--surface);
      cursor: pointer;
      text-align: left;
      width: 100%;
      font: inherit;
    }}
    .exam-history-item:hover {{ background: var(--bg); }}
    .exam-history-item.active {{
      border-color: var(--accent);
      background: var(--accent-soft);
    }}
    .exam-history-item .score {{ font-weight: 700; color: var(--accent); }}
    .exam-history-item .meta {{ font-size: 0.82rem; color: var(--muted); }}
    .exam-sidebar-hint {{
      font-size: 0.8rem;
      color: var(--muted);
      margin: 0.75rem 0 0;
      line-height: 1.4;
    }}
    .exam-empty {{
      color: var(--muted);
      font-style: italic;
      padding: 1.5rem;
      text-align: center;
    }}
    #exam-nav .filter-btn {{ margin-bottom: 0.25rem; }}

    /* Mindmaps */
    .mindmaps-intro {{
      color: var(--muted);
      margin: 0 0 1rem;
      font-size: 0.95rem;
    }}
    .mm-group-label {{
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
      margin: 0.85rem 0 0.35rem;
      font-weight: 700;
    }}
    .mm-group-label:first-child {{ margin-top: 0; }}
    .mm-nav-btn {{ font-size: 0.84rem; }}
    .mm-nav-btn.active {{
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 600;
    }}
    .mm-subtitle {{
      color: var(--muted);
      margin: -0.5rem 0 1.25rem;
      font-size: 0.92rem;
    }}
    .mm-diagram-wrap {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.25rem;
      box-shadow: var(--shadow);
      overflow-x: auto;
      min-height: 320px;
    }}
    .mm-diagram-wrap svg {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 0 auto;
    }}
    .panel-mindmaps {{ max-width: 1100px; }}
    .mm-loading {{
      color: var(--muted);
      font-style: italic;
      padding: 2rem;
      text-align: center;
    }}

    @media (max-width: 900px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{
        position: static;
        height: auto;
        border-right: none;
        border-bottom: 1px solid var(--border);
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        padding: 0.75rem;
      }}
      .sidebar h2 {{ width: 100%; }}
      .sidebar a, .sidebar button.filter-btn {{
        width: auto;
        display: inline-block;
        margin: 0;
      }}
      .main {{ padding: 1rem; }}
      .editor-layout {{ grid-template-columns: 1fr; }}
      .editor-form {{ position: static; }}
    }}
  </style>
</head>
<body>
  <header class="app-header">
    <h1>Life Events — Examen</h1>
    <div class="header-actions">
      <div class="tabs" role="tablist">
        <button class="tab active" data-panel="guide" role="tab">Studiegids</button>
        <button class="tab" data-panel="flashcards" role="tab">Flashcards (<span id="tab-fc-count">{len(cards)}</span>)</button>
        <button class="tab" data-panel="editor" role="tab">Bewerken</button>
        <button class="tab" data-panel="exam" role="tab">Oefenexamen</button>
        <button class="tab" data-panel="mindmaps" role="tab">Mindmaps</button>
        <button class="tab" data-panel="checklist" role="tab">Checklist</button>
      </div>
      <button type="button" class="theme-toggle" id="btn-theme-toggle" title="Donker thema" aria-label="Donker thema">🌙</button>
    </div>
  </header>

  <div class="layout">
    <aside class="sidebar" id="sidebar">
      <h2 id="sidebar-title">Navigatie</h2>
      <div id="guide-nav">
        {"".join(f'<a href="#{n["anchor"]}">{n["label"]}</a>' for n in nav)}
      </div>
      <div id="fc-nav" style="display:none"></div>
      <div id="editor-nav" style="display:none">
        <button class="filter-btn active" data-editor-section="all">Alle kaarten</button>
        {"".join(
            f'<button class="filter-btn" data-editor-section="{s}">{s.split(":")[0] if ":" in s else s}</button>'
            for s in sections
        )}
      </div>
      <div id="exam-nav" style="display:none">
        <button class="filter-btn active" data-exam-section="all">Alle vragen</button>
        {"".join(
            f'<button class="filter-btn" data-exam-section="{s}">{s}</button>'
            for s in exam_sections
        )}
        <p class="exam-sidebar-hint">Kies een onderwerp en start een oefenexamen. Resultaten worden lokaal opgeslagen op dit apparaat.</p>
        <h2 style="margin-top:1.25rem">Historiek</h2>
        <div class="exam-history-list" id="exam-history-sidebar"></div>
        <button type="button" class="filter-btn" id="btn-clear-exam-history" style="margin-top:0.5rem;color:var(--danger)">Wis historiek</button>
      </div>
      <div id="mindmap-nav" style="display:none">
        {build_mindmap_sidebar()}
      </div>
    </aside>

    <main class="main">
      <section id="panel-guide" class="panel active guide-content">
        {guide_html}
      </section>

      <section id="panel-flashcards" class="panel">
        <div class="fc-toolbar">
          <button class="primary" id="btn-shuffle">Shuffle wachtrij</button>
          <button id="btn-reset-progress">Reset voortgang</button>
          <button id="btn-show-list">Toon alle kaarten</button>
          <button id="btn-edit-current">Bewerk huidige kaart</button>
        </div>
        <div class="fc-progress">
          <span id="fc-stats">0 / 0 beheerst</span>
          <div class="fc-progress-bar"><div class="fc-progress-fill" id="fc-progress-fill"></div></div>
        </div>
        <div class="fc-session-stats" id="fc-session-stats"></div>
        <div class="fc-stage" id="fc-stage">
          <div class="fc-stage-toolbar">
            <div class="fc-fullscreen-progress" id="fc-fullscreen-progress" aria-hidden="true">
              <span id="fc-stats-fullscreen">0 / 0 beheerst</span>
              <div class="fc-progress-bar"><div class="fc-progress-fill" id="fc-progress-fill-fullscreen"></div></div>
              <div class="fc-session-stats" id="fc-session-stats-fullscreen"></div>
            </div>
            <div class="fc-stage-toolbar-actions">
              <button type="button" id="btn-fc-edit" title="Huidige kaart bewerken" style="display:none">✎ Bewerk</button>
              <button type="button" id="btn-fc-fullscreen" title="Groot scherm (Esc om te sluiten)">⛶ Groot scherm</button>
            </div>
          </div>
          <div class="fc-fullscreen-editor" id="fc-fullscreen-editor" hidden>
            <h3>Kaart bewerken</h3>
            <label for="fc-edit-section">Onderwerp / hoorcollege</label>
            <input list="section-options" id="fc-edit-section" placeholder="bv. Hoorcollege 1: Inleiding">
            <label for="fc-edit-question">Vraag</label>
            <textarea id="fc-edit-question" rows="3"></textarea>
            <label for="fc-edit-answer">Antwoord</label>
            <textarea id="fc-edit-answer" rows="6"></textarea>
            <div class="fc-fullscreen-editor-actions">
              <button type="button" class="primary" id="btn-fc-save-card">Opslaan</button>
              <button type="button" id="btn-fc-cancel-edit">Annuleren</button>
            </div>
          </div>
          <div class="flashcard-wrap" id="fc-wrap">
            <div class="flashcard" id="flashcard" aria-live="polite">
              <div class="fc-face fc-front">
                <div class="fc-section" id="fc-section"></div>
                <div class="fc-question" id="fc-question"></div>
                <div class="fc-status-badge" id="fc-status-badge"></div>
              </div>
              <div class="fc-face fc-back">
                <div class="fc-section" id="fc-section-back"></div>
                <div class="fc-answer" id="fc-answer"></div>
                <div class="fc-status-badge confirm" id="fc-status-badge-back"></div>
              </div>
            </div>
          </div>
          <p class="fc-hint">
            Klik of <kbd>Spatie</kbd> = omdraaien ·
            <kbd>←</kbd> <kbd>→</kbd> = vorige/volgende ·
            <kbd>Enter</kbd> = ken ik (2× = echt beheerst) ·
            <kbd>Backspace</kbd> = ken ik niet
          </p>
          <div class="fc-actions">
            <button class="unknown" id="btn-hard">Ken ik niet (Backspace)</button>
            <button id="btn-prev">← Vorige</button>
            <button id="btn-next">Volgende →</button>
            <button class="known" id="btn-easy">Ken ik (Enter)</button>
          </div>
        </div>
        <div class="fc-weak-panel" id="fc-weak-panel">
          <h3>Meer aandacht nodig</h3>
          <p>Kaarten die je minstens 2× als &ldquo;ken ik niet&rdquo; hebt gemarkeerd. Oefen deze extra.</p>
          <div class="fc-weak-list" id="fc-weak-list"></div>
          <button type="button" class="primary" id="btn-study-weak" style="display:none">Oefen alleen zwakke kaarten</button>
          <button type="button" id="btn-study-all" style="display:none">Terug naar alle kaarten</button>
        </div>
        <div class="fc-list" id="fc-list" style="display:none"></div>
      </section>

      <section id="panel-editor" class="panel">
        <p class="editor-intro">
          Pas vragen en antwoorden hier direct aan. Wijzigingen worden automatisch opgeslagen in je browser.
          Gebruik <strong>Exporteer backup</strong> om een kopie te bewaren, of <strong>Herstel origineel</strong> om terug te gaan naar de standaardkaarten.
        </p>
        <div class="editor-toolbar">
          <button class="primary" id="btn-new-card">+ Nieuwe kaart</button>
          <button id="btn-export-cards">Exporteer backup</button>
          <label class="btn-file">Importeer backup<input type="file" id="import-file" accept=".json"></label>
          <button class="danger" id="btn-reset-cards">Herstel origineel</button>
        </div>
        <div class="editor-layout">
          <div>
            <input type="search" class="editor-search" id="editor-search" placeholder="Zoek in vragen of antwoorden…">
            <div class="editor-list" id="editor-list"></div>
          </div>
          <div class="editor-form" id="editor-form-wrap">
            <h3 id="editor-form-title">Selecteer een kaart</h3>
            <div id="editor-form-empty" class="editor-empty">Kies een kaart uit de lijst of maak een nieuwe aan.</div>
            <div id="editor-form-fields" style="display:none">
              <label for="edit-section">Onderwerp / hoorcollege</label>
              <input list="section-options" id="edit-section" placeholder="bv. Hoorcollege 1: Inleiding">
              <datalist id="section-options">
                {"".join(f'<option value="{s}">' for s in sections)}
              </datalist>
              <label for="edit-question">Vraag</label>
              <textarea id="edit-question" rows="3"></textarea>
              <label for="edit-answer">Antwoord</label>
              <textarea id="edit-answer" rows="5"></textarea>
              <div class="editor-form-actions">
                <button class="primary" id="btn-save-card">Opslaan</button>
                <button id="btn-duplicate-card">Dupliceren</button>
                <button class="danger" id="btn-delete-card">Verwijderen</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="panel-exam" class="panel">
        <div id="exam-view-start">
          <p class="exam-intro">
            Oefen met meerkeuzevragen in <strong>examstijl</strong> (casussen, stellingen, tool-keuze).
            Inclusief reconstructie van het <strong>1e zit 2025-2026</strong> (antwoorden op basis van cursus + studentenconsensus; niet officieel geverifieerd).
            Resultaten worden <strong>lokaal opgeslagen</strong> in je browser (per apparaat, geen database).
          </p>
          <div class="exam-setup">
            <h2>Nieuw oefenexamen</h2>
            <div class="exam-setup-row">
              <label>
                Aantal vragen
                <select id="exam-count">
                  <option value="10">10 vragen</option>
                  <option value="20" selected>20 vragen</option>
                  <option value="30">30 vragen</option>
                  <option value="50">50 vragen</option>
                  <option value="all">Alle beschikbare vragen</option>
                </select>
              </label>
              <label>
                Onderwerp
                <select id="exam-section-select">
                  <option value="all">Alle vragen</option>
                  {"".join(f'<option value="{s}">{s}</option>' for s in exam_sections)}
                </select>
              </label>
              <button type="button" class="primary" id="btn-start-exam">Start oefenexamen</button>
            </div>
            <p class="exam-sidebar-hint" style="margin:0">
              Vragenset: <strong id="exam-bank-count">{len(mc_questions)}</strong> meerkeuzevragen beschikbaar.
            </p>
          </div>
          <div id="exam-recent-wrap">
            <h2>Recente resultaten</h2>
            <div id="exam-recent-list" class="exam-history-list"></div>
            <p class="exam-empty" id="exam-recent-empty" style="display:none">Nog geen oefenexamens afgelegd op dit apparaat.</p>
          </div>
        </div>

        <div id="exam-view-active" style="display:none">
          <div class="exam-progress" id="exam-progress-text">Vraag 1 / 20</div>
          <div class="exam-question-card" id="exam-question-card"></div>
          <div class="exam-nav-btns">
            <button type="button" id="btn-exam-prev">← Vorige</button>
            <button type="button" id="btn-exam-next">Volgende →</button>
            <button type="button" class="success" id="btn-exam-submit">Examen indienen</button>
            <button type="button" id="btn-exam-cancel">Annuleren</button>
          </div>
        </div>

        <div id="exam-view-results" style="display:none">
          <div class="exam-results" id="exam-results-summary"></div>
          <h2>Overzicht antwoorden</h2>
          <div id="exam-review-list"></div>
          <div class="exam-nav-btns" style="margin-top:1.5rem">
            <button type="button" class="primary" id="btn-exam-retry">Nieuw oefenexamen</button>
            <button type="button" id="btn-exam-back-start">Terug naar start</button>
          </div>
        </div>

        <div id="exam-view-history" style="display:none">
          <button type="button" class="filter-btn" id="btn-exam-back-from-history" style="margin-bottom:1rem">← Terug</button>
          <div class="exam-results" id="exam-history-detail-summary"></div>
          <div id="exam-history-detail-review"></div>
        </div>
      </section>

      <section id="panel-mindmaps" class="panel panel-mindmaps">
        <p class="mindmaps-intro">
          Visueel overzicht per hoorcollege en per complex artikel. Kies links een mindmap.
          Klik en sleep om te pannen · scroll om te zoomen (in de SVG).
        </p>
        <div id="mindmap-panels">
          {build_mindmap_panels()}
        </div>
      </section>

      <section id="panel-checklist" class="panel">
        <h2>Snelle examenchecklist</h2>
        <p style="color:var(--muted)">Vink af wat je vanbuiten kent. Je voortgang wordt lokaal opgeslagen.</p>
        <div class="checklist" id="checklist">
          {"".join(f'<label><input type="checkbox" data-id="c{i}"><span>{item}</span></label>' for i, item in enumerate(checklist))}
        </div>
      </section>
    </main>
  </div>

  <div class="save-toast" id="save-toast">Opgeslagen</div>

  <script>
    const DEFAULT_CARDS = {json.dumps(cards, ensure_ascii=False)};
    const MC_QUESTIONS = {json.dumps(mc_questions, ensure_ascii=False)};
    const STORAGE_CARDS = 'life_events_cards_custom';
    const STORAGE_FC = 'life_events_fc_known';
    const STORAGE_FC_PROGRESS = 'life_events_fc_progress';
    const STORAGE_CL = 'life_events_checklist';
    const STORAGE_EXAM_HISTORY = 'life_events_exam_history';
    const STORAGE_THEME = 'life_events_theme';
    const EXAM_HISTORY_MAX = 50;
    const FC_REQUEUE_GOOD = 5;
    const FC_REQUEUE_BAD = 5;
    const FC_WEAK_THRESHOLD = 2;
    const MM_DEFAULT_ID = {json.dumps(MINDMAPS[0]["id"])};
    let currentMmId = MM_DEFAULT_ID;
    let mermaidApi = null;
    let mermaidThemeUsed = null;
    const mmRendered = new Set();

    let CARDS = loadCards();
    let fcProgress = loadFcProgress();
    let queue = [];
    let index = 0;
    let filterSection = 'all';
    let weakStudyMode = false;
    let listVisible = false;
    let fcFullscreen = false;
    let fcFullscreenEditing = false;
    let editingId = null;
    let editorFilterSection = 'all';
    let editorSearch = '';

    function getTheme() {{
      return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    }}

    function getMermaidTheme() {{
      return getTheme() === 'dark' ? 'dark' : 'neutral';
    }}

    function applyTheme(theme, save = true) {{
      if (theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
      else document.documentElement.removeAttribute('data-theme');
      if (save) {{
        try {{ localStorage.setItem(STORAGE_THEME, theme); }} catch (e) {{}}
      }}
      const btn = document.getElementById('btn-theme-toggle');
      if (btn) {{
        btn.textContent = theme === 'dark' ? '☀️' : '🌙';
        btn.title = theme === 'dark' ? 'Licht thema' : 'Donker thema';
        btn.setAttribute('aria-label', btn.title);
      }}
      refreshMermaidTheme();
    }}

    function initTheme() {{
      let theme;
      try {{ theme = localStorage.getItem(STORAGE_THEME); }} catch (e) {{}}
      if (!theme) {{
        theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }}
      applyTheme(theme, false);
    }}

    function refreshMermaidTheme() {{
      const next = getMermaidTheme();
      if (mermaidThemeUsed === next && mermaidApi) return;
      mermaidThemeUsed = next;
      mermaidApi = null;
      mmRendered.clear();
      const panel = document.getElementById('panel-mindmaps');
      if (panel && panel.classList.contains('active') && currentMmId) showMindmap(currentMmId);
    }}

    function loadFcProgress() {{
      let raw = {{}};
      try {{
        const stored = localStorage.getItem(STORAGE_FC_PROGRESS);
        if (stored) {{
          const parsed = JSON.parse(stored);
          if (parsed && typeof parsed === 'object') raw = parsed;
        }}
      }} catch (e) {{}}
      if (!Object.keys(raw).length) {{
        try {{
          const legacy = JSON.parse(localStorage.getItem(STORAGE_FC) || '[]');
          legacy.forEach(id => {{
            raw[id] = {{ state: 'mastered', fails: 0 }};
          }});
        }} catch (e) {{}}
      }}
      const migrated = migrateFcProgress(raw);
      if (JSON.stringify(migrated) !== JSON.stringify(raw)) {{
        localStorage.setItem(STORAGE_FC_PROGRESS, JSON.stringify(migrated));
      }}
      return migrated;
    }}

    function getCardProgress(id) {{
      if (!fcProgress[id]) fcProgress[id] = {{ state: 'new', fails: 0 }};
      return fcProgress[id];
    }}

    function isMastered(id) {{
      return getCardProgress(id).state === 'mastered';
    }}

    function saveFcProgress() {{
      localStorage.setItem(STORAGE_FC_PROGRESS, JSON.stringify(fcProgress));
      const mastered = Object.entries(fcProgress)
        .filter(([, p]) => p.state === 'mastered')
        .map(([id]) => id);
      localStorage.setItem(STORAGE_FC, JSON.stringify(mastered));
      updateStats();
    }}

    function loadCards() {{
      const defaults = JSON.parse(JSON.stringify(DEFAULT_CARDS));
      try {{
        const saved = localStorage.getItem(STORAGE_CARDS);
        if (saved) {{
          const parsed = JSON.parse(saved);
          if (Array.isArray(parsed) && parsed.length) return mergeCardSets(parsed, defaults);
        }}
      }} catch (e) {{}}
      return defaults;
    }}

    function saveCards(showToast = true) {{
      localStorage.setItem(STORAGE_CARDS, JSON.stringify(CARDS));
      rebuildFcNav();
      document.getElementById('tab-fc-count').textContent = CARDS.length;
      updateStats();
      if (showToast) showSaved();
    }}

    function showSaved() {{
      const t = document.getElementById('save-toast');
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 1600);
    }}

    function cardKey(c) {{
      return c.section + '\\x1f' + c.q;
    }}

    function progressRank(p) {{
      const ranks = {{ new: 0, confirm: 1, mastered: 2 }};
      return ranks[p && p.state] || 0;
    }}

    function mergeProgressEntry(a, b) {{
      if (!a) return b;
      if (!b) return a;
      const primary = progressRank(a) >= progressRank(b) ? a : b;
      return {{
        state: primary.state,
        fails: Math.max(a.fails || 0, b.fails || 0),
      }};
    }}

    function migrateFcProgress(raw) {{
      const idToContent = {{}};
      [...CARDS, ...DEFAULT_CARDS].forEach(c => {{
        idToContent[c.id] = cardKey(c);
      }});
      const migrated = {{}};
      Object.entries(raw || {{}}).forEach(([key, val]) => {{
        const contentKey = idToContent[key] || key;
        migrated[contentKey] = mergeProgressEntry(migrated[contentKey], val);
      }});
      return migrated;
    }}

    function mergeCardSets(saved, defaults) {{
      const savedByContent = new Map(saved.map(c => [cardKey(c), c]));
      const merged = [];
      const seen = new Set();
      defaults.forEach(def => {{
        const key = cardKey(def);
        const custom = savedByContent.get(key);
        merged.push(custom ? {{ ...custom, id: def.id }} : {{ ...def }});
        seen.add(key);
      }});
      saved.forEach(c => {{
        const key = cardKey(c);
        if (!seen.has(key)) {{
          merged.push({{ ...c }});
          seen.add(key);
        }}
      }});
      return merged;
    }}

    function newId() {{
      return 'c' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
    }}

    function getSections() {{
      return [...new Set(CARDS.map(c => c.section))].sort();
    }}

    function rebuildFcNav() {{
      const nav = document.getElementById('fc-nav');
      const sections = getSections();
      nav.innerHTML = `<button class="filter-btn active" data-section="all">Alle (${{CARDS.length}})</button>` +
        sections.map(s => {{
          const n = CARDS.filter(c => c.section === s).length;
          const label = s.includes(':') ? s.split(':')[0] : s;
          return `<button class="filter-btn" data-section="${{escapeAttr(s)}}">${{label}} (${{n}})</button>`;
        }}).join('');
      nav.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          nav.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          filterSection = btn.dataset.section;
          weakStudyMode = false;
          applyFilter();
          updateWeakStudyButtons();
        }});
      }});
      if (filterSection !== 'all' && !sections.includes(filterSection)) filterSection = 'all';
    }}

    function escapeAttr(s) {{
      return s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
    }}

    function escapeHtml(s) {{
      return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }}

    // Tabs
    const tabs = document.querySelectorAll('.tab');
    const panels = document.querySelectorAll('.panel');
    const guideNav = document.getElementById('guide-nav');
    const fcNav = document.getElementById('fc-nav');
    const editorNav = document.getElementById('editor-nav');
    const examNav = document.getElementById('exam-nav');
    const mindmapNav = document.getElementById('mindmap-nav');
    const sidebarTitle = document.getElementById('sidebar-title');

    function switchPanel(name) {{
      tabs.forEach(t => t.classList.toggle('active', t.dataset.panel === name));
      panels.forEach(p => p.classList.remove('active'));
      document.getElementById('panel-' + name).classList.add('active');
      guideNav.style.display = name === 'guide' ? 'block' : 'none';
      fcNav.style.display = name === 'flashcards' ? 'block' : 'none';
      editorNav.style.display = name === 'editor' ? 'block' : 'none';
      examNav.style.display = name === 'exam' ? 'block' : 'none';
      mindmapNav.style.display = name === 'mindmaps' ? 'block' : 'none';
      if (name === 'guide') sidebarTitle.textContent = 'Navigatie';
      else if (name === 'flashcards') sidebarTitle.textContent = 'Filter';
      else if (name === 'editor') {{ sidebarTitle.textContent = 'Onderwerp'; renderEditorList(); }}
      else if (name === 'exam') {{ sidebarTitle.textContent = 'Oefenexamen'; renderExamHistory(); showExamView('start'); }}
      else if (name === 'mindmaps') {{ sidebarTitle.textContent = 'Mindmaps'; showMindmap(currentMmId || MM_DEFAULT_ID); }}
      else sidebarTitle.textContent = '';
    }}

    tabs.forEach(tab => tab.addEventListener('click', () => switchPanel(tab.dataset.panel)));

    document.querySelectorAll('#editor-nav .filter-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('#editor-nav .filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        editorFilterSection = btn.dataset.editorSection;
        renderEditorList();
      }});
    }});

    function saveKnown() {{ saveFcProgress(); }}

    function filteredPool() {{
      return filterSection === 'all' ? CARDS : CARDS.filter(c => c.section === filterSection);
    }}

    function buildQueue(shuffle = false) {{
      const pool = filteredPool();
      if (weakStudyMode) {{
        queue = pool.filter(c => {{
          const p = getCardProgress(cardKey(c));
          return p.fails >= FC_WEAK_THRESHOLD && p.state !== 'mastered';
        }});
      }} else {{
        queue = pool.filter(c => !isMastered(cardKey(c)));
      }}
      if (shuffle) {{
        for (let i = queue.length - 1; i > 0; i--) {{
          const j = Math.floor(Math.random() * (i + 1));
          [queue[i], queue[j]] = [queue[j], queue[i]];
        }}
      }}
      if (!queue.length) index = 0;
      else if (index >= queue.length) index = 0;
    }}

    function applyFilter() {{
      buildQueue(false);
      renderCard();
      updateStats();
      renderList();
      renderWeakList();
      updateWeakStudyButtons();
    }}

    function updateWeakStudyButtons() {{
      const weakCount = getWeakCards().length;
      const btnWeak = document.getElementById('btn-study-weak');
      const btnAll = document.getElementById('btn-study-all');
      btnWeak.style.display = !weakStudyMode && weakCount > 0 ? 'inline-block' : 'none';
      btnAll.style.display = weakStudyMode ? 'inline-block' : 'none';
    }}

    function getWeakCards() {{
      return CARDS.filter(c => {{
        const p = getCardProgress(cardKey(c));
        return p.fails >= FC_WEAK_THRESHOLD;
      }}).sort((a, b) => getCardProgress(cardKey(b)).fails - getCardProgress(cardKey(a)).fails);
    }}

    function renderWeakList() {{
      const list = document.getElementById('fc-weak-list');
      const weak = getWeakCards();
      if (!weak.length) {{
        list.innerHTML = '<p class="fc-weak-empty">Nog geen kaarten met meerdere fouten — goed bezig!</p>';
        return;
      }}
      list.innerHTML = weak.map(c => {{
        const p = getCardProgress(cardKey(c));
        const mastered = p.state === 'mastered' ? ' · beheerst' : '';
        return `<div class="fc-weak-item" data-id="${{c.id}}">
          <div><span class="tag">${{escapeHtml(c.section)}}</span> ${{escapeHtml(c.q)}}${{mastered}}</div>
          <span class="fail-count">${{p.fails}}× fout</span>
        </div>`;
      }}).join('');
      list.querySelectorAll('.fc-weak-item').forEach(el => {{
        el.addEventListener('click', () => {{
          const card = CARDS.find(c => c.id === el.dataset.id);
          if (!card) return;
          weakStudyMode = false;
          filterSection = card.section;
          rebuildFcNav();
          buildQueue(false);
          const idx = queue.findIndex(c => c.id === card.id);
          if (idx < 0) {{
            queue = [card, ...queue];
            index = 0;
          }} else index = idx;
          renderCard();
          updateWeakStudyButtons();
          document.getElementById('fc-stage').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }});
      }});
    }}

    function renderCard() {{
      const card = document.getElementById('flashcard');
      card.classList.remove('flipped');
      if (!queue.length) {{
        document.getElementById('fc-question').textContent = weakStudyMode
          ? 'Geen zwakke kaarten meer in deze selectie — goed gedaan!'
          : 'Alle kaarten in deze selectie zijn beheerst!';
        document.getElementById('fc-answer').textContent = weakStudyMode
          ? 'Klik op "Terug naar alle kaarten" om verder te oefenen.'
          : 'Kies een ander filter of reset de voortgang om opnieuw te starten.';
        document.getElementById('fc-section').textContent = '';
        document.getElementById('fc-section-back').textContent = '';
        document.getElementById('fc-status-badge').textContent = '';
        document.getElementById('fc-status-badge-back').textContent = '';
        if (fcFullscreen) {{
          document.getElementById('btn-fc-edit').style.display = 'none';
          if (fcFullscreenEditing) closeFcFullscreenEditor();
        }}
        return;
      }}
      const c = queue[index];
      const p = getCardProgress(cardKey(c));
      document.getElementById('fc-section').textContent = c.section;
      document.getElementById('fc-section-back').textContent = c.section;
      document.getElementById('fc-question').textContent = c.q;
      document.getElementById('fc-answer').textContent = c.a;
      let badge = '';
      if (p.state === 'confirm') {{
        badge = '↻ Nog 1× op Enter = echt beheerst';
      }} else if (p.fails >= FC_WEAK_THRESHOLD) {{
        badge = '⚠ ' + p.fails + '× eerder fout — extra oefenen';
      }}
      document.getElementById('fc-status-badge').textContent = badge;
      document.getElementById('fc-status-badge-back').textContent = badge;
      if (fcFullscreen) document.getElementById('btn-fc-edit').style.display = 'inline-block';
    }}

    function updateStats() {{
      const pool = filteredPool();
      const total = pool.length || 1;
      const mastered = pool.filter(c => isMastered(cardKey(c))).length;
      const confirm = pool.filter(c => getCardProgress(cardKey(c)).state === 'confirm').length;
      const remaining = pool.filter(c => !isMastered(cardKey(c))).length;
      const summary = mastered + ' / ' + pool.length + ' beheerst in deze selectie';
      const sessionHtml =
        '<span><strong>' + remaining + '</strong> nog te leren</span>' +
        '<span><strong>' + confirm + '</strong> wacht op bevestiging</span>' +
        '<span><strong>' + queue.length + '</strong> in wachtrij</span>' +
        (queue.length ? '<span>Kaart <strong>' + (index + 1) + '</strong> / ' + queue.length + '</span>' : '');
      const showConfirm = confirm > 0 && mastered < pool.length;
      const pct = (mastered / total * 100) + '%';

      document.getElementById('fc-stats').textContent = summary;
      document.getElementById('fc-progress-fill').style.width = pct;
      document.getElementById('fc-progress-fill').classList.toggle('confirm', showConfirm);
      document.getElementById('fc-session-stats').innerHTML = sessionHtml;

      document.getElementById('fc-stats-fullscreen').textContent = summary;
      document.getElementById('fc-progress-fill-fullscreen').style.width = pct;
      document.getElementById('fc-progress-fill-fullscreen').classList.toggle('confirm', showConfirm);
      document.getElementById('fc-session-stats-fullscreen').innerHTML = sessionHtml;
    }}

    function nextCard() {{
      if (!queue.length) return;
      index = (index + 1) % queue.length;
      renderCard();
    }}

    function prevCard() {{
      if (!queue.length) return;
      index = (index - 1 + queue.length) % queue.length;
      renderCard();
    }}

    function flipCard() {{
      document.getElementById('flashcard').classList.toggle('flipped');
    }}

    function isCardFlipped() {{
      return document.getElementById('flashcard').classList.contains('flipped');
    }}

    function requeueCard(offset) {{
      const card = queue.splice(index, 1)[0];
      const insertAt = Math.min(index + offset, queue.length);
      queue.splice(insertAt, 0, card);
      if (index >= queue.length) index = 0;
    }}

    function rateGood() {{
      if (!queue.length) return;
      if (!isCardFlipped()) {{ flipCard(); return; }}
      const c = queue[index];
      const key = cardKey(c);
      const p = getCardProgress(key);
      if (p.state === 'confirm') {{
        p.state = 'mastered';
        saveFcProgress();
        queue.splice(index, 1);
        if (index >= queue.length) index = 0;
      }} else {{
        p.state = 'confirm';
        saveFcProgress();
        requeueCard(FC_REQUEUE_GOOD);
      }}
      renderCard();
      updateStats();
      renderList();
      renderWeakList();
      updateWeakStudyButtons();
    }}

    function rateBad() {{
      if (!queue.length) return;
      if (!isCardFlipped()) {{ flipCard(); return; }}
      const c = queue[index];
      const key = cardKey(c);
      const p = getCardProgress(key);
      p.fails = (p.fails || 0) + 1;
      p.state = 'new';
      saveFcProgress();
      requeueCard(FC_REQUEUE_BAD);
      renderCard();
      updateStats();
      renderList();
      renderWeakList();
      updateWeakStudyButtons();
    }}

    function updateCardContent(card, data) {{
      const oldKey = cardKey(card);
      Object.assign(card, data);
      const newKey = cardKey(card);
      if (oldKey !== newKey && fcProgress[oldKey]) {{
        fcProgress[newKey] = mergeProgressEntry(fcProgress[newKey], fcProgress[oldKey]);
        delete fcProgress[oldKey];
        saveFcProgress();
      }}
    }}

    function readFullscreenEditorForm() {{
      return {{
        section: document.getElementById('fc-edit-section').value.trim() || 'Eigen kaarten',
        q: document.getElementById('fc-edit-question').value.trim(),
        a: document.getElementById('fc-edit-answer').value.trim(),
      }};
    }}

    function openFcFullscreenEditor() {{
      if (!fcFullscreen || !queue.length) return;
      const card = queue[index];
      fcFullscreenEditing = true;
      document.getElementById('fc-stage').classList.add('fc-editing');
      document.getElementById('fc-fullscreen-editor').hidden = false;
      document.getElementById('btn-fc-edit').textContent = '✕ Sluit bewerken';
      document.getElementById('fc-edit-section').value = card.section;
      document.getElementById('fc-edit-question').value = card.q;
      document.getElementById('fc-edit-answer').value = card.a;
      document.getElementById('fc-edit-question').focus();
    }}

    function closeFcFullscreenEditor() {{
      fcFullscreenEditing = false;
      document.getElementById('fc-stage').classList.remove('fc-editing');
      document.getElementById('fc-fullscreen-editor').hidden = true;
      document.getElementById('btn-fc-edit').textContent = '✎ Bewerk';
    }}

    function saveFcFullscreenEditor() {{
      if (!queue.length) return;
      const data = readFullscreenEditorForm();
      if (!data.q || !data.a) {{
        alert('Vul minstens een vraag en antwoord in.');
        return;
      }}
      const card = queue[index];
      updateCardContent(card, data);
      saveCards();
      applyFilter();
      closeFcFullscreenEditor();
      renderCard();
      renderList();
      renderWeakList();
      showSaved();
    }}

    function toggleFcFullscreen() {{
      if (fcFullscreen && fcFullscreenEditing) closeFcFullscreenEditor();
      fcFullscreen = !fcFullscreen;
      const stage = document.getElementById('fc-stage');
      stage.classList.toggle('fullscreen', fcFullscreen);
      document.getElementById('fc-fullscreen-progress').setAttribute('aria-hidden', fcFullscreen ? 'false' : 'true');
      document.getElementById('btn-fc-edit').style.display = fcFullscreen && queue.length ? 'inline-block' : 'none';
      document.body.style.overflow = fcFullscreen ? 'hidden' : '';
      document.getElementById('btn-fc-fullscreen').textContent = fcFullscreen ? '✕ Sluit groot scherm' : '⛶ Groot scherm';
      if (fcFullscreen) updateStats();
    }}

    document.getElementById('flashcard').addEventListener('click', flipCard);
    document.getElementById('btn-next').addEventListener('click', nextCard);
    document.getElementById('btn-prev').addEventListener('click', prevCard);
    document.getElementById('btn-easy').addEventListener('click', rateGood);
    document.getElementById('btn-hard').addEventListener('click', rateBad);
    document.getElementById('btn-fc-fullscreen').addEventListener('click', toggleFcFullscreen);
    document.getElementById('btn-fc-edit').addEventListener('click', () => {{
      if (fcFullscreenEditing) closeFcFullscreenEditor();
      else openFcFullscreenEditor();
    }});
    document.getElementById('btn-fc-save-card').addEventListener('click', saveFcFullscreenEditor);
    document.getElementById('btn-fc-cancel-edit').addEventListener('click', closeFcFullscreenEditor);

    document.getElementById('btn-shuffle').addEventListener('click', () => {{
      buildQueue(true);
      index = 0;
      renderCard();
      updateStats();
    }});

    document.getElementById('btn-reset-progress').addEventListener('click', () => {{
      if (confirm('Alle leervoortgang wissen? (Kaarten en foutentelling blijven, maar alles wordt opnieuw geoefend)')) {{
        fcProgress = {{}};
        localStorage.removeItem(STORAGE_FC_PROGRESS);
        localStorage.removeItem(STORAGE_FC);
        weakStudyMode = false;
        buildQueue(true);
        index = 0;
        saveFcProgress();
        renderList();
        renderWeakList();
        renderCard();
        updateWeakStudyButtons();
      }}
    }});

    document.getElementById('btn-study-weak').addEventListener('click', () => {{
      weakStudyMode = true;
      buildQueue(true);
      index = 0;
      renderCard();
      updateStats();
      updateWeakStudyButtons();
      document.getElementById('fc-stage').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});

    document.getElementById('btn-study-all').addEventListener('click', () => {{
      weakStudyMode = false;
      buildQueue(false);
      index = 0;
      renderCard();
      updateStats();
      updateWeakStudyButtons();
    }});

    document.getElementById('btn-edit-current').addEventListener('click', () => {{
      if (!queue.length) return;
      if (fcFullscreen) openFcFullscreenEditor();
      else {{
        openEditorForCard(queue[index].id);
        switchPanel('editor');
      }}
    }});

    function renderList() {{
      const list = document.getElementById('fc-list');
      const items = filteredPool();
      list.innerHTML = items.map(c => {{
        const p = getCardProgress(cardKey(c));
        let cls = '';
        if (p.state === 'mastered') cls = 'done';
        const failTag = p.fails >= FC_WEAK_THRESHOLD ? ` · ${{p.fails}}× fout` : '';
        const confirmTag = p.state === 'confirm' ? ' · bevestigen' : '';
        return `<div class="fc-list-item ${{cls}}" data-id="${{c.id}}">
          <span class="tag">${{escapeHtml(c.section)}}</span>${{escapeHtml(c.q)}}${{failTag}}${{confirmTag}}
        </div>`;
      }}).join('');
      list.querySelectorAll('.fc-list-item').forEach(el => {{
        el.addEventListener('click', () => {{
          const idx = queue.findIndex(c => c.id === el.dataset.id);
          if (idx >= 0) {{
            index = idx;
            renderCard();
            if (listVisible) window.scrollTo({{ top: document.getElementById('fc-wrap').offsetTop - 80, behavior: 'smooth' }});
          }}
        }});
      }});
    }}

    document.getElementById('btn-show-list').addEventListener('click', () => {{
      listVisible = !listVisible;
      document.getElementById('fc-list').style.display = listVisible ? 'grid' : 'none';
      document.getElementById('btn-show-list').textContent = listVisible ? 'Verberg lijst' : 'Toon alle kaarten';
      if (listVisible) renderList();
    }});

    // Editor
    function filteredEditorCards() {{
      let list = editorFilterSection === 'all' ? CARDS : CARDS.filter(c => c.section === editorFilterSection);
      const q = editorSearch.trim().toLowerCase();
      if (q) list = list.filter(c => c.q.toLowerCase().includes(q) || c.a.toLowerCase().includes(q) || c.section.toLowerCase().includes(q));
      return list;
    }}

    function renderEditorList() {{
      const list = document.getElementById('editor-list');
      const items = filteredEditorCards();
      if (!items.length) {{
        list.innerHTML = '<div class="editor-empty">Geen kaarten gevonden.</div>';
        return;
      }}
      list.innerHTML = items.map(c => `
        <button type="button" class="editor-list-item ${{c.id === editingId ? 'active' : ''}}" data-id="${{c.id}}">
          <span class="tag">${{escapeHtml(c.section)}}</span>${{escapeHtml(c.q)}}
        </button>`).join('');
      list.querySelectorAll('.editor-list-item').forEach(el => {{
        el.addEventListener('click', () => openEditorForCard(el.dataset.id));
      }});
    }}

    function openEditorForCard(id) {{
      const card = CARDS.find(c => c.id === id);
      if (!card) return;
      editingId = id;
      document.getElementById('editor-form-empty').style.display = 'none';
      document.getElementById('editor-form-fields').style.display = 'block';
      document.getElementById('editor-form-title').textContent = 'Kaart bewerken';
      document.getElementById('edit-section').value = card.section;
      document.getElementById('edit-question').value = card.q;
      document.getElementById('edit-answer').value = card.a;
      renderEditorList();
    }}

    function readEditorForm() {{
      return {{
        section: document.getElementById('edit-section').value.trim() || 'Eigen kaarten',
        q: document.getElementById('edit-question').value.trim(),
        a: document.getElementById('edit-answer').value.trim(),
      }};
    }}

    function saveEditorCard() {{
      const data = readEditorForm();
      if (!data.q || !data.a) {{
        alert('Vul minstens een vraag en antwoord in.');
        return;
      }}
      if (editingId) {{
        const card = CARDS.find(c => c.id === editingId);
        if (card) updateCardContent(card, data);
      }} else {{
        const card = {{ id: newId(), ...data }};
        CARDS.push(card);
        editingId = card.id;
      }}
      saveCards();
      applyFilter();
      renderEditorList();
      openEditorForCard(editingId);
    }}

    document.getElementById('btn-save-card').addEventListener('click', saveEditorCard);

    document.getElementById('btn-new-card').addEventListener('click', () => {{
      editingId = null;
      document.getElementById('editor-form-empty').style.display = 'none';
      document.getElementById('editor-form-fields').style.display = 'block';
      document.getElementById('editor-form-title').textContent = 'Nieuwe kaart';
      document.getElementById('edit-section').value = editorFilterSection !== 'all' ? editorFilterSection : '';
      document.getElementById('edit-question').value = '';
      document.getElementById('edit-answer').value = '';
      document.getElementById('edit-question').focus();
      renderEditorList();
    }});

    document.getElementById('btn-duplicate-card').addEventListener('click', () => {{
      const data = readEditorForm();
      if (!data.q) return;
      const card = {{ id: newId(), section: data.section, q: data.q + ' (kopie)', a: data.a }};
      CARDS.push(card);
      saveCards();
      applyFilter();
      openEditorForCard(card.id);
    }});

    document.getElementById('btn-delete-card').addEventListener('click', () => {{
      if (!editingId) return;
      if (!confirm('Deze kaart definitief verwijderen?')) return;
      const removed = CARDS.find(c => c.id === editingId);
      CARDS = CARDS.filter(c => c.id !== editingId);
      if (removed) delete fcProgress[cardKey(removed)];
      saveFcProgress();
      editingId = null;
      saveCards();
      applyFilter();
      document.getElementById('editor-form-empty').style.display = 'block';
      document.getElementById('editor-form-fields').style.display = 'none';
      document.getElementById('editor-form-title').textContent = 'Selecteer een kaart';
      renderEditorList();
    }});

    document.getElementById('editor-search').addEventListener('input', e => {{
      editorSearch = e.target.value;
      renderEditorList();
    }});

    document.getElementById('btn-export-cards').addEventListener('click', () => {{
      const blob = new Blob([JSON.stringify(CARDS, null, 2)], {{ type: 'application/json' }});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'life_events_flashcards_backup.json';
      a.click();
      URL.revokeObjectURL(a.href);
    }});

    document.getElementById('import-file').addEventListener('change', e => {{
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {{
        try {{
          const data = JSON.parse(reader.result);
          if (!Array.isArray(data) || !data.length) throw new Error('Leeg');
          CARDS = data.map(c => ({{
            id: c.id || newId(),
            section: c.section || 'Eigen kaarten',
            q: c.q || '',
            a: c.a || '',
          }})).filter(c => c.q && c.a);
          saveCards();
          applyFilter();
          renderEditorList();
          alert('Backup geïmporteerd: ' + CARDS.length + ' kaarten.');
        }} catch (err) {{
          alert('Kon backup niet lezen. Controleer het JSON-bestand.');
        }}
        e.target.value = '';
      }};
      reader.readAsText(file);
    }});

    document.getElementById('btn-reset-cards').addEventListener('click', () => {{
      if (!confirm('Alle kaarten terugzetten naar de originele set? Je eigen wijzigingen gaan verloren.')) return;
      CARDS = JSON.parse(JSON.stringify(DEFAULT_CARDS));
      localStorage.removeItem(STORAGE_CARDS);
      editingId = null;
      saveCards(false);
      applyFilter();
      document.getElementById('editor-form-empty').style.display = 'block';
      document.getElementById('editor-form-fields').style.display = 'none';
      renderEditorList();
      showSaved();
    }});

    document.addEventListener('keydown', e => {{
      if (!document.getElementById('panel-flashcards').classList.contains('active')) return;
      const tag = (e.target && e.target.tagName) || '';
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
      if (e.code === 'Escape' && fcFullscreen) {{
        e.preventDefault();
        if (fcFullscreenEditing) closeFcFullscreenEditor();
        else toggleFcFullscreen();
        return;
      }}
      if (e.code === 'Space') {{ e.preventDefault(); flipCard(); }}
      if (e.code === 'ArrowRight') {{ e.preventDefault(); nextCard(); }}
      if (e.code === 'ArrowLeft') {{ e.preventDefault(); prevCard(); }}
      if (e.code === 'Enter') {{ e.preventDefault(); rateGood(); }}
      if (e.code === 'Backspace') {{ e.preventDefault(); rateBad(); }}
    }});

    // Checklist
    const clState = JSON.parse(localStorage.getItem(STORAGE_CL) || '{{}}');
    document.querySelectorAll('#checklist input').forEach(inp => {{
      if (clState[inp.dataset.id]) inp.checked = true;
      inp.addEventListener('change', () => {{
        clState[inp.dataset.id] = inp.checked;
        localStorage.setItem(STORAGE_CL, JSON.stringify(clState));
      }});
    }});

    // Oefenexamen
    let examSectionFilter = 'all';
    let examSession = null;
    let examHistoryViewId = null;

    function loadExamHistory() {{
      try {{
        const raw = localStorage.getItem(STORAGE_EXAM_HISTORY);
        const parsed = raw ? JSON.parse(raw) : [];
        return Array.isArray(parsed) ? parsed : [];
      }} catch (e) {{ return []; }}
    }}

    function saveExamHistory(list) {{
      localStorage.setItem(STORAGE_EXAM_HISTORY, JSON.stringify(list.slice(0, EXAM_HISTORY_MAX)));
    }}

    function formatExamDate(iso) {{
      const d = new Date(iso);
      return d.toLocaleDateString('nl-BE', {{
        day: 'numeric', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      }});
    }}

    function formatDuration(ms) {{
      if (!ms || ms < 1000) return '< 1 min';
      const m = Math.floor(ms / 60000);
      const s = Math.floor((ms % 60000) / 1000);
      return m ? m + ' min ' + s + ' s' : s + ' s';
    }}

    function getMcBank(section) {{
      if (section === 'all') return [...MC_QUESTIONS];
      return MC_QUESTIONS.filter(q => q.section === section);
    }}

    function shuffleArray(arr) {{
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }}
      return a;
    }}

    function showExamView(view) {{
      document.getElementById('exam-view-start').style.display = view === 'start' ? 'block' : 'none';
      document.getElementById('exam-view-active').style.display = view === 'active' ? 'block' : 'none';
      document.getElementById('exam-view-results').style.display = view === 'results' ? 'block' : 'none';
      document.getElementById('exam-view-history').style.display = view === 'history' ? 'block' : 'none';
    }}

    function renderExamHistory() {{
      const history = loadExamHistory();
      const empty = document.getElementById('exam-recent-empty');
      const recent = document.getElementById('exam-recent-list');
      const sidebar = document.getElementById('exam-history-sidebar');

      if (!history.length) {{
        if (empty) empty.style.display = 'block';
        if (recent) recent.innerHTML = '';
        if (sidebar) sidebar.innerHTML = '<p class="exam-empty" style="padding:0.5rem 0">Geen historiek</p>';
        return;
      }}
      if (empty) empty.style.display = 'none';

      const itemHtml = (h, compact) => `
        <button type="button" class="exam-history-item ${{examHistoryViewId === h.id ? 'active' : ''}}" data-id="${{h.id}}">
          <span>
            <span class="score">${{h.score}}/${{h.total}} (${{h.pct}}%)</span>
            <span class="meta">${{formatExamDate(h.date)}} · ${{h.sectionLabel}} · ${{formatDuration(h.durationMs)}}</span>
          </span>
        </button>`;

      if (recent) {{
        recent.innerHTML = history.slice(0, 5).map(h => itemHtml(h, true)).join('');
        recent.querySelectorAll('.exam-history-item').forEach(btn => {{
          btn.addEventListener('click', () => openExamHistoryDetail(btn.dataset.id));
        }});
      }}
      if (sidebar) {{
        sidebar.innerHTML = history.map(h => itemHtml(h, false)).join('');
        sidebar.querySelectorAll('.exam-history-item').forEach(btn => {{
          btn.addEventListener('click', () => openExamHistoryDetail(btn.dataset.id));
        }});
      }}
    }}

    function openExamHistoryDetail(id) {{
      const h = loadExamHistory().find(x => x.id === id);
      if (!h) return;
      examHistoryViewId = id;
      showExamView('history');
      document.getElementById('exam-history-detail-summary').innerHTML = `
        <div class="exam-score-big">${{h.score}} / ${{h.total}}</div>
        <div class="exam-score-sub">${{h.pct}}% correct · ${{formatExamDate(h.date)}} · ${{h.sectionLabel}} · ${{formatDuration(h.durationMs)}}</div>
      `;
      document.getElementById('exam-history-detail-review').innerHTML = h.answers.map((a, i) => {{
        const cls = a.chosen === a.correct ? 'right' : 'wrong';
        const chosenText = a.chosen != null ? escapeHtml(a.options[a.chosen]) : '<em>Geen antwoord</em>';
        const correctText = escapeHtml(a.options[a.correct]);
        return `<div class="exam-review-item ${{cls}}">
          <strong>Vraag ${{i + 1}}:</strong> ${{escapeHtml(a.q)}}<br>
          <span style="color:var(--muted)">${{escapeHtml(a.section)}}</span><br>
          Jouw antwoord: ${{chosenText}}<br>
          ${{a.chosen !== a.correct ? 'Correct: ' + correctText : '✓ Correct'}}
        </div>`;
      }}).join('');
      renderExamHistory();
    }}

    function shuffleQuestionOptions(q) {{
      const indexed = q.options.map((opt, i) => ({{ opt, i }}));
      const shuffled = shuffleArray(indexed);
      return {{
        ...q,
        options: shuffled.map(x => x.opt),
        correct: shuffled.findIndex(x => x.i === q.correct),
      }};
    }}

    function startExam() {{
      const countSel = document.getElementById('exam-count').value;
      const section = document.getElementById('exam-section-select').value;
      let bank = getMcBank(section);
      if (!bank.length) {{
        alert('Geen vragen beschikbaar voor dit onderwerp.');
        return;
      }}
      bank = shuffleArray(bank);
      const n = countSel === 'all' ? bank.length : Math.min(parseInt(countSel, 10), bank.length);
      const questions = bank.slice(0, n).map(q => shuffleQuestionOptions(q));
      examSession = {{
        startedAt: Date.now(),
        section,
        sectionLabel: section === 'all' ? 'Alle vragen' : section,
        questions,
        answers: new Array(questions.length).fill(null),
        index: 0,
      }};
      showExamView('active');
      renderExamQuestion();
    }}

    function renderExamQuestion() {{
      if (!examSession) return;
      const {{ questions, answers, index }} = examSession;
      const q = questions[index];
      const card = document.getElementById('exam-question-card');
      document.getElementById('exam-progress-text').textContent =
        'Vraag ' + (index + 1) + ' / ' + questions.length +
        ' · ' + answers.filter(a => a !== null).length + ' beantwoord';

      const letters = ['A', 'B', 'C', 'D'];
      card.innerHTML = `
        <div class="exam-q-num">${{escapeHtml(q.section)}}</div>
        <div class="exam-q-text">${{escapeHtml(q.q)}}</div>
        <div class="exam-options">
          ${{q.options.map((opt, i) => `
            <label class="exam-option ${{answers[index] === i ? 'selected' : ''}}">
              <input type="radio" name="exam-opt" value="${{i}}" ${{answers[index] === i ? 'checked' : ''}}>
              <span><strong>${{letters[i]}}.</strong> ${{escapeHtml(opt)}}</span>
            </label>
          `).join('')}}
        </div>
      `;
      card.querySelectorAll('.exam-option').forEach(label => {{
        const input = label.querySelector('input');
        label.addEventListener('click', () => {{
          examSession.answers[index] = parseInt(input.value, 10);
          card.querySelectorAll('.exam-option').forEach(l => l.classList.remove('selected'));
          label.classList.add('selected');
          input.checked = true;
          document.getElementById('exam-progress-text').textContent =
            'Vraag ' + (index + 1) + ' / ' + questions.length +
            ' · ' + examSession.answers.filter(a => a !== null).length + ' beantwoord';
        }});
      }});
      document.getElementById('btn-exam-prev').disabled = index === 0;
      document.getElementById('btn-exam-next').disabled = index === questions.length - 1;
    }}

    function submitExam() {{
      if (!examSession) return;
      const unanswered = examSession.answers.filter(a => a === null).length;
      if (unanswered > 0) {{
        if (!confirm('Je hebt nog ' + unanswered + ' onbeantwoorde vraag/vragen. Toch indienen?')) return;
      }}
      const {{ questions, answers, startedAt, section, sectionLabel }} = examSession;
      let score = 0;
      const answerRecords = questions.map((q, i) => {{
        const chosen = answers[i];
        const correct = q.correct;
        if (chosen === correct) score++;
        return {{
          id: q.id,
          section: q.section,
          q: q.q,
          options: q.options,
          correct,
          chosen,
        }};
      }});
      const total = questions.length;
      const pct = total ? Math.round(score / total * 100) : 0;
      const entry = {{
        id: 'exam_' + Date.now(),
        date: new Date().toISOString(),
        score,
        total,
        pct,
        section,
        sectionLabel,
        durationMs: Date.now() - startedAt,
        answers: answerRecords,
      }};
      const history = loadExamHistory();
      history.unshift(entry);
      saveExamHistory(history);
      examSession = null;
      showExamResults(entry);
      renderExamHistory();
    }}

    function showExamResults(entry) {{
      showExamView('results');
      const emoji = entry.pct >= 80 ? '🎉' : entry.pct >= 60 ? '👍' : '📚';
      document.getElementById('exam-results-summary').innerHTML = `
        <div class="exam-score-big">${{entry.score}} / ${{entry.total}} ${{emoji}}</div>
        <div class="exam-score-sub">${{entry.pct}}% correct · ${{entry.sectionLabel}} · ${{formatDuration(entry.durationMs)}}</div>
        <p style="margin:1rem 0 0;color:var(--muted);font-size:0.9rem">Opgeslagen in je lokale historiek op dit apparaat.</p>
      `;
      document.getElementById('exam-review-list').innerHTML = entry.answers.map((a, i) => {{
        const cls = a.chosen === a.correct ? 'right' : 'wrong';
        const chosenText = a.chosen != null ? escapeHtml(a.options[a.chosen]) : '<em>Geen antwoord</em>';
        const correctText = escapeHtml(a.options[a.correct]);
        return `<div class="exam-review-item ${{cls}}">
          <strong>Vraag ${{i + 1}}:</strong> ${{escapeHtml(a.q)}}<br>
          Jouw antwoord: ${{chosenText}}<br>
          ${{a.chosen !== a.correct ? '<span style="color:var(--danger)">Correct: ' + correctText + '</span>' : '<span style="color:var(--success)">Correct</span>'}}
        </div>`;
      }}).join('');
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    document.getElementById('btn-start-exam').addEventListener('click', startExam);
    document.getElementById('btn-exam-prev').addEventListener('click', () => {{
      if (examSession && examSession.index > 0) {{ examSession.index--; renderExamQuestion(); }}
    }});
    document.getElementById('btn-exam-next').addEventListener('click', () => {{
      if (examSession && examSession.index < examSession.questions.length - 1) {{
        examSession.index++;
        renderExamQuestion();
      }}
    }});
    document.getElementById('btn-exam-submit').addEventListener('click', submitExam);
    document.getElementById('btn-exam-cancel').addEventListener('click', () => {{
      if (examSession && !confirm('Oefenexamen annuleren? Voortgang gaat verloren.')) return;
      examSession = null;
      showExamView('start');
    }});
    document.getElementById('btn-exam-retry').addEventListener('click', () => {{
      showExamView('start');
      document.getElementById('exam-section-select').value = examSectionFilter === 'all' ? 'all' : examSectionFilter;
    }});
    document.getElementById('btn-exam-back-start').addEventListener('click', () => showExamView('start'));
    document.getElementById('btn-exam-back-from-history').addEventListener('click', () => {{
      examHistoryViewId = null;
      showExamView('start');
      renderExamHistory();
    }});

    document.getElementById('btn-clear-exam-history').addEventListener('click', () => {{
      if (!confirm('Alle oefenexamen-resultaten op dit apparaat wissen?')) return;
      localStorage.removeItem(STORAGE_EXAM_HISTORY);
      examHistoryViewId = null;
      renderExamHistory();
      showExamView('start');
    }});

    document.querySelectorAll('#exam-nav .filter-btn[data-exam-section]').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('#exam-nav .filter-btn[data-exam-section]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        examSectionFilter = btn.dataset.examSection;
        document.getElementById('exam-section-select').value = examSectionFilter;
        const n = getMcBank(examSectionFilter).length;
        document.getElementById('exam-bank-count').textContent = n;
      }});
    }});

    document.getElementById('exam-section-select').addEventListener('change', e => {{
      examSectionFilter = e.target.value;
      document.querySelectorAll('#exam-nav .filter-btn[data-exam-section]').forEach(b => {{
        b.classList.toggle('active', b.dataset.examSection === examSectionFilter);
      }});
      document.getElementById('exam-bank-count').textContent = getMcBank(examSectionFilter).length;
    }});

    // Mindmaps (Mermaid)
    async function initMermaid() {{
      const theme = getMermaidTheme();
      if (mermaidApi && mermaidThemeUsed === theme) return mermaidApi;
      const mod = await import('https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs');
      mermaidApi = mod.default;
      mermaidApi.initialize({{
        startOnLoad: false,
        theme: theme,
        securityLevel: 'loose',
        mindmap: {{ padding: 16, useMaxWidth: true }},
      }});
      mermaidThemeUsed = theme;
      return mermaidApi;
    }}

    async function showMindmap(id) {{
      currentMmId = id;
      document.querySelectorAll('.mm-panel').forEach(p => {{
        p.style.display = p.dataset.mmId === id ? 'block' : 'none';
      }});
      document.querySelectorAll('.mm-nav-btn').forEach(b => {{
        b.classList.toggle('active', b.dataset.mmId === id);
      }});
      const panel = document.getElementById('mm-' + id);
      if (!panel || mmRendered.has(id)) return;
      const source = panel.querySelector('.mm-source');
      if (!source) return;
      const wrap = panel.querySelector('.mm-diagram-wrap');
      wrap.innerHTML = '<div class="mm-loading">Mindmap laden…</div>';
      try {{
        const mermaid = await initMermaid();
        const code = source.textContent.trim();
        const uid = 'mm-render-' + id;
        const {{ svg }} = await mermaid.render(uid, code);
        wrap.innerHTML = svg;
        mmRendered.add(id);
      }} catch (err) {{
        console.error(err);
        wrap.innerHTML = '<div class="mm-loading">Kon mindmap niet renderen. Vernieuw de pagina.</div>';
      }}
    }}

    document.querySelectorAll('.mm-nav-btn').forEach(btn => {{
      btn.addEventListener('click', () => showMindmap(btn.dataset.mmId));
    }});

    initTheme();
    document.getElementById('btn-theme-toggle').addEventListener('click', () => {{
      applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
    }});

    rebuildFcNav();
    applyFilter();
    updateStats();
    renderWeakList();
  </script>
</body>
</html>
"""

OUTPUT_PATH.write_text(html, encoding="utf-8")
INDEX_OUTPUT_PATH.write_text(html, encoding="utf-8")
print(f"Created: {OUTPUT_PATH}")
print(f"Created: {INDEX_OUTPUT_PATH}")
print(f"Cards embedded: {len(cards)}")
print(f"MC questions: {len(mc_questions)} ({sum(1 for q in mc_questions if q['section'] == EXAM_SECTION_RECON)} uit 1e zit)")
print(f"Mindmaps: {len(MINDMAPS)}")
print(f"Checklist items: {len(checklist)}")
