"""Read the glossary's pages into one glossary.json the app loads.

    python -m ez_prompt.extract <glossary-dir> <out.json>

Exits non-zero, writing nothing, if any entry is refused.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Keys, in the sheet's order, which is also the flat prompt's order:
# key -> (part, label). The parts are Medium and CTLT's camera, tone, light, texture.
KEYS = {
    "medium": ("medium", "Medium"),
    "format": ("camera", "Format"),
    "lens": ("camera", "Lens"),
    "focus": ("camera", "Focus"),
    "shot-size": ("camera", "Shot Size"),
    "angle": ("camera", "Angle"),
    "composition": ("camera", "Composition"),
    "scene": ("camera", "Scene Format"),
    "color": ("tone", "Color"),
    "mood": ("tone", "Mood"),
    "light": ("light", "Light"),
    "exposure": ("light", "Exposure"),
    "time": ("light", "Time of Day"),
    "atmosphere": ("light", "Atmosphere"),
    "image-texture": ("texture", "Image Texture"),
    "finish": ("texture", "Finish"),
}

# Pages in scope: page -> the key its sections take when SECTIONS names none.
# A page with no default must have every section in SECTIONS or HELD_SECTIONS.
PAGES: dict[str, str | None] = {
    "3d-rendering.md": "medium",
    "animation-styles.md": "medium",
    "illustration-styles.md": "medium",
    "cameras-and-lenses.md": None,
    "angles-and-composition.md": None,
    "lighting.md": "light",
    "film-stocks-and-analog.md": None,
    "color-grading-and-tone.md": "color",
    "textures-and-materials.md": None,
    "weather-and-atmosphere.md": None,
}

# (page, section) -> key
SECTIONS = {
    ("cameras-and-lenses.md", "Film Formats"): "format",
    ("cameras-and-lenses.md", "Historical & Alternative Processes"): "format",
    ("cameras-and-lenses.md", "Focal Length"): "lens",
    ("cameras-and-lenses.md", "Lens Types"): "lens",
    ("cameras-and-lenses.md", "Aperture"): "focus",
    ("angles-and-composition.md", "Camera Angles"): "angle",
    ("angles-and-composition.md", "Shot Size / Framing"): "shot-size",
    ("angles-and-composition.md", "Composition Principles"): "composition",
    ("lighting.md", "Contrast and Exposure Styles"): "exposure",
    ("film-stocks-and-analog.md", "Analog Artifacts"): "image-texture",
    ("textures-and-materials.md", "Surface Quality"): "finish",
    ("weather-and-atmosphere.md", "Time of Day"): "time",
    ("weather-and-atmosphere.md", "Precipitation"): "atmosphere",
    ("weather-and-atmosphere.md", "Atmospheric Effects"): "atmosphere",
    ("weather-and-atmosphere.md", "Mood → Visual Mapping"): "mood",
}

# Sections kept out whole: (page, section) -> reason
STOCK = "a color grade and grain under a brand; Color and Image Texture cover it"
HELD_SECTIONS = {
    ("textures-and-materials.md", "Organic Textures"): "a material, which needs a subject",
    ("textures-and-materials.md", "Synthetic / Manufactured Textures"): (
        "a material, which needs a subject"
    ),
    ("textures-and-materials.md", "Paper & Foil"): "a material, which needs a subject",
    ("film-stocks-and-analog.md", "Color Negative Film"): STOCK,
    ("film-stocks-and-analog.md", "Slide / Reversal Film"): STOCK,
    ("film-stocks-and-analog.md", "Black and White Film"): STOCK,
    ("film-stocks-and-analog.md", "Specialty / Distinctive Film"): STOCK,
}

# A term placed outside its section's key: (page, heading) -> (key, section)
PLACES = {
    ("3d-rendering.md", "Isometric"): ("angle", "Camera Angles"),
    ("3d-rendering.md", "Diorama / Miniature Scene"): ("scene", "Scene Format"),
    ("3d-rendering.md", "Cross-Section / Cutaway"): ("scene", "Scene Format"),
    ("3d-rendering.md", "Exploded View"): ("scene", "Scene Format"),
    ("cameras-and-lenses.md", "Infrared Photography"): ("format", "Film Formats"),
    ("cameras-and-lenses.md", "Prism / Crystal Photography"): ("lens", "Lens Types"),
    ("cameras-and-lenses.md", "Freelensing"): ("lens", "Lens Types"),
    ("cameras-and-lenses.md", "Solarization (Sabattier Effect)"): ("color", "Tonal Treatments"),
    ("lighting.md", "Golden Hour"): ("time", "Time of Day"),
    ("lighting.md", "Blue Hour"): ("time", "Time of Day"),
    ("lighting.md", "Hard Midday Sun"): ("time", "Time of Day"),
    ("lighting.md", "Overcast / Diffused Daylight"): ("time", "Time of Day"),
    ("textures-and-materials.md", "Chrome / Mirror Finish"): ("finish", "Surface Quality"),
    ("textures-and-materials.md", "Brushed Metal"): ("finish", "Surface Quality"),
    ("textures-and-materials.md", "Rust / Patina / Decay"): ("finish", "Surface Quality"),
}

# Terms kept out of glossary.json, with the reason: (page, heading) -> reason
HELD = {
    **{
        ("3d-rendering.md", name): "names a tool, untested"
        for name in [
            "Octane Render",
            "Blender Cycles",
            "Blender Eevee",
            "Unreal Engine",
            "Cinema 4D",
            "V-Ray",
        ]
    },
    **{
        ("3d-rendering.md", name): "names a process, untested"
        for name in [
            "Ray Tracing",
            "Path Tracing",
            "Physically Based Rendering (PBR)",
            "Subsurface Scattering (SSS)",
            "Volumetric Rendering",
            "Ambient Occlusion",
            "Global Illumination",
            "Caustics",
        ]
    },
    **{
        ("animation-styles.md", name): "named franchise style"
        for name in [
            "Studio Ghibli",
            "Pixar / Modern CG Animation",
            "Spider-Verse / Hybrid",
            "Anime-Influenced Western",
        ]
    },
    ("animation-styles.md", "Mecha"): "a subject, not a look",
    ("animation-styles.md", "Motion Graphics"): "shows only in motion",
    ("illustration-styles.md", "Children's Book Illustration"): "a purpose; its look is characters",
    ("illustration-styles.md", "Botanical / Scientific Illustration"): "a subject: specimens",
    ("3d-rendering.md", "Holographic Render"): "a subject: a projected object",
    ("angles-and-composition.md", "Over the Shoulder (OTS)"): "needs two subjects",
    ("angles-and-composition.md", "Rule of Odds"): "a count of subjects",
    ("lighting.md", "Broad Lighting"): "depends on a face and its turn to camera",
    ("lighting.md", "Short Lighting"): "depends on a face and its turn to camera",
    ("cameras-and-lenses.md", "Normal (40-60mm)"): "nothing visible",
    ("cameras-and-lenses.md", "Moderate (f/2.8 - f/5.6)"): "nothing visible",
    ("cameras-and-lenses.md", "Prime Lens"): "nothing visible",
    ("lighting.md", "Daylight (~5,500K)"): "nothing visible",
    ("lighting.md", "Motivated Lighting"): "nothing visible",
    ("weather-and-atmosphere.md", "Early Morning (7-9am)"): "a clock time; dawn covers the look",
    ("weather-and-atmosphere.md", "Afternoon (2-4pm)"): "a clock time; midday covers the look",
    ("weather-and-atmosphere.md", "Deep Night / 3am"): "covered by Night",
    ("cameras-and-lenses.md", "Medium Telephoto (105-200mm)"): "covered by Telephoto",
    ("cameras-and-lenses.md", "Super Telephoto (400mm+)"): "covered by Telephoto",
    ("cameras-and-lenses.md", "Small Aperture (f/16 - f/22)"): "covered by Stopped Down",
    ("lighting.md", "Loop Lighting"): "covered by Rembrandt Lighting",
    ("lighting.md", "Clamshell Lighting"): "covered by Butterfly / Paramount Lighting",
    ("lighting.md", "Diffused Light"): "covered by Soft Light",
    ("lighting.md", "Softbox"): "covered by Soft Light",
    ("lighting.md", "Tent / Wraparound Lighting"): "covered by Soft Light",
    ("lighting.md", "Book Lighting"): "covered by Soft Light",
    ("animation-styles.md", "Flash / Web Animation"): "covered by Vector / Flat Illustration",
    ("illustration-styles.md", "Concept Art"): "covered by Digital Painting",
}


@dataclass
class Scope:
    pages: dict[str, str | None] = field(default_factory=lambda: dict(PAGES))
    sections: dict[tuple[str, str], str] = field(default_factory=lambda: dict(SECTIONS))
    held_sections: dict[tuple[str, str], str] = field(default_factory=lambda: dict(HELD_SECTIONS))
    places: dict[tuple[str, str], tuple[str, str]] = field(default_factory=lambda: dict(PLACES))
    held: dict[tuple[str, str], str] = field(default_factory=lambda: dict(HELD))


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
    "Prompt cues": "cues",
}
EXTRAS = {
    "Associated cameras",
    "Landmark uses",
    "Landmark use",
    "Landmark techniques",
    "Common aspect ratios",
    "Color temperature",
    "Aspect ratio",
    "Aperture blade count",
    "Production specifics",
    "Production specifics (Laika)",
}

# Cues go to the model as written, so a brand or a long phrase is refused.
CUE_MAX_WORDS = 8
BRANDS = re.compile(
    r"\b(?:kodak|fuji(?:film)?|ilford|agfa|cinestill|polaroid|portra|ektar|ektachrome"
    r"|kodachrome|velvia|provia|superia|tri-x|t-max|hp5|fp4|fomapan|lensbaby|hasselblad"
    r"|leica|canon|nikon|sony|iphone|octane|unreal|cinema 4d|c4d|v-ray|blender|pixar"
    r"|ghibli|laika|aardman|henson|muppets?|technicolor)\b",
    re.IGNORECASE,
)

FIELD_LINE = re.compile(r"^\*\*(?P<label>[^*]+)\*\*:\s*(?P<rest>.*)$")


class Refused(Exception):
    pass


@dataclass
class Entry:
    name: str
    section: str
    line: int
    fields: dict[str, list[str]] = field(default_factory=dict)
    extras: dict[str, list[str]] = field(default_factory=dict)
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
        elif line.startswith("#"):
            raise Refused(f"line {number}: a heading level the extract does not read")
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
        else:
            entry.prose.append(f"line {number}: {line.strip()}")

    return title, entries


def joined(lines: list[str] | None) -> str | None:
    return " ".join(lines) if lines else None


def cues(entry: Entry) -> list[str]:
    lines = entry.fields.get("cues")
    if lines is None:
        return []
    found = [cue.strip() for cue in " ".join(lines).split(";")]
    for cue in found:
        if not cue:
            raise Refused(f"line {entry.line}: {entry.name}: empty cue")
        if len(cue.split()) > CUE_MAX_WORDS:
            raise Refused(f"line {entry.line}: {entry.name}: cue over {CUE_MAX_WORDS} words")
        if brand := BRANDS.search(cue):
            raise Refused(f"line {entry.line}: {entry.name}: cue names a brand, '{brand[0]}'")
    return found


def to_term(entry: Entry) -> dict[str, object]:
    if entry.prose:
        raise Refused(f"{entry.name}: text outside a field, {entry.prose[0]}")
    if not entry.fields.get("effect"):
        raise Refused(f"line {entry.line}: {entry.name}: no effect")
    return {
        "id": slug(entry.name),
        "name": entry.name,
        "section": entry.section,
        "what": joined(entry.fields.get("what")),
        "effect": joined(entry.fields.get("effect")),
        "pairs": entry.fields.get("pairs", []),
        "conflicts": entry.fields.get("conflicts", []),
        "example": joined(entry.fields.get("example")),
        "cues": cues(entry),
        "extras": {label: " ".join(lines) for label, lines in entry.extras.items()},
    }


def extract(glossary: Path, scope: Scope | None = None) -> dict[str, object]:
    scope = scope or Scope()
    keys: dict[str, dict[str, object]] = {}
    refusals: list[str] = []
    seen: set[tuple[str, str]] = set()
    seen_sections: set[tuple[str, str]] = set()

    def add(key: str, page: str, term: dict[str, object]) -> None:
        if key not in KEYS:
            refusals.append(f"{page}: unknown key '{key}'")
            return
        part, label = KEYS[key]
        dimension = keys.setdefault(key, {"id": key, "label": label, "part": part, "terms": []})
        terms = dimension["terms"]
        assert isinstance(terms, list)
        if any(t["id"] == term["id"] for t in terms):
            refusals.append(f"{page}: {term['name']}: id '{term['id']}' taken")
        else:
            terms.append(term)

    # Placed terms join a key after its own pages have built it.
    placed_terms: list[tuple[str, str, dict[str, object]]] = []

    for page, default in scope.pages.items():
        try:
            title, entries = parse_page((glossary / page).read_text(encoding="utf-8"))
        except Refused as refusal:
            refusals.append(f"{page}: {refusal}")
            continue
        for entry in entries:
            name_key, section_key = (page, entry.name), (page, entry.section)
            seen.add(name_key)
            seen_sections.add(section_key)
            if name_key in scope.held:
                continue
            if name_key in scope.places:
                key, section = scope.places[name_key]
            elif section_key in scope.held_sections:
                continue
            elif section_key in scope.sections:
                key, section = scope.sections[section_key], entry.section
            elif default is not None:
                key, section = default, entry.section
            else:
                refusals.append(f"{page}: {entry.name}: section '{entry.section}' has no key")
                continue
            if key == "medium":
                section = title
            try:
                term = to_term(entry)
            except Refused as refusal:
                refusals.append(f"{page}: {refusal}")
                continue
            term["section"] = section
            if name_key in scope.places:
                placed_terms.append((key, page, term))
            else:
                add(key, page, term)

    for pending in placed_terms:
        add(*pending)

    for page, name in sorted((set(scope.places) | set(scope.held)) - seen):
        if page in scope.pages:
            refusals.append(f"{page}: '{name}' is placed or held but has no entry")
    for page, section in sorted((set(scope.sections) | set(scope.held_sections)) - seen_sections):
        if page in scope.pages:
            refusals.append(f"{page}: section '{section}' is mapped but has no entry")

    if refusals:
        raise Refused("\n".join(refusals))
    order = {key: index for index, key in enumerate(KEYS)}
    return {"dimensions": sorted(keys.values(), key=lambda d: order[str(d["id"])])}


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
