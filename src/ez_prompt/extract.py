"""Read the glossary's craft pages into one glossary.json the app loads.

    python -m ez_prompt.extract <glossary-dir> <out.json>

Exits non-zero, writing nothing, if any entry is refused.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Scope: page -> dimension id
PAGES = {
    "cameras-and-lenses.md": "camera",
    "angles-and-composition.md": "angle",
    "lighting.md": "lighting",
    "film-stocks-and-analog.md": "film-stock",
    "color-grading-and-tone.md": "color-grade",
    "textures-and-materials.md": "texture",
    "weather-and-atmosphere.md": "weather",
}

# A section that is its own dimension rather than part of its page's
SECTION_DIMENSIONS = {
    ("weather-and-atmosphere.md", "Mood → Visual Mapping"): ("mood", "Mood"),
}

SKIPPED_SECTIONS = {"References"}

# Field labels -> the key they fill. Every label the pages use is listed, so an
# unknown one is a typo or a new field, and is refused rather than dropped.
FIELDS = {
    "What it is": "what",
    "Visual effect": "effect",
    "Visual": "effect",
    "Visual recipe": "effect",
    "Pairs well with": "pairs",
    "Pairs with": "pairs",
    "Conflicts with": "conflicts",
    "Example combination": "example",
}
EXTRAS = {
    "Associated cameras",
    "Landmark uses",
    "Landmark use",
    "Common aspect ratios",
    "Color temperature",
    "Aspect ratio",
    "Aperture blade count",
}
# A group lends these to each of its bullet terms; any other field on a group is refused.
GROUP_FIELDS = {"pairs", "conflicts"}

FIELD_LINE = re.compile(r"^\*\*(?P<label>[^*]+)\*\*:\s*(?P<rest>.*)$")
BULLET_TERM = re.compile(r"^- \*\*(?P<name>[^*]+)\*\*\s*[—–-]\s*(?P<effect>.+)$")


class Refused(Exception):
    pass


@dataclass
class Entry:
    name: str
    section: str
    line: int
    fields: dict[str, list[str]] = field(default_factory=dict)
    extras: dict[str, list[str]] = field(default_factory=dict)
    bullets: list[tuple[str, str]] = field(default_factory=list)
    prose: list[str] = field(default_factory=list)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_page(text: str) -> tuple[str, list[Entry]]:
    """Split a page into its title and its entries, fields still raw."""
    title = ""
    section = ""
    entries: list[Entry] = []
    entry: Entry | None = None
    target: list[str] | None = None

    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            section = line[3:].strip()
            entry = target = None
        elif line.startswith("### "):
            entry = target = None
            if section not in SKIPPED_SECTIONS:
                entry = Entry(line[4:].strip(), section, number)
                entries.append(entry)
        elif line == "---":
            target = None
        elif entry is None and section not in SKIPPED_SECTIONS and FIELD_LINE.match(line):
            raise Refused(f"line {number}: field outside an entry, under '{section}'")
        elif entry is None or not line:
            continue
        elif match := FIELD_LINE.match(line):
            label, rest = match["label"].strip(), match["rest"].strip()
            if label in FIELDS:
                key = FIELDS[label]
                if key in entry.fields:
                    raise Refused(f"line {number}: {entry.name}: second '{label}'")
                target = entry.fields[key] = []
            elif label in EXTRAS:
                target = entry.extras[label] = []
            else:
                raise Refused(f"line {number}: {entry.name}: unknown field '{label}'")
            if rest:
                target.append(rest)
        elif target is not None:
            target.append(line[2:].strip() if line.startswith("- ") else line.strip())
        elif bullet := BULLET_TERM.match(line):
            entry.bullets.append((bullet["name"].strip(), bullet["effect"].strip()))
        else:
            entry.prose.append(f"line {number}: {line.strip()}")

    return title, entries


def joined(lines: list[str] | None) -> str | None:
    return " ".join(lines) if lines else None


def to_group(entry: Entry) -> tuple[dict[str, object], list[dict[str, object]]]:
    """A heading over bulleted terms: each bullet is a term, the prose its note."""
    stray = set(entry.fields) - GROUP_FIELDS
    if stray or entry.extras:
        raise Refused(f"line {entry.line}: {entry.name}: group has its own fields")
    group_id = slug(entry.name)
    note = " ".join(line.split(": ", 1)[1] for line in entry.prose) or None
    group: dict[str, object] = {
        "id": group_id,
        "name": entry.name,
        "section": entry.section,
        "note": note,
    }
    terms: list[dict[str, object]] = [
        {
            "id": slug(name),
            "name": name,
            "section": entry.section,
            "group": group_id,
            "what": None,
            "effect": effect,
            "pairs": entry.fields.get("pairs", []),
            "conflicts": entry.fields.get("conflicts", []),
            "example": None,
            "extras": {},
        }
        for name, effect in entry.bullets
    ]
    return group, terms


def to_term(entry: Entry) -> dict[str, object]:
    if entry.prose:
        raise Refused(f"{entry.name}: text outside a field, {entry.prose[0]}")
    if not entry.fields.get("effect"):
        raise Refused(f"line {entry.line}: {entry.name}: no effect")
    return {
        "id": slug(entry.name),
        "name": entry.name,
        "section": entry.section,
        "group": None,
        "what": joined(entry.fields.get("what")),
        "effect": joined(entry.fields.get("effect")),
        "pairs": entry.fields.get("pairs", []),
        "conflicts": entry.fields.get("conflicts", []),
        "example": joined(entry.fields.get("example")),
        "extras": {label: " ".join(lines) for label, lines in entry.extras.items()},
    }


def extract(glossary: Path, pages: dict[str, str] = PAGES) -> dict[str, object]:
    dimensions: dict[str, dict[str, list[dict[str, object]] | str]] = {}
    refusals: list[str] = []

    for page, dimension_id in pages.items():
        try:
            title, entries = parse_page((glossary / page).read_text(encoding="utf-8"))
        except Refused as refusal:
            refusals.append(f"{page}: {refusal}")
            continue
        for entry in entries:
            target_id, label = SECTION_DIMENSIONS.get((page, entry.section), (dimension_id, title))
            dimension = dimensions.setdefault(
                target_id,
                {"id": target_id, "label": label, "source": page, "groups": [], "terms": []},
            )
            groups, terms = dimension["groups"], dimension["terms"]
            assert isinstance(groups, list) and isinstance(terms, list)
            try:
                if entry.bullets:
                    group, new = to_group(entry)
                    groups.append(group)
                else:
                    new = [to_term(entry)]
            except Refused as refusal:
                refusals.append(f"{page}: {refusal}")
                continue
            for term in new:
                if any(t["id"] == term["id"] for t in terms):
                    refusals.append(f"{page}: {term['name']}: id '{term['id']}' taken")
                else:
                    terms.append(term)

    if refusals:
        raise Refused("\n".join(refusals))
    return {"dimensions": list(dimensions.values())}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        glossary = extract(Path(argv[0]))
    except Refused as refusal:
        print(f"refused:\n{refusal}", file=sys.stderr)
        return 1
    out = Path(argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(glossary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
