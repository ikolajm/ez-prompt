import json
from pathlib import Path

import pytest

from ez_prompt.cues import insert, main
from ez_prompt.extract import Refused

PAGE = (
    "# P\r\n## S\r\n### Alpha\r\n**Visual effect**: a.\r\n\r\n---\r\n\r\n"
    "### Beta\r\n**Visual effect**: b.\r\n\r\n**Prompt cues**: old\r\n"
)


def test_inserts_after_the_last_field_and_keeps_crlf(tmp_path: Path) -> None:
    (tmp_path / "p.md").write_bytes(PAGE.encode("utf-8"))
    out = insert(tmp_path, {"p.md": {"Alpha": "one; two"}})
    text = out[tmp_path / "p.md"].decode("utf-8")
    assert "### Alpha\r\n**Visual effect**: a.\r\n\r\n**Prompt cues**: one; two\r\n\r\n---" in text
    assert text.count("\n") == text.count("\r\n")


@pytest.mark.parametrize(
    ("heading", "reason"),
    [("Gone", "found 0 times"), ("Beta", "already has cues")],
)
def test_refuses(tmp_path: Path, heading: str, reason: str) -> None:
    (tmp_path / "p.md").write_bytes(PAGE.encode("utf-8"))
    with pytest.raises(Refused, match=reason):
        insert(tmp_path, {"p.md": {heading: "x"}})


def test_refuses_a_heading_given_twice(tmp_path: Path) -> None:
    twice = "# P\n### A\n**Visual effect**: a.\n### A\n**Visual effect**: b.\n"
    (tmp_path / "p.md").write_text(twice)
    with pytest.raises(Refused, match="found 2 times"):
        insert(tmp_path, {"p.md": {"A": "x"}})


def test_one_refusal_writes_nothing(tmp_path: Path) -> None:
    (tmp_path / "p.md").write_bytes(PAGE.encode("utf-8"))
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"p.md": {"Alpha": "one", "Gone": "two"}}))
    assert main([str(tmp_path), str(plan), "--write"]) == 1
    assert (tmp_path / "p.md").read_bytes() == PAGE.encode("utf-8")
