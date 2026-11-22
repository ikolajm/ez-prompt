# 3D & Rendering

How three-dimensional scenes are constructed and translated into images. In prompt composition, referencing a render engine, technique, or style invokes the specific visual qualities of that pipeline — from photorealistic to stylized, from wireframe to fully shaded.

---

## Render Engines

The software that computes the final image. Each engine has a distinct visual signature even when rendering the same scene.

### Octane Render

**What it is**: GPU-accelerated, unbiased path tracer by OTOY. Popular in motion graphics, product visualization, and art. Known for speed and visual quality.

**Visual effect**: Clean, physically accurate lighting with a distinctive "look" — slightly warm, beautiful volumetrics, excellent glass and SSS rendering. The default Octane image has a polished, cinematic quality. Very popular in the Instagram/Behance 3D art community, creating a recognizable "Octane look."

**Pairs well with**:
- Product visualization — clean, accurate materials
- Abstract 3D art — the community aesthetic leans here
- Volumetric lighting — Octane handles god rays and fog beautifully
- Glass/translucent materials — a known strength
- HDR environment lighting — realistic reflections and ambient light

**Conflicts with**:
- Stylized/non-photorealistic work — Octane defaults to realism
- Retro/lo-fi 3D — too polished
- Hand-drawn/illustrated aesthetic — too clean

**Example combination**: Octane render + glass object + volumetric fog + warm key light + dark background → clean caustics through glass, volumetric rays visible in fog, physically accurate reflections, polished art-station quality

---

### Blender Cycles

**What it is**: Open-source path tracing render engine built into Blender. Physically based, supports CPU and GPU rendering. The most accessible professional render engine.

**Visual effect**: Physically accurate but with a slightly different character than Octane — default output can lean a bit cooler and more neutral. Cycles' look depends heavily on the artist's material and lighting setup. Less of a built-in "look" than Octane — more of a blank canvas.

**Pairs well with**:
- Any 3D style — Cycles is versatile, not opinionated
- Open-source/indie projects — Blender's ecosystem
- Photorealistic architectural visualization
- Stylized work with NPR node setups — Blender's shader nodes allow cel-shaded and painterly effects

**Conflicts with**:
- Real-time rendering — Cycles is offline, not interactive
- A specific "engine look" — Cycles doesn't have one the way Octane does

---

### Blender Eevee

**What it is**: Blender's real-time render engine. Rasterization-based, not path tracing. Fast previews and final renders at the cost of some physical accuracy.

**Visual effect**: Slightly less realistic than Cycles — shadows are approximated (screen-space), reflections use probes rather than true ray tracing, and light bouncing is limited. But it's fast and produces good-looking results with a slightly "game engine" quality. Good for stylized work where perfect physical accuracy isn't needed.

**Pairs well with**:
- Stylized/non-photorealistic renders — the approximations matter less
- Motion graphics — speed enables animation iteration
- Toon/cel-shaded styles — Eevee handles flat shading well
- Quick concept renders — speed over perfection

**Conflicts with**:
- Photorealistic accuracy — Cycles/Octane do this better
- Complex glass/caustics — Eevee can't compute them accurately
- Precise indirect lighting — limited light bouncing

---

### Unreal Engine

**What it is**: Epic Games' real-time 3D engine. Originally a game engine, now widely used for film pre-visualization, virtual production (LED wall stages), architectural visualization, and cinematic renders. Lumen (global illumination) and Nanite (mesh virtualization) have pushed real-time quality toward offline render levels.

**Visual effect**: High-fidelity real-time rendering. The Unreal "look" is cinematic and polished — excellent volumetric lighting, lens effects (bloom, chromatic aberration, depth of field), and atmosphere. Post-processing is aggressive by default: lens flares, bloom, film grain, vignetting. The output looks like a high-end game cutscene or virtual production shot.

**Pairs well with**:
- Cinematic/virtual production aesthetic — this is what LED wall stages use
- Architectural visualization — real-time walkthroughs
- Photorealistic environments — landscapes, interiors, cityscapes
- Atmospheric effects — fog, volumetric light, particle systems

**Conflicts with**:
- Stylized/minimal rendering — Unreal defaults to cinematic bombast
- Simple/clean output — the default post-processing is heavy
- Hand-crafted/artisanal quality — Unreal is industrial-scale

---

### Cinema 4D

**What it is**: Maxon's 3D application, widely used in motion graphics and advertising. Integrated Redshift renderer (GPU path tracer). Known for ease of use and polished output.

**Visual effect**: Clean, commercial, motion-graphics-friendly. The C4D aesthetic is associated with smooth surfaces, satisfying physics simulations, abstract compositions, and advertising polish. The "daily render" Instagram culture runs heavily on C4D.

**Pairs well with**:
- Motion graphics — the industry standard tool
- Abstract 3D art — smooth shapes, satisfying physics, clean materials
- Product visualization — polished, commercial quality
- Advertising/commercial — the tool of ad agencies
- Smooth/satisfying animations — soft body, cloth, particle sims

**Conflicts with**:
- Gritty/imperfect aesthetic — C4D output is too clean
- Game development — not a game engine
- Raw/unpolished looks — the tool encourages polish

---

### V-Ray

**What it is**: Chaos Group's render engine. Industry standard for architectural visualization, product rendering, and VFX. Biased and unbiased modes. Plugins for Maya, 3ds Max, SketchUp, Rhino.

**Visual effect**: The benchmark for architectural visualization. V-Ray's default output is clean, accurate, and commercially neutral — it renders what's there without imposing a look. Excellent interior lighting (radiosity, caustics through glass, natural light simulation). The "architect's rendering" look is often V-Ray.

**Pairs well with**:
- Architectural visualization — THE standard
- Interior design rendering — natural light through windows, material accuracy
- Product photography replacement — studio-quality renders
- Photorealism — V-Ray's core competency

**Conflicts with**:
- Stylized/artistic rendering — too accurate for deliberate distortion
- Real-time — V-Ray is offline rendering
- Abstract art — too grounded in physical accuracy

---

## Rendering Techniques

### Ray Tracing

**What it is**: Rendering technique that traces the path of light rays from the camera through each pixel, calculating intersections with objects and simulating reflection, refraction, and shadow. Computationally expensive, physically accurate.

**Visual effect**: Realistic reflections (mirrors reflect accurately, curved surfaces distort correctly), accurate shadows (soft shadows from area lights, sharp from point lights), correct refraction through glass and water. The "ground truth" of rendering — what things actually look like when light behaves correctly.

**Pairs well with**:
- Photorealistic rendering — the purpose of ray tracing
- Reflective/glass materials — accurate refraction and reflection
- Complex lighting — multiple light sources, indirect illumination
- Product visualization — materials look correct

**Conflicts with**:
- Stylized rendering — ray tracing is about accuracy, not style
- Real-time (historically) — now possible with RTX hardware but still costly
- Deliberately "wrong" light behavior — ray tracing corrects what stylization requires

---

### Path Tracing

**What it is**: An extension of ray tracing that simulates light bouncing multiple times through a scene — each ray splits and bounces, accumulating color from every surface it touches. The most physically accurate rendering method. Produces global illumination (light bouncing between surfaces, color bleeding).

**Visual effect**: The most realistic light behavior possible in a render. Color bleeds between surfaces (a red wall tints nearby white objects pink). Soft, natural shadows. Accurate caustics (light focused through glass). The image is indistinguishable from a photograph when materials and geometry are accurate.

**Pairs well with**:
- Maximum photorealism — the gold standard
- Interior scenes — light bouncing between walls is critical for interiors
- Translucent materials — subsurface scattering, caustics
- Film VFX — integrating CG with live action requires physical accuracy

**Conflicts with**:
- Speed — path tracing is slow, especially for complex scenes
- Stylized/non-photorealistic — too accurate
- Noise — undersampled path tracing produces visible noise/grain

---

### Physically Based Rendering (PBR)

**What it is**: A material and lighting system based on real-world optics — energy conservation (a surface can't reflect more light than it receives), microfacet theory (surfaces are rough at microscopic scale), and the Fresnel effect (everything is reflective at glancing angles). Now the standard in games and film.

**Visual effect**: Materials look "right" because they follow real-world rules. Metals reflect their own color. Rough surfaces scatter light broadly. Smooth surfaces produce sharp reflections. Everything has some reflection at grazing angles (even concrete). The difference from older rendering: PBR materials look correct in ANY lighting condition, not just the one they were built for.

**Pairs well with**:
- Modern game engines (Unreal, Unity) — PBR is the default
- Photorealistic rendering — the material model is physically grounded
- Product visualization — materials match real-world counterparts
- Any lighting condition — PBR materials respond correctly everywhere

**Conflicts with**:
- Deliberately unrealistic materials — PBR enforces physics
- Retro/lo-fi 3D — older games didn't use PBR
- Flat/toon shading — PBR is about realistic light response

---

### Subsurface Scattering (SSS)

**What it is**: Light enters a translucent material, bounces around internally, and exits at a different point than where it entered. Human skin gets ~94% of its appearance from SSS — only ~6% is direct surface reflection.

**Visual effect**: Soft, warm internal glow in translucent materials. Skin looks alive rather than plastic. Backlit ears glow red-orange. Thin marble glows. Wax transmits warm light. Milk appears opaque but luminous. Leaves glow green when backlit. Without SSS, skin and organic materials look like painted plastic.

**Pairs well with**:
- Skin/character rendering — essential for believable skin
- Backlit subjects — SSS is most visible when light passes through the material
- Wax, marble, jade, milk — classic SSS materials
- Close-up/portrait rendering — the viewer is close enough to see the effect
- Warm lighting — the internal scattering often reads warm

**Conflicts with**:
- Opaque/metallic surfaces — metals don't exhibit SSS
- Hard/graphic rendering styles — SSS is soft and subtle
- Distance shots — the effect is invisible from far away

---

## Rendering Styles

### Photorealistic

**What it is**: Rendering that aims to be indistinguishable from a photograph. Accurate materials, physically correct lighting, real-world scale and proportion.

**Visual effect**: Looks real. The viewer shouldn't be able to tell it's CG. This requires accurate PBR materials, ray/path traced lighting, correct camera simulation (depth of field, exposure, lens distortion), and photographic imperfections (grain, chromatic aberration, slight motion blur).

**Pairs well with**:
- Architectural visualization — clients need to see the building before it's built
- Product rendering — replacing expensive photo shoots
- VFX integration — CG elements must match live action
- Camera simulation — depth of field, lens effects, film grain make it believable

**Conflicts with**:
- Stylized art — photorealism is deliberately not stylized
- Low-poly, toon, or abstract work — opposite intent
- Speed — photorealism requires computational time

**Prompt cues**: photorealistic 3D render; physically accurate light and reflections; flawless clean surfaces; soft accurate contact shadows

---

### Clay Render

**What it is**: A render with a uniform matte gray material applied to everything — no textures, no color, just form and light. Used to evaluate shape, composition, and lighting without the distraction of materials.

**Visual effect**: Sculptural, minimal, focused entirely on form. Every object looks like a clay maquette. Light and shadow define shape without any material complexity. Reads as clean, architectural, and study-like.

**Pairs well with**:
- Architectural form studies — shape without materiality
- 3D sculpture/character modeling — evaluating form
- Minimal/clean aesthetic — the reduction is the point
- Soft/even lighting — soft light on clay = gentle, sculptural
- Product design — shape evaluation before material application

**Conflicts with**:
- Material-dependent subjects — no texture or color information
- Realistic rendering — clay render is an abstraction
- Vivid/colorful palettes — everything is gray

**Example combination**: Clay render + soft directional light + architectural model + ambient occlusion → pure form study, every surface matte gray, shadows defining depth and overlap, clean and sculptural

**Prompt cues**: 3D clay render; uniform matte grey material; untextured sculpted forms; soft shadows in every crevice

---

### Cel-Shaded / Toon

**What it is**: Non-photorealistic rendering that mimics hand-drawn or cartoon aesthetics. Lighting is quantized into flat color bands (lit/shadow/highlight) instead of smooth gradients. Black outlines around objects. Named after animation cels.

**Visual effect**: Flat, graphic, cartoon-like. Hard shadow edges instead of soft gradients. Bold outlines. Looks drawn or painted rather than rendered. The 3D geometry provides form and movement while the shading removes photorealistic complexity. Notable examples: Wind Waker, Okami, Spider-Verse.

**Pairs well with**:
- Stylized/cartoon characters — the core use case
- Bold color palettes — flat shading needs strong color choices
- Graphic compositions — the flatness suits graphic design
- Animation — the style was designed for moving images
- Comics/manga aesthetic — outlines + flat color = comic book

**Conflicts with**:
- Photorealism — the opposite approach
- Subtle tonal gradation — cel-shading eliminates gradients
- Realistic materials — everything is flat color

**Example combination**: Cel-shaded + bold primary colors + black outlines + dynamic pose → comic book/anime aesthetic, flat color bands, hard shadow edges, graphic energy

**Prompt cues**: cel-shaded 3D render; flat color with hard-edged shadows; bold black outlines

---

### Low Poly

**What it is**: 3D models built with deliberately minimal polygon counts. Originated from hardware limitations of 1990s game consoles, revived as a conscious aesthetic choice around 2013.

**Visual effect**: Geometric, faceted, simplified. Objects are reduced to essential forms — a tree becomes a cluster of triangles, a face becomes angular planes. The visible facets catch light differently, creating a crystalline/gem-like quality. Reads as stylized, retro, indie-game, or deliberately abstract.

**Pairs well with**:
- Flat/pastel colors — low poly + soft color = the indie game look
- Soft lighting — gentle light across faceted surfaces creates pleasant gradients
- Landscape/environment scenes — low poly nature is a genre unto itself
- Isometric camera — low poly + isometric = miniature world
- Nostalgia/retro gaming — the early 3D callback

**Conflicts with**:
- Photorealism — not enough geometry for realistic surfaces
- Organic/smooth forms — the facets fight smoothness
- High-detail/macro — low poly has no fine detail to zoom into

**Example combination**: Low poly landscape + soft pastel colors + isometric camera + warm lighting → miniature geometric world, faceted trees and mountains, soft gradients across flat surfaces, cozy indie aesthetic

**Prompt cues**: low-poly 3D render; flat-shaded triangular facets; simple geometric forms; soft light gradients across facets

---

### Wireframe

**What it is**: Only edges and vertices rendered — no surfaces, no fills, no shading. The structural skeleton of a 3D model, showing every polygon edge as a line.

**Visual effect**: Technical, skeletal, transparent. You see through objects to the geometry behind them. Reads as blueprint, technical, deconstructed, or digital/matrix-like. The complexity of the wireframe reveals the density of the mesh.

**Pairs well with**:
- Technical/engineering aesthetic — wireframe is a design tool
- Digital/matrix/cyberpunk themes — the geometry of virtual reality
- Overlay on solid renders — wireframe + photorealistic = "making of" look
- Dark backgrounds — bright wireframe lines on black
- Neon/glowing lines — wireframe as light sculpture

**Conflicts with**:
- Material/texture emphasis — wireframe has no surfaces
- Photorealism — wireframe is an abstraction
- Solid/heavy visual weight — wireframe is transparent and skeletal

**Prompt cues**: 3D wireframe render; visible polygon mesh lines; transparent see-through geometry

---

### Isometric

**What it is**: Parallel projection where the three coordinate axes appear equally foreshortened — no vanishing points, no perspective convergence. Objects maintain their size regardless of distance. The camera angle is typically ~30 degrees from horizontal.

**Visual effect**: Clean, diagrammatic, game-like. Everything is readable without perspective distortion. The lack of vanishing points creates a "miniature world" quality. Depth is implied through position (higher = farther) rather than size difference. Reads as game (Sim City, Diablo), architectural diagram, or technical illustration.

**Pairs well with**:
- Low poly — isometric + low poly = the indie game look
- Miniature/diorama scenes — the parallel projection creates a toy-like quality
- Architecture/interior cutaways — everything is readable from the isometric view
- Pixel art — isometric pixel art is a distinct aesthetic
- Clean/flat colors — the diagrammatic quality suits simple palettes

**Conflicts with**:
- Cinematic perspective — isometric removes perspective drama
- Depth/atmosphere — parallel projection flattens spatial depth
- Photorealistic rendering — the camera projection is non-physical

**Example combination**: Isometric + miniature room interior + warm lighting + detailed objects → dollhouse-like cutaway, every object readable, no perspective distortion, charming miniature world

**Prompt cues**: isometric view; no vanishing points; parallel lines staying parallel; elevated diagonal angle

---

### Voxel

**What it is**: 3D equivalent of a pixel — a cube unit that builds 3D objects the way pixels build 2D images. Think Minecraft's block-based world.

**Visual effect**: Blocky, cubic, chunky. Everything is built from uniform cubes. The grid is visible and defines the aesthetic. Reads as retro-digital, game-like (Minecraft), or deliberately primitive. The uniformity of the grid creates an oddly satisfying regularity.

**Pairs well with**:
- Retro/game aesthetic — Minecraft is the reference point
- Isometric camera — voxels + isometric is a common combination
- Bright/saturated block colors — each voxel is a solid color
- Landscapes/environments — voxel worlds are charming
- Nostalgic/playful mood — the blockiness is inherently friendly

**Conflicts with**:
- Smooth/organic forms — voxels are cubic by definition
- Photorealism — too abstract
- Fine detail — the minimum unit is one cube

**Prompt cues**: voxel art; built entirely from small uniform cubes; blocky stepped surfaces

---

### Volumetric Rendering

**What it is**: Rendering of participating media — fog, smoke, clouds, dust, atmospheric haze. Light interacts with particles suspended in the air rather than just surfaces.

**Visual effect**: Visible light beams (god rays), atmospheric depth (distant objects fade into haze), soft glowing light sources in fog, realistic clouds and smoke. Adds a sense of atmosphere, depth, and weight to the air itself.

**Pairs well with**:
- Cinematic/dramatic lighting — god rays through windows or trees
- Horror/mystery — fog obscures, creates tension
- Fantasy environments — magical atmosphere, glowing particles
- Architectural visualization — atmospheric interiors
- Any scene with depth — atmosphere sells distance

**Conflicts with**:
- Clean/clinical rendering — volumetrics add softness and haze
- Flat/graphic styles — volumetrics are photographic
- Speed — volumetric rendering is computationally expensive

**Example combination**: Volumetric fog + single beam of light through window + dark interior + dust particles → god ray cutting through darkness, particles visible in the beam, atmospheric depth, cinematic drama

---

## Additional Techniques

### Ambient Occlusion

**What it is**: Rendering technique that calculates how exposed each point is to ambient light. Crevices, corners, and areas where surfaces meet become darker because less light reaches them. Often combined with other lighting but can be rendered alone.

**Visual effect**: Soft contact shadows in every crevice and corner. Adds subtle depth and grounding — objects feel heavier and more connected to surfaces. Alone, it produces a soft, shadowless image with dark creases. The "clay render + depth" look. Ubiquitous in modern rendering as a subtle realism enhancer.

**Pairs well with**:
- Clay render — AO on clay is a classic visualization technique
- Photorealistic rendering — AO adds micro-detail to shadows
- Architectural visualization — grounds objects on surfaces
- Product rendering — subtle contact shadows add believability

**Conflicts with**:
- Flat/graphic styles — AO adds unwanted depth
- Cel-shaded/toon — AO's soft gradients fight hard shadow edges
- Stylized rendering that rejects physical accuracy

---

### Global Illumination

**What it is**: Light bouncing between surfaces in a scene — indirect illumination. A red wall tints nearby white objects pink. The ceiling glows from light bouncing off the floor. The fundamental difference between "CG-looking" and "photorealistic."

**Visual effect**: Realistic, natural-feeling light. Color bleeding between surfaces. Soft, warm fill in shadows from bounced light. Interiors feel inhabited and real. Without GI, scenes look like objects floating in black — with it, light fills the space naturally.

**Pairs well with**:
- Interior scenes — GI is essential for believable interiors
- Path tracing — the technique that computes GI naturally
- Warm materials — wood, fabric, skin all benefit from color bleed
- Architectural visualization — natural light through windows bouncing everywhere

**Conflicts with**:
- Hard/graphic rendering — GI softens and fills
- Stylized flat lighting — GI adds complexity
- Speed — GI is computationally expensive

---

### Caustics

**What it is**: Focused light patterns produced when light refracts through or reflects off curved transparent/reflective surfaces. The dancing light patterns at the bottom of a swimming pool. The bright spot under a wine glass.

**Visual effect**: Dancing, focused light patterns on surfaces near glass, water, or curved metal. Bright, sharp, beautiful. One of the hardest effects to render and one of the most visually striking. Adds realism to any scene with transparent objects.

**Pairs well with**:
- Glass objects — wine glasses, bottles, crystal
- Water surfaces — pool caustics are the classic example
- Hard directional light — caustics need a clear light source
- Product photography — glass and liquid products
- Octane/path tracers — engines that handle caustics well

**Conflicts with**:
- Flat/diffused lighting — caustics need directional light
- Opaque/matte scenes — no transparent objects to create them
- Real-time rendering — caustics are expensive to compute

---

### Diorama / Miniature Scene

**What it is**: 3D scene rendered to look like a physical miniature model — a tiny world on a table. Combines isometric or slight perspective with selective focus, visible edges, and a sense of contained scale.

**Visual effect**: The scene has visible boundaries — it sits on a surface, the edges are defined. Tilt-shift-like selective focus. Everything looks miniature and precious. Warm, controlled lighting (like a photographer lit the tiny set). Objects are detailed but clearly at model scale.

**Pairs well with**:
- Isometric or slight overhead camera — the miniature viewing angle
- Tilt-shift/selective focus — only a band is sharp
- Warm/controlled lighting — photographed model quality
- Architectural subjects — buildings, rooms, cityscapes as models
- Low poly — miniature + geometric = cozy indie aesthetic

**Conflicts with**:
- Epic/vast scale — dioramas are small and contained
- Photorealistic full-scale — dioramas are obviously miniature
- First-person perspective — the overhead view is essential

**Example combination**: Diorama + miniature Japanese garden + slight overhead angle + selective focus + warm lighting → tiny perfect world, model-scale detail, visible edges, precious and contained

**Prompt cues**: miniature diorama; the whole scene at tiny model scale; narrow band of sharp focus; tilt-shift blur at top and bottom

---

### Cross-Section / Cutaway

**What it is**: Render showing the interior of an object or building by slicing away a portion of the exterior. Common in architectural visualization, product design, and educational illustration.

**Visual effect**: The interior is exposed while the exterior context remains. Shows hidden structure — the rooms inside a building, the components inside a machine, the layers inside a material. Technical and educational but visually striking.

**Pairs well with**:
- Isometric projection — the classic cutaway angle
- Architecture — showing room layouts and spatial relationships
- Product design — internal mechanisms revealed
- Diorama style — the miniature cutaway is charming
- Clean/even lighting — the interior needs to be readable

**Conflicts with**:
- Exterior-only rendering — cutaway removes the exterior
- Abstract art — cutaway is technical and literal
- Organic/natural subjects (usually) — better for manufactured things

**Prompt cues**: cross-section cutaway view; one side sliced open; interior structure exposed

---

### Exploded View

**What it is**: Components of an object separated along their assembly axes, floating in space showing how they fit together. The classic technical illustration device — every part visible and identifiable.

**Visual effect**: All components visible simultaneously, separated but aligned. Assembly relationships are clear. Technical, educational, satisfying. The floating-apart quality creates a sense of organized complexity.

**Pairs well with**:
- Technical/patent illustration — the native format
- Product design — showing manufacturing assembly
- Isometric projection — the standard exploded view angle
- Clean white background — the parts need to be readable
- Mechanical subjects — watches, engines, electronics

**Conflicts with**:
- Assembled/complete objects — exploded views disassemble
- Organic subjects — hard to "explode" a plant or animal
- Atmospheric rendering — the clinical quality fights mood

**Prompt cues**: exploded view; components floating apart, aligned; every part visible at once

---

### Holographic Render

**What it is**: Rendering that mimics holographic display aesthetics — semi-transparent, glowing, grid-like, usually blue or cyan against a dark background. Sci-fi UI conventions from Star Wars, Iron Man, Blade Runner 2049.

**Visual effect**: Semi-transparent geometry floating in space. Glowing edges and wireframe-like structures. Typically blue, cyan, or white against dark. Grid/scanline overlay. The object appears to be a light projection rather than a solid. Reads as sci-fi, futuristic, interface, military.

**Pairs well with**:
- Cyberpunk/sci-fi — the genre's visual language
- Dark backgrounds — holograms need darkness to glow
- Blue/cyan monochrome — the default hologram color
- Wireframe elements — exposed geometry
- UI/interface design — holographic dashboards

**Conflicts with**:
- Photorealism — holograms are obviously artificial
- Warm/organic aesthetics — holograms are cold and digital
- Solid/opaque rendering — holograms are translucent

---

### Glitch Art / Databending

**What it is**: Deliberately corrupting or manipulating digital data to produce visual artifacts. In 3D: distorted geometry, fragmented polygons, RGB channel splitting, pixel sorting, moshing compression artifacts.

**Visual effect**: Corrupted, fragmented, digital-decay. Geometry shatters or warps. Colors split into RGB channels. Compression artifacts (JPEG moshing) create painterly smearing. Reads as digital, broken, post-internet, deliberately imperfect.

**Pairs well with**:
- Cyberpunk — digital decay in dystopian context
- Vaporwave — shared digital nostalgia
- Dreamcore/Weirdcore — shared uncanny quality
- VHS/analog artifacts — cross-media corruption
- Neon/saturated color — the artifacts amplify vivid color

**Conflicts with**:
- Clean/precise rendering — glitch is the opposite
- Photorealism — too abstract and broken
- Natural/organic — glitch is digital-native
- Minimalism — glitch adds chaos

**Prompt cues**: glitch art; RGB channel splitting; corrupted pixel smears and displaced blocks; datamoshed distortion

---

### Retro 3D / PS1 Aesthetic

**What it is**: The look of early 3D graphics from the PlayStation 1 era (1994-2000). Affine texture warping (textures swim and distort), vertex jitter (geometry wobbles), low-resolution textures, limited polygon counts, no anti-aliasing.

**Visual effect**: Textures that warp and shimmer as the camera moves. Geometry that jitters and pops at vertices. Chunky, low-resolution textures with visible pixels. No texture filtering — everything is crunchy. Limited draw distance with fog. Reads as retro, nostalgic, lo-fi, deliberately primitive, horror (the distortion creates unease).

**Pairs well with**:
- Horror games — the visual instability creates tension (Puppet Combo, Iron Lung)
- Nostalgia for 1990s gaming — PS1, N64, Saturn era
- Low poly — the natural geometric companion
- Fog/limited draw distance — hiding the pop-in
- VHS/analog degradation — cross-media lo-fi
- Liminal space aesthetic — PS1 + empty space = uncanny

**Conflicts with**:
- Photorealism — the opposite
- Clean/smooth rendering — PS1 is crunchy by nature
- High resolution — defeats the purpose
- Modern PBR materials — wrong era entirely

**Example combination**: PS1 aesthetic + empty school hallway + warping textures + vertex jitter + fog + low resolution → unsettling retro horror, textures swimming, geometry unstable, liminal and nostalgic

**Prompt cues**: 1990s video game 3D graphics; low-resolution pixelated textures; jagged low-poly geometry; distance fog

---

### ASCII / Text-Based Rendering

**What it is**: Rendering images using text characters (letters, numbers, symbols) as "pixels." Each character's density represents a brightness value. From early computer art to modern artistic choice.

**Visual effect**: Images composed entirely of typed characters. At distance, the characters blend into a recognizable image. Up close, it's pure text. Monospaced font grid structure. Reads as retro-digital, hacker, matrix-like, deliberately primitive.

**Pairs well with**:
- Hacker/matrix aesthetic — the terminal/command line
- Retro computing — early computer art
- Cyberpunk — digital primitives
- Monochrome (green or amber on black) — the CRT terminal palette
- Wireframe — shared structural/skeletal quality

**Conflicts with**:
- Photorealism — too abstract
- Color (usually) — ASCII is typically monochrome
- Smooth gradients — the character grid is always visible
- Organic softness — the grid is rigid and mechanical

**Prompt cues**: ASCII art; image built from typed text characters; monospaced character grid

---

## References

- [3D rendering — Wikipedia](https://en.wikipedia.org/wiki/3D_rendering)
- [Isometric video game graphics — Wikipedia](https://en.wikipedia.org/wiki/Isometric_video_game_graphics)
- [Low poly — Wikipedia](https://en.wikipedia.org/wiki/Low_poly)
- [Cel shading — Wikipedia](https://en.wikipedia.org/wiki/Cel_shading)
- [Wireframe model — Wikipedia](https://en.wikipedia.org/wiki/Wireframe_model)
- [Physically based rendering — Wikipedia](https://en.wikipedia.org/wiki/Physically_based_rendering)
- [Subsurface scattering — Wikipedia](https://en.wikipedia.org/wiki/Subsurface_scattering)
