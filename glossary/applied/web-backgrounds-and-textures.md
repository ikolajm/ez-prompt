# Web Backgrounds & Textures

Recipes for backgrounds, hero sections, and animated textures for web, app, and presentation design. These entries are motion-ready — each notes whether it works as a still, a loop, or both.

---

## Gradients

### Linear Gradient

**The brief**: Two-tone color transition. The simplest background that still communicates mood.

**The recipe**: Two brand colors transitioning at a subtle angle (135-180 degrees). Add **grain/noise texture** overlay to prevent banding on screens.

**Example prompt**: Linear gradient background, soft transition from deep navy to teal, 135-degree angle, subtle film grain overlay, smooth color transition, dark mode web hero background

**Motion**: Works as still. For animation: slow angle rotation or color shift over time.

**Variations**:
- Sunset gradient (warm → cool: amber → purple) — emotional, editorial
- Brand gradient (primary → secondary brand color) — identity-driven
- Dark mode gradient (near-black → dark navy) — subtle, premium

---

### Mesh Gradient

**The brief**: Multi-point color blending — organic, fluid, modern. The dominant web background trend (2022-present).

**The recipe**: 3-5 color nodes blending into soft organic shapes. Colors from the same warm or cool family avoid mud. The blending is smooth, not hard-edged.

**Example prompt**: Mesh gradient background, organic blending of soft pink, lavender, and pale mint, multiple color nodes creating fluid shapes, smooth transitions, modern web design aesthetic, no hard edges

**Motion**: Excellent for animation — nodes drift slowly, colors shift. 15-30 second loop at slow speed. The organic movement is the appeal.

**Variations**:
- Vibrant mesh (neon pink + electric blue + lime) — bold, Gen Z
- Pastel mesh (blush + cream + sage) — soft, wellness
- Dark mesh (deep purple + navy + charcoal) — premium dark mode

---

### Gradient + Grain

**The brief**: Any gradient with film grain overlay. The grain prevents color banding and adds analog warmth to digital surfaces.

**The recipe**: Base gradient + **film grain texture** at 5-15% opacity. The grain adds subtle noise that makes the gradient feel less "digital." References film-stocks-and-analog.md grain characteristics.

**Example prompt**: Gradient background with visible film grain overlay, warm amber to deep brown transition, organic noise texture preventing banding, analog warmth on digital surface, retro-modern web aesthetic

---

## Animated Blobs & Organic Shapes

### Lava Lamp Blobs

**The brief**: Slow-moving, glossy, translucent organic forms. The classic "living background" for hero sections.

**The recipe**:
- Shape: **metaball/isosurface** — forms that merge and split organically
- Surface: **glossy translucent** — subsurface scattering, slight transparency, catches light
- Color: **2-3 saturated colors** against a dark background. The blobs glow
- Motion: **very slow** — hypnotic, not energetic. 20-60 second loops
- Lighting: **soft ambient** with slight directional — gives the blobs dimension

**Example prompt**: Lava lamp blob animation, three glossy translucent organic forms in vivid coral, purple, and blue, merging and separating slowly against dark background, subsurface scattering glow, soft ambient lighting, hypnotic slow movement, seamless loop, hero section background

**Motion notes**: 0.5-2px movement per frame. Ease-in/out on all motion. Seamless loop essential. Metaball physics for merging behavior.

---

### Morphing Gradient Blobs

**The brief**: Soft-edged color shapes that slowly morph and drift. Less defined than lava lamp — more atmospheric, like colored smoke or aurora.

**The recipe**:
- Shape: **soft gaussian blobs** — no hard edges, no defined surface. Pure color clouds
- Color: **brand palette or analogous** — soft transitions, never jarring
- Motion: **drift and morph** — shapes expand, contract, rotate slowly
- Background: **solid color** that the blobs float over

**Example prompt**: Morphing gradient blob animation, soft pink and blue gaussian shapes drifting and transforming on dark background, no hard edges, atmospheric color smoke, gentle slow morphing, seamless loop, ambient web background

**Motion notes**: Even slower than lava lamp. 30-120 second loops. The subtlety is the point — the viewer should barely notice it's moving.

---

## Particle Systems

### Floating Dust / Bokeh Particles

**The brief**: Soft, out-of-focus particles drifting slowly through the frame. Adds depth and life to any background.

**The recipe**:
- Particles: **small circles or dots** at various sizes, out of focus (bokeh quality)
- Movement: **gentle drift** — upward or lateral, very slow
- Depth: **multiple layers** at different speeds (parallax) — creates 3D depth
- Color: **white/warm on dark BG** or **dark on light BG**
- Opacity: **low** (20-50%) — subtle, atmospheric, not distracting

**Example prompt**: Floating bokeh particles on dark navy background, various sizes of soft out-of-focus circles, warm amber and white, gentle upward drift at multiple depths, parallax layers, atmospheric and subtle, seamless loop, dark mode hero section

---

### Connected Node Network

**The brief**: Points connected by lines — the "data visualization" aesthetic. Tech, SaaS, AI company backgrounds.

**The recipe**:
- Nodes: **small dots** at irregular spacing
- Lines: **thin connections** between nearby nodes — opacity based on distance (closer = more visible)
- Motion: **nodes drift slowly**, connections stretch and break as distance changes
- Color: **monochrome** — white on dark, or brand accent on dark. The simplicity is the aesthetic
- Interaction: ideally **mouse-responsive** — nodes near cursor attract or repel

**Example prompt**: Connected node network background, small white dots connected by thin lines on dark background, nodes drifting slowly, connections forming and breaking based on proximity, tech/SaaS aesthetic, subtle blue accent on nearest nodes, data visualization feel, seamless loop

---

### Confetti / Celebration

**The brief**: Colorful particles falling with gravity. Playful, celebratory, event-driven.

**The recipe**:
- Shapes: **small rectangles, circles, squares** — varied, colorful
- Motion: **falling with gravity + lateral drift + rotation** — each piece tumbles differently
- Color: **bold, multi-color** — brand palette or rainbow
- Density: **moderate** — enough to celebrate, not enough to obscure content

**Example prompt**: Confetti celebration particles, colorful small rectangles and circles falling with gravity and gentle lateral drift, rotation on each piece, brand colors (coral, gold, teal), moderate density, playful and celebratory, against clean white background

---

## Noise & Grain Textures

### Film Grain Overlay

**The brief**: Analog grain applied as a texture layer. Adds warmth and tactile quality to any digital surface.

**The recipe**: **Animated grain** (shifting frame-to-frame, not static) at low opacity (5-15%). Fine grain for subtle warmth, coarse grain for vintage/lo-fi. See film-stocks-and-analog.md for specific grain characters.

**Motion notes**: Grain MUST be animated (each frame slightly different) or it looks like a static texture, not film. Even a 2-frame alternation works.

---

### Halftone / Dot Pattern

**The brief**: Visible dot pattern as graphic texture. Print aesthetic on screen.

**The recipe**: Regular dot grid where dot size represents value (larger dots = darker). From graphic-design-styles.md Ben-Day dots and risograph aesthetics. Works as overlay on photography or as standalone pattern.

**Example prompt**: Halftone dot pattern texture, regular grid of circles varying in size, larger dots in shadow areas, smaller in highlights, graphic print aesthetic, single color on white, Ben-Day dot quality

---

## Hero Section Compositions

### Dark Mode Hero

**The brief**: The premium dark-background hero section. Gradient, subtle particles, glowing accent.

**The recipe**:
- Background: **dark mesh gradient** (near-black → dark navy → dark purple)
- Particles: **floating bokeh** or **subtle node network** at very low opacity
- Accent: **one glowing element** — a gradient orb, a line of light, a subtle lens flare
- Typography: **white or light on dark** — the text lives in the dark space
- Glassmorphism elements optional — frosted glass cards floating over the gradient

**Example prompt**: Dark mode web hero section, deep navy to black mesh gradient background, subtle floating bokeh particles, single soft glowing orb of brand purple in upper right, white headline text, glassmorphism frosted card element, premium tech aesthetic

---

### Light / Airy Hero

**The brief**: Clean, bright, minimal. The wellness/lifestyle/SaaS hero.

**The recipe**:
- Background: **white to soft pastel gradient** + **grain overlay**
- Shapes: **soft organic blobs** in pastel brand colors, very low opacity
- Particles: **none or minimal** — the lightness IS the aesthetic
- Typography: **dark on light** — clean sans-serif
- Mood: **open, breathing, trustworthy**

**Example prompt**: Light airy web hero section, white to pale blush gradient with subtle grain, soft organic pastel shapes at 10% opacity, clean sans-serif dark text, abundant negative space, wellness/lifestyle brand, bright and trustworthy

---

### 3D Abstract Hero

**The brief**: Floating 3D objects (spheres, toruses, abstract shapes) rendered in a clean studio environment. The Dribbble/Behance/SaaS hero style.

**The recipe**:
- Objects: **smooth abstract shapes** — spheres, donuts, rounded cubes, soft-body forms
- Rendering: **Octane or C4D** aesthetic — clean PBR materials, soft lighting, subtle reflections
- Color: **brand palette on shapes** against gradient or solid background
- Materials: **matte, glossy, glass, or iridescent** — mixing 2-3 material types
- Lighting: **soft 3-point** — clean, professional, no dramatic shadows

**Example prompt**: 3D abstract hero section, floating matte and glass spheres and rounded shapes in brand purple and coral, soft studio lighting, Octane render quality, clean gradient background, subtle reflections, modern SaaS web design, C4D aesthetic

---

## References

Cross-references:
- [3D & Rendering](../3d-rendering.md) — Octane, C4D, volumetric, subsurface scattering, procedural
- [Film Stocks](../film-stocks-and-analog.md) — film grain characteristics
- [Graphic Design](../graphic-design-styles.md) — glassmorphism, flat design, neubrutalism
- [Textures & Materials](../textures-and-materials.md) — glossy, matte, translucent, metallic
- [Color Grading](../color-grading-and-tone.md) — analogous, complementary, pastel, monochromatic
- [Music Video & Live Visuals](../music-video-and-live-visuals.md) — generative/audio-reactive, VJ content loops
