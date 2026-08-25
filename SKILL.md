---
name: scientific-figure-ppt
description: Create, reconstruct, revise, and validate editable scientific-paper figures in PowerPoint using top-down subplot decomposition, ImageGen components, native typography, and OfficeCLI assembly. Use when a journal or conference figure must be delivered as editable PPTX and publication-ready PDF. Do not use for ordinary slide decks, posters, manuscript writing, standalone code-native plots, or bitmap-only illustrations.
---

# Scientific Figure PPT

Create scientific figures as layered PowerPoint artifacts, not flattened illustrations. The default deliverables are an editable `.pptx`, a publication-size `.pdf`, a rendered preview, and traceable component assets.

## Required capabilities

This workflow composes two other skills:

- Read and follow the active `$imagegen` skill before generating or editing any bitmap component.
- Read and follow the active `$officecli` skill before creating, inspecting, or changing a PowerPoint file.
- For final PDF export or inspection, use the available PDF skill or equivalent PDF rendering tools.

If ImageGen or OfficeCLI is unavailable, stop at the affected gate and report the blocker. Do not replace the missing capability with a full-slide screenshot or a fake editable deliverable.

## Choose the operating mode

- **New figure:** derive a visual specification from the manuscript, caption, and author constraints.
- **Reconstruction:** treat the supplied figure as a structural reference; rebuild text and components separately instead of placing the source image as the slide.
- **Targeted revision:** freeze every approved subplot and modify only the named region unless the requested change necessarily alters a higher-level layout decision.

For an ambiguous nested region, default to the smallest stable named object or approved bounding box. Keep its title, connectors, neighboring objects, and parent geometry frozen unless the user explicitly includes them or the requested change cannot work without reopening that scope.

Preserve exact scientific meaning. Do not invent labels, mechanisms, outcomes, quantitative values, or visual claims that are not supported by the provided manuscript or instructions.

## Mandatory hierarchy

Work from large decisions to small decisions and do not skip levels:

1. **Output contract:** physical page size, aspect ratio, required formats, final reading scale, source text, and editable-content expectations.
2. **Whole-figure layout:** assign subplot bounds, relative visual weight, reading order, margins, and background grouping.
3. **Subplot skeleton:** place input, process, output, hubs, axes, rows, and connection routes as simple placeholders.
4. **Component specification:** define every visual unit's semantic role, bounding box, direction, aspect ratio, color, and implementation type.
5. **Component production:** generate or extract only the approved components; validate transparency and fidelity before assembly.
6. **PowerPoint assembly:** place backgrounds, structural primitives, bitmap components, connectors, and native text in that order.
7. **Typography:** add labels, formulas, values, and subplot letters only after component geometry is stable.
8. **Density pass:** remove redundant arrows and text, reduce non-functional whitespace, and rebalance subplot areas without stretching assets.
9. **QA and export:** run structure checks, render at publication scale and high resolution, repair the smallest failing scope, then export PDF.

Each level becomes a gate. Once accepted, freeze it and keep a regression reference. If a lower-level problem can be solved locally, do not reopen a higher-level decision.

Read [references/workflow.md](references/workflow.md) for gate criteria and mode-specific execution.

## Object implementation rules

- Keep all readable text, formulas, subplot letters, values, and axis labels as visible native PowerPoint text or equation objects.
- Use native PowerPoint primitives for simple rectangles, circles, ellipses, axes, separators, and uncomplicated lines when they satisfy the visual system.
- Use ImageGen for scientific pictograms, complex mini-diagrams, stylized arrows, badges, hub graphics, and other visual units that would look templated or crude as default PowerPoint shapes.
- One bitmap should represent one coherent semantic unit. Do not generate the whole figure, a whole slide, or multiple unrelated subplots as one raster image.
- Do not burn final text into ImageGen assets. Generate text-free art and overlay native PowerPoint text.
- Do not use ImageGen to invent quantitative curves, calibration trajectories, uncertainty bands, axes, ticks, or measured values. Build data-encoding graphics deterministically from supplied data, as native/vector objects, or from a traceable source-derived asset; reserve ImageGen for non-quantitative editorial components.
- Preserve image aspect ratios. If an asset does not fit its approved bounding box, crop or regenerate it; never distort it to fill space.
- Reuse the same master asset for repeated symbols when semantic identity is unchanged.
- Use subplot background color only when it clarifies grouping. A visible border is not the default.

Read [references/imagegen-components.md](references/imagegen-components.md) whenever raster components are needed.

## Layout and typography

- Obtain physical dimensions, font families, font sizes, line weights, and file requirements from the target journal's author guidelines or explicit user instructions before final layout.
- Do not substitute generic defaults when the journal specifies a value. If a required rule is unavailable, record it as an unresolved input instead of presenting a provisional choice as compliant.
- Calibrate text at the required final physical size, not at an enlarged editing zoom.
- Use consistent role-based typography tokens for subplot letters, titles, stage labels, ordinary labels, micro-labels, and mathematics.
- Treat every empty region as either functional spacing or a layout defect. Eliminate non-functional whitespace without removing the separation needed to read groups.
- Allocate subplot area by information density and importance, not by mechanical equal division.

Read [references/layout-and-typography.md](references/layout-and-typography.md) when defining layout, whitespace, fonts, or line weights.

## PowerPoint build rules

- Prefer OfficeCLI DOM operations. Use raw OOXML only when DOM operations cannot express a required result.
- Ask `officecli help` instead of guessing property names.
- Use stable object names or IDs and explicit coordinates and dimensions.
- Use atomic `officecli batch` operations for repeated assembly when practical.
- Save or close the OfficeCLI resident before any external renderer reads the file.
- Keep a versioned last-known-good `.pptx`; do not overwrite the only accepted version during an experimental repair.
- If PowerPoint has the file open, close it before OfficeCLI mutations.

Read [references/officecli-build-and-qa.md](references/officecli-build-and-qa.md) before assembly, validation, or PDF delivery.

## Standard run artifacts

Use `scripts/init_figure_run.py` when a structured run directory will improve traceability. It creates planning, asset, build, QA, and final-delivery locations without overwriting existing work.

Keep at least:

- a figure specification;
- a subplot layout blueprint;
- an asset manifest with generation provenance;
- the editable PowerPoint source;
- a component contact sheet when raster assets exist;
- a rendered preview;
- validation results;
- the final PDF.

Read [references/run-schema.md](references/run-schema.md) when initializing a run or recording manifests.

## Quality gates

Do not call the task complete until all applicable gates pass:

- **Layout gate:** the blank skeleton already communicates subplot hierarchy and reading order.
- **Component gate:** assets have correct meaning, direction, style, alpha, crop, resolution, and aspect ratio.
- **Typography gate:** text is editable, accurate, consistent, unclipped, and readable at final size.
- **Density gate:** no unexplained large blank regions, redundant connectors, or secondary subplot dominating the figure.
- **Structural gate:** OfficeCLI validation and issue scans pass; the PPTX package is intact.
- **Visual gate:** a fresh render shows no collision, distortion, fringe, low contrast, broken path, or unexpected drift in frozen areas.
- **PDF gate:** physical size, page count, embedded fonts, transparency, and high-resolution rendering match the accepted PPTX.

Use `scripts/validate_delivery.py` for deterministic package, asset, and OfficeCLI checks. This script complements visual review; it cannot replace it.

Read [references/failure-modes-checklist.md](references/failure-modes-checklist.md) during final review or when a build repeatedly fails to converge.

For a complex build, use an independent reviewer or fresh subagent for the final visual audit when available. Repair only the smallest failing object or subplot, then rerun the affected gate and the final whole-figure regression check.
