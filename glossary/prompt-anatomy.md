# Prompt Anatomy & Composition

How to structure a prompt. The order, the weighting, the skeleton that every prompt follows. This is the grammar — the glossary pages are the vocabulary.

---

## The Prompt Skeleton

Every visual prompt fills these slots. Not every slot is needed for every prompt — but knowing the full skeleton lets you add or remove dimensions intentionally.

```
[Subject] + [Medium/Style] + [Camera/Format] + [Lighting] + [Color/Grade] + [Composition/Angle] + [Atmosphere/Weather] + [Mood] + [Quality/Detail]
```

### Slot Definitions

| Slot | What it controls | Example terms |
|------|-----------------|---------------|
| **Subject** | What/who is in the image | "portrait of a woman," "abandoned factory," "plate of pasta" |
| **Medium/Style** | The rendering approach | "oil painting," "anime," "photograph," "3D render," "watercolor" |
| **Camera/Format** | Optical character | "85mm f/1.4," "Hasselblad medium format," "fisheye," "anamorphic" |
| **Lighting** | Light quality and direction | "Rembrandt lighting," "golden hour backlight," "direct flash," "neon" |
| **Color/Grade** | Palette and processing | "Kodak Portra 400," "teal and orange," "desaturated," "monochrome" |
| **Composition/Angle** | Framing and camera position | "rule of thirds," "centered symmetry," "low angle," "overhead flat lay" |
| **Atmosphere/Weather** | Environmental conditions | "rain," "fog," "golden hour," "night," "dusty" |
| **Mood** | Emotional register | "melancholic," "energetic," "intimate," "ominous" |
| **Quality/Detail** | Technical specifications | "highly detailed," "sharp focus," "4K," "film grain" |

### Ordering Principles

1. **Subject first** — the model needs to know WHAT before HOW
2. **Medium/style early** — "oil painting of X" vs "X in oil painting style" produces different results; upfront is stronger
3. **The most important modifier goes closest to the subject** — if lighting is the key differentiator, put it right after the subject
4. **Quality modifiers last** — "highly detailed," "8K," etc. are finishing touches, not structural
5. **Fewer terms = stronger per-term influence** — a 10-word prompt with 3 strong terms beats a 50-word prompt with 15 competing terms

---

## Prompt Length and Weighting

### The 3-Term Minimum Viable Prompt

The simplest effective prompt: **Subject + Style + One Strong Modifier**

> Portrait of an old man, oil painting, Rembrandt lighting

This works because each term is unambiguous and non-conflicting. The model has clear direction on WHAT (portrait of old man), HOW (oil painting), and the KEY MODIFIER (Rembrandt lighting = dramatic side light with shadow triangle).

### The 7-Term Standard Prompt

The workhorse: **Subject + Style + Camera + Lighting + Color + Composition + Mood**

> Portrait of a woman in a red dress, cinematic photograph, 85mm f/1.4 shallow depth of field, Rembrandt side lighting, warm Kodak Portra 400 color grade, rule of thirds composition, intimate and melancholic mood

Each term pulls from a different glossary page. No two terms compete for the same dimension. The result is specific and predictable.

### The 12+ Term Maximum Detail Prompt

For precise control when you know exactly what you want:

> Full body portrait of a woman in a flowing red silk dress, editorial fashion photography, Hasselblad medium format, Rembrandt lighting with hard key from upper left and no fill, warm amber color grade with crushed blacks, shot on Kodak Portra 800 with visible film grain, rule of thirds composition with negative space on left for text, standing in foggy cobblestone alley at blue hour, neon sign reflecting in wet pavement, intimate and cinematic mood, highly detailed

The risk with long prompts: terms compete for influence. If the model can't reconcile everything, it averages, producing something generic. Better to prioritize 5-7 strong terms than dilute with 15.

---

## Common Prompt Failures

### Conflicting Terms

| Prompt fragment | The conflict | What happens |
|----------------|-------------|-------------|
| "high key, crushed blacks" | High key = bright everywhere. Crushed blacks = deep dark shadows. | Model averages to medium contrast — neither high key nor crushed |
| "shallow DOF, everything in focus" | Shallow = narrow focus. Everything sharp = deep focus. | Unpredictable — model picks one or produces muddy compromise |
| "golden hour, blue hour" | Different times, different color temperatures | Gets one or a confused warm-cool mix |
| "minimalist, maximalist" | Literal opposites | Generic middle ground |
| "photorealistic, watercolor" | Photo = accurate rendering. Watercolor = painted medium. | Hybrid that's neither — sometimes interesting, usually muddy |
| "Wes Anderson, gritty realism" | Centered pastels vs raw handheld | Neither aesthetic comes through |

**Rule**: If two terms appear in each other's "Conflicts with" lists in the glossary, don't use them together unless you're deliberately seeking a hybrid.

### Overloaded Prompts

**Symptom**: The output looks "AI-generated" — technically competent but generic, lacking a specific visual identity.

**Cause**: Too many style modifiers competing. The model can't prioritize, so it averages everything into a middle ground.

**Fix**: Remove terms until you have 5-7 non-competing modifiers across different dimensions. Each dimension should have ONE term, not three.

**Bad**: "Rembrandt lighting, butterfly lighting, rim lighting, dramatic side light"
**Good**: "Rembrandt lighting" (one lighting term does the work)

### Redundant Terms

**Symptom**: The output doesn't change when you add more words.

**Cause**: Terms that overlap. "Shallow depth of field, blurred background, bokeh, subject isolation" all describe the same visual effect.

**Fix**: Pick the most specific term. "85mm f/1.4" implies shallow DOF, bokeh, AND subject isolation — one term does the work of four.

### Missing Anchor

**Symptom**: The composition is undefined — the subject floats, the framing is arbitrary.

**Cause**: No composition/angle term. The model defaults to a generic 3/4 view at medium distance.

**Fix**: Always include at least ONE spatial term: "overhead flat lay," "close-up," "wide establishing shot," "low angle," "centered symmetry."

---

## Quality Modifiers

These don't change the subject or style — they adjust the overall rendering quality and detail level. Use sparingly. They're finishing touches, not structural.

### Useful Quality Terms

| Term | What it actually does |
|------|---------------------|
| "highly detailed" | Increases fine detail (pores, texture, material quality) |
| "sharp focus" | Ensures the subject isn't soft (useful when DOF isn't specified) |
| "professional photography" | Pushes toward technically competent, well-lit, well-composed |
| "editorial" | Pushes toward magazine-quality art direction |
| "cinematic" | Wider aspect ratio tendency, dramatic lighting, film-like color |
| "film grain" | Adds analog texture (more specific: "Kodak Tri-X grain" or "Portra 400 grain") |
| "8K" / "4K" | Pushes toward high resolution and detail — diminishing returns past 4K |

### Diminishing Returns

"Highly detailed, ultra-realistic, 8K, HDR, sharp focus, professional, masterpiece" — stacking quality modifiers doesn't stack their effects. One or two strong quality terms work. Five quality terms waste prompt space that could hold a meaningful modifier.

---

## Aspect Ratios as Compositional Choice

The frame shape determines what can exist inside it.

| Ratio | Common use | Compositional effect |
|-------|-----------|---------------------|
| **1:1** (square) | Instagram feed, album cover | Centered subjects, symmetry, no horizontal/vertical bias |
| **4:5** (vertical) | Instagram feed (max height) | Vertical emphasis, more body in portraits, more sky in landscapes |
| **3:2** (horizontal) | 35mm film native, standard photo print | The default. Balanced horizontal. Most "natural" looking |
| **4:3** | Medium format native, TV, older photo | Slightly less wide than 3:2. More vertical breathing room |
| **16:9** (widescreen) | YouTube, presentations, cinematic | Horizontal emphasis. Landscapes, establishing shots, letterbox feeling |
| **2.39:1** (anamorphic) | Cinema widescreen | Ultra-wide. Faces at edges, vast landscapes, cinematic scope |
| **9:16** (vertical video) | TikTok, Stories, Reels | Full vertical. Forces vertical composition — subject stacked, text zones top/bottom |
| **2:3** (vertical) | Pinterest, portrait print | Tall vertical. Fashion (head-to-toe), architecture (floor-to-ceiling) |
| **1.43:1** (IMAX) | IMAX sequences | Nearly square but slightly wide. Immersive, fills peripheral vision. Nolan territory |

---

## References

This page cross-references the entire glossary. Every term mentioned should trace back to its vocabulary page for full definition, pairings, and conflicts.
