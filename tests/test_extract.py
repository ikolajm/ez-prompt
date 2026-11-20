from pathlib import Path

import pytest

from ez_prompt.extract import Refused, extract

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


def run(tmp_path: Path, text: str) -> dict[str, object]:
    (tmp_path / "page.md").write_text(text, encoding="utf-8")
    return extract(tmp_path, {"page.md": "dim"})


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


@pytest.mark.parametrize(
    ("text", "reason"),
    [
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
