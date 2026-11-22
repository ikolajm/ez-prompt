from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from ez_prompt.extract import Refused, Scope, extract

FULL = """# Lighting

## Natural Light

### Golden Hour

**What it is**: The hour after sunrise.

**Visual effect**: Warm, soft, directional.

**Pairs well with**:
- Backlit subjects — rim light
- 85mm portrait lens

**Conflicts with**:
- Cool/clinical moods

**Example combination**: Golden hour + backlit subject → warm rim light

---

### Midday

**Visual**: Sun overhead.

**Pairs with**: Hard editorial fashion, graphic shadow patterns.

---

## References

### Not a term

Anything here is skipped.
"""

GROUP = """# Textures

## Additional Materials

### Leather (Specific Types)

- **Patent leather** — high-gloss lacquered mirror finish.
- **Suede** — napped, soft, matte.

Each type reads completely differently.

**Pairs well with**: Warm lighting, earth tones.
"""


def bare(pages: dict[str, str | None], **tables: Any) -> Scope:
    empty = Scope(pages=pages, sections={}, held_sections={}, places={}, merged={}, held={})
    return replace(empty, **tables)


def run(tmp_path: Path, text: str) -> dict[str, object]:
    (tmp_path / "page.md").write_text(text, encoding="utf-8")
    return extract(tmp_path, bare({"page.md": "light"}))


def write(tmp_path: Path, pages: dict[str, str]) -> None:
    for name, text in pages.items():
        (tmp_path / name).write_text(text, encoding="utf-8")


def terms(result: dict[str, object]) -> list[dict[str, object]]:
    dimensions = result["dimensions"]
    assert isinstance(dimensions, list)
    found = dimensions[0]["terms"]
    assert isinstance(found, list)
    return found


def test_reads_both_entry_shapes(tmp_path: Path) -> None:
    golden, midday = terms(run(tmp_path, FULL))
    assert golden["id"] == "golden-hour"
    assert golden["section"] == "Natural Light"
    assert golden["pairs"] == ["Backlit subjects — rim light", "85mm portrait lens"]
    assert golden["example"] == "Golden hour + backlit subject → warm rim light"
    assert midday["effect"] == "Sun overhead."
    assert midday["what"] is None
    assert midday["pairs"] == ["Hard editorial fashion, graphic shadow patterns."]


def test_group_bullets_become_terms(tmp_path: Path) -> None:
    result = run(tmp_path, GROUP)
    patent, suede = terms(result)
    assert patent["name"] == "Patent leather"
    assert patent["group"] == "leather-specific-types"
    assert suede["pairs"] == ["Warm lighting, earth tones."]
    dimensions = result["dimensions"]
    assert isinstance(dimensions, list)
    assert dimensions[0]["groups"][0]["note"] == "Each type reads completely differently."


SUBS = """# Animation

### Anime Sub-Styles

#### Shoujo

**Visual effect**: Sparkling eyes.

**Prompt cues**: large sparkling eyes; pastel palette

#### Seinen

**Visual effect**: Grounded proportions.
"""


def test_sub_terms_become_a_group(tmp_path: Path) -> None:
    result = run(tmp_path, SUBS)
    shoujo, seinen = terms(result)
    assert shoujo["group"] == seinen["group"] == "anime-sub-styles"
    assert shoujo["cues"] == ["large sparkling eyes", "pastel palette"]
    assert seinen["cues"] == []
    dimensions = result["dimensions"]
    assert isinstance(dimensions, list)
    assert dimensions[0]["groups"][0]["id"] == "anime-sub-styles"


STYLE = (
    "# 3D\n## Styles\n### Low Poly\n**Visual effect**: Facets.\n"
    "### Diorama\n**Visual effect**: A tiny world.\n"
    "### Octane\n**Visual effect**: Glossy.\n"
)
ANGLES = (
    "# Angles\n## Camera Angles\n### Low Angle\n**Visual effect**: Looking up.\n"
    "## Shot Size\n### Close-Up\n**Visual effect**: A face.\n"
    "### Tight Close-Up\n**Visual effect**: A tighter face.\n"
    "## Materials\n### Wood\n**Visual effect**: Grain.\n"
)


def test_keys_places_holds_and_merges(tmp_path: Path) -> None:
    write(tmp_path, {"style.md": STYLE, "angles.md": ANGLES})
    result = extract(
        tmp_path,
        bare(
            {"angles.md": None, "style.md": "medium"},
            sections={
                ("angles.md", "Camera Angles"): "angle",
                ("angles.md", "Shot Size"): "shot-size",
            },
            held_sections={("angles.md", "Materials"): "a material"},
            places={("style.md", "Diorama"): ("angle", "Camera Angles")},
            held={("style.md", "Octane"): "names a tool"},
            merged={("angles.md", "Tight Close-Up"): ("angles.md", "Close-Up")},
        ),
    )
    dimensions = result["dimensions"]
    assert isinstance(dimensions, list)
    medium, shot, angle = dimensions
    assert (medium["id"], medium["part"], medium["label"]) == ("medium", "medium", "Medium")
    assert [(t["name"], t["section"]) for t in medium["terms"]] == [("Low Poly", "3D")]
    assert [(t["name"], t["covers"]) for t in shot["terms"]] == [("Close-Up", ["Tight Close-Up"])]
    assert (angle["part"], angle["source"]) == ("camera", "angles.md")
    assert [(t["name"], t["section"]) for t in angle["terms"]] == [
        ("Low Angle", "Camera Angles"),
        ("Diorama", "Camera Angles"),
    ]


ONE = "# P\n## S\n### T\n**Visual effect**: x\n### U\n**Visual effect**: y\n"


@pytest.mark.parametrize(
    ("pages", "tables", "reason"),
    [
        ({"page.md": "light"}, {"places": {("page.md", "Gone"): ("angle", "S")}}, "has no entry"),
        ({"page.md": "light"}, {"held": {("page.md", "Gone"): "a tool"}}, "has no entry"),
        (
            {"page.md": "light"},
            {"merged": {("page.md", "Gone"): ("page.md", "T")}},
            "has no entry",
        ),
        ({"page.md": "light"}, {"sections": {("page.md", "Gone"): "light"}}, "mapped but"),
        ({"page.md": None}, {}, "section 'S' has no key"),
        ({"page.md": "nowhere"}, {}, "unknown key"),
        (
            {"page.md": "light"},
            {
                "held": {("page.md", "T"): "a tool"},
                "merged": {("page.md", "U"): ("page.md", "T")},
            },
            "which is not built",
        ),
    ],
)
def test_refuses_a_scope_that_misses(
    tmp_path: Path, pages: dict[str, str | None], tables: dict[str, Any], reason: str
) -> None:
    write(tmp_path, {"page.md": ONE})
    with pytest.raises(Refused, match=reason):
        extract(tmp_path, bare(pages, **tables))


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("# P\n#### Orphan\n**Visual effect**: x\n", "sub-term outside an entry"),
        ("# P\n## S\n### T\n**Visual effect**: x\n**Prompt cues**: a; ; b\n", "empty cue"),
        (
            "# P\n## S\n### T\n**Visual effect**: x\n"
            "**Prompt cues**: one two three four five six seven eight nine\n",
            "over 8 words",
        ),
        ("# P\n## S\n### T\n**Visual effect**: x\n**Prompt cues**: warm Portra tones\n", "brand"),
        ("# P\n## S\n### T\n**Visual effect**: x\n**Prompt cues**: tri-x grain\n", "brand"),
        ("# P\n## S\n### T\n**What it is**: x\n", "no effect"),
        ("# P\n## S\n### T\n**Visual effect**: x\n**Pair with**: y\n", "unknown field"),
        ("# P\n## S\n### T\n**Visual effect**: x\n**Visual**: y\n", "second"),
        ("# P\n## S\n### T\nA loose line.\n\n**Visual effect**: x\n", "text outside a field"),
        ("# P\n## S\n### T\n**Visual effect**: x\n---\n### T\n**Visual effect**: y\n", "taken"),
        ("# P\n## S\n### G\n- **A** — a\n**Visual effect**: x\n", "group has its own fields"),
        ("# P\n## Bokeh\nIntro prose.\n**Visual effect**: x\n", "field outside an entry"),
    ],
)
def test_refuses(tmp_path: Path, text: str, reason: str) -> None:
    with pytest.raises(Refused, match=reason):
        run(tmp_path, text)
