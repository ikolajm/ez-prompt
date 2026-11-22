"""Add a Prompt cues field to the end of named glossary entries.

    python -m ez_prompt.cues <glossary-dir> <cues.json> [--write]

cues.json maps page -> heading -> one cue line, cues separated by semicolons.
Without --write it reports where each line would go. It refuses a heading it
cannot find or finds twice, and an entry that already has cues, and then writes
nothing at all.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ez_prompt.extract import Refused


def insert(glossary: Path, plan: dict[str, dict[str, str]]) -> dict[Path, bytes]:
    """Return each page's new bytes, or raise listing every refusal."""
    out: dict[Path, bytes] = {}
    refusals: list[str] = []
    for page, entries in plan.items():
        path = glossary / page
        raw = path.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        lines = raw.decode("utf-8").split(newline)
        for heading, cue in entries.items():
            headings = (f"### {heading}", f"#### {heading}")
            starts = [i for i, line in enumerate(lines) if line in headings]
            if len(starts) != 1:
                refusals.append(f"{page}: '{heading}' found {len(starts)} times")
                continue
            start = starts[0]
            end = start + 1
            while end < len(lines) and lines[end] != "---" and not lines[end].startswith("#"):
                end += 1
            if any(line.startswith("**Prompt cues**") for line in lines[start:end]):
                refusals.append(f"{page}: '{heading}' already has cues")
                continue
            last = end - 1
            while last > start and not lines[last].strip():
                last -= 1
            lines[last + 1 : last + 1] = ["", f"**Prompt cues**: {cue}"]
        out[path] = newline.join(lines).encode("utf-8")
    if refusals:
        raise Refused("\n".join(refusals))
    return out


def main(argv: list[str]) -> int:
    write = "--write" in argv
    args = [arg for arg in argv if arg != "--write"]
    if len(args) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    plan = json.loads(Path(args[1]).read_text(encoding="utf-8"))
    try:
        pages = insert(Path(args[0]), plan)
    except Refused as refusal:
        print(f"refused, nothing written:\n{refusal}", file=sys.stderr)
        return 1
    if write:
        for path, data in pages.items():
            path.write_bytes(data)
    count = sum(len(entries) for entries in plan.values())
    print(f"{'wrote' if write else 'would write'} cues for {count} entries in {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
