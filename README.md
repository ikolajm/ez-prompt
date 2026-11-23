# ez-prompt

A glossary of camera, tone, light and texture terms that turns a chosen look into an image prompt, in words tested on the image models themselves.

Live at [ikolajm.github.io/ez-prompt](https://ikolajm.github.io/ez-prompt/).

## What it does

### The glossary

Terms are grouped into the medium and four parts of a picture a prompt can describe: camera, tone, light and texture. Each part is split into smaller choices, so a camera angle and a shot size are picked separately. Opening a term shows its entry: what it looks like, and often what it is, what it pairs well with and what it conflicts with.

### The spec sheet

Checking a term adds it to a sheet beside the glossary, grouped the same way. Most choices hold one term, and a new pick replaces the old one; light, composition and image texture stack.

### Copying it out

The sheet copies as a readable list of each choice and its term, or as one comma-joined prompt for an image model. The prompt carries each term's cues, short phrases describing what it looks like, in place of its name. The subject is yours to add, wherever it fits: the app sets the look, not the scene.

## What the models read

The cues come from test rounds on two open image models, Z-Image Turbo and MOSS-Image, run locally in ComfyUI, with one subject and one fixed seed per model in each round. The images were compared by eye, not scored.

Shorthand, brand names and lens specs failed: ECU was ignored, Kodak Tri-X 400 stayed in color and came back as a logo on the scene, and "85mm f/1.4" moved the subject rather than the focus. Described by what they look like, the same picks worked. So a cue says what is visible, states its effect outright, and never names gear: "seen from slightly below" came out at eye level, and three-point lighting by name put a light stand in the frame.

## Running it

You need Python 3.12 or later, and Node 20.19 or 22.12 or later.

From the repository root, in a Python environment of your choice:

```
python -m pip install -e ".[dev]"
cd web
npm install
npm run dev
```

The app is at `http://localhost:5173/ez-prompt/`. It reads `web/public/glossary.json` in the browser, so it needs no server and no model.

## The glossary's source

The terms live as pages in `glossary/`, one entry per `###` heading, with fields such as `**Visual effect**:` and `**Prompt cues**:`, cues separated by semicolons. `src/ez_prompt/extract.py` maps the pages' sections to the app's choices, holds out terms that do not belong in it, each with its reason, and writes `web/public/glossary.json`:

```
python -m ez_prompt.extract glossary web/public/glossary.json
```

The extract writes nothing if any entry is refused, so nothing is dropped unseen. It refuses, among others, a term with no visual effect, a field it does not know, text outside a field, and a cue that is empty, runs past eight words or names a brand.

## Checks

```
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pytest
cd web
npm run build
```

The build type-checks `glossary.json` against the types the app reads it through. A push to `main` runs the same checks, fails if the committed `glossary.json` differs from what the extract writes, and deploys to GitHub Pages.
