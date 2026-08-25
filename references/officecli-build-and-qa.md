# OfficeCLI Assembly, QA, and PDF Delivery

Use this reference before creating or editing the PowerPoint, and again before delivery. The active `$officecli` skill remains authoritative for current command syntax.

## Build approach

1. Close the source file in PowerPoint or WPS before OfficeCLI mutations.
2. Inspect existing files with `view`, `get`, and `query` before changing them.
3. Prefer DOM operations; use raw OOXML only for a feature that DOM operations cannot express.
4. Run `officecli help pptx <element>` instead of guessing a property.
5. Use explicit units and stable object names or IDs.
6. Use atomic `batch` operations for repeated construction when practical.
7. Flush with `save` or `close` before an external renderer or PDF exporter reads the file.

## Layer order

Create objects from back to front:

1. slide and subplot background;
2. native structural primitives;
3. background raster components;
4. primary and secondary raster components;
5. arrows and relation lines;
6. native text and equations;
7. subplot letters and final calibration marks.

Name objects by subplot and semantic role. Do not rely on positional indices after insertion or deletion.

## Editable content rules

- All readable text must be visible native PowerPoint text or equations.
- Keep complex ImageGen art as independently replaceable pictures.
- Keep simple primitives native when their appearance meets the visual system.
- Avoid default Office themes, automatic shadows, default SmartArt, and default arrow styling when they create a presentation-template look.
- Preserve each picture's aspect ratio.
- Group objects by semantic unit only after their positions are stable; text must remain independently editable.

## Deterministic checks

Use deterministic environment flags when resident behavior or update checks could affect repeatability:

```bash
export OFFICECLI_SKIP_UPDATE=1
export OFFICECLI_NO_AUTO_RESIDENT=1

officecli validate figure.pptx --json
officecli view figure.pptx issues --json
officecli view figure.pptx text
officecli query figure.pptx 'picture:no-alt' --json
unzip -t figure.pptx
```

Interpret results rather than only recording exit codes:

- schema errors must be zero;
- formatting, overflow, and structural issues must be zero or explicitly justified;
- extracted text must contain no placeholder, TODO, lorem ipsum, temporary label, or missing required string;
- package relationships and media must be intact;
- picture accessibility requirements must match the delivery context.

`scripts/validate_delivery.py` automates these checks when the local dependencies are available.

## Visual audit

Render every figure after meaningful changes. The final audit must include a high-resolution render, preferably 300 dpi, and a view at the actual publication size.

Review adversarially for:

- collisions, clipping, narrow text boxes, or abnormal wrapping;
- stretched, blurry, or low-resolution components;
- alpha halos, opaque corners, and transparent padding;
- inconsistent component scale, outline, or baseline;
- wrong arrow direction, duplicated arrowheads, broken paths, or crossings;
- low contrast and fine lines that disappear when reduced;
- unjustified blank regions or an oversized secondary subplot;
- changed pixels or objects inside frozen regions.

A clean OfficeCLI report cannot prove these visual properties. When available, give the final render to an independent reviewer or fresh subagent.

## Repair loop

Repair only the smallest failing scope. After each repair:

1. rerun the affected structural check;
2. rerender the repaired subplot;
3. compare frozen regions with the last accepted version;
4. inspect the whole figure once more.

Stop and report after three non-converging cycles rather than accumulating compensating changes.

## PDF delivery

Export from the accepted editable PowerPoint, never from a preview PNG. Verify:

- correct page count and physical dimensions;
- PDF opens and is not unexpectedly encrypted;
- required fonts are embedded with no substitution;
- raster components were not over-downsampled;
- transparency and line weights match the PowerPoint render;
- a 300 dpi PDF render is visually identical to the accepted preview;
- the manuscript references the intended final filename.

If the user requests export without content changes, hash and timestamp the PPTX before and after export and confirm that they are unchanged.
