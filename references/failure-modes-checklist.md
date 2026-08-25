# Failure Modes and Final Checklist

Read this reference during final review or after a repair loop fails to converge.

## Frequent process failures

- Generating polished icons before the page and subplot proportions are approved.
- Generating the complete figure as one image and covering it with editable text.
- Expanding the canvas repeatedly instead of fixing a subplot's internal organization.
- Dividing subplots equally despite different information density or narrative weight.
- Revising one subplot through whole-slide scaling or re-layout, causing accepted areas to drift.
- Adding final text before component geometry stabilizes.
- Shrinking labels below the publication-readable threshold to avoid re-layout.

## Frequent component failures

- Generated text, numbers, labels, or equations inside bitmap components.
- Opaque or haloed backgrounds around supposedly transparent assets.
- Excessive transparent padding that corrupts alignment and whitespace calculations.
- Inconsistent perspective, line weight, color, or detail across generation batches.
- Arrows generated before route geometry is fixed, then stretched or rotated into unsuitable directions.
- Repeated symbols regenerated separately and no longer visually identical.
- Low-resolution line art that appears acceptable only at editing zoom.

## Frequent PowerPoint failures

- Default Office arrowheads, shadows, or rounded rectangles conflicting with the scientific visual system.
- A generated arrow plus a native arrowhead creating a duplicate tip.
- Position-based object references changing after insertions.
- Pictures stretched to fill approved boxes.
- Text technically fitting but wrapping into visually narrow, fragmented lines.
- Native text or equations replaced by invisible, off-canvas, or metadata-only content.
- The file remaining open in PowerPoint while OfficeCLI attempts to mutate it.

## Frequent QA failures

- Treating zero schema errors as proof of visual quality.
- Inspecting only a whole-figure thumbnail and missing small-label or alpha defects.
- Inspecting only a zoomed render and missing illegibility at final publication size.
- Delivering the PPTX without checking the exported PDF for font substitution or downsampling.
- Fixing an isolated defect without comparing frozen areas to the accepted version.

## Final acceptance checklist

### Scientific fidelity

- [ ] Every claim, label, symbol, and relation is grounded in supplied source material.
- [ ] Caption, manuscript, and visual content do not contradict each other.
- [ ] No generated component introduces an unrequested scientific object or implication.

### Layout

- [ ] Physical size and aspect ratio match the output contract.
- [ ] Subplot hierarchy and reading order are immediately clear.
- [ ] Area reflects importance and information density.
- [ ] Empty space is functional; no subplot is crowded beside an unexplained blank region.
- [ ] Secondary subplots do not dominate the visual weight.

### Components

- [ ] Complex visuals are separate replaceable components.
- [ ] Repeated symbols reuse a common master.
- [ ] Alpha corners, crop, aspect ratio, resolution, and edge quality pass.
- [ ] No final text is embedded in bitmap art.
- [ ] Styles are consistent across batches.

### Typography and paths

- [ ] All readable text and mathematics are native and editable.
- [ ] Role-based fonts, sizes, weights, and colors are consistent.
- [ ] Minimum text size remains readable at final output size.
- [ ] Arrows are minimal, directional, unambiguous, and visually consistent.
- [ ] No label, connector, or component is clipped or overlapped.

### Structure and delivery

- [ ] OfficeCLI schema validation passes.
- [ ] OfficeCLI issue scan passes or every exception is justified.
- [ ] Extracted text has no placeholder or temporary label.
- [ ] PPTX ZIP integrity passes.
- [ ] Final high-resolution render passes independent visual review.
- [ ] PDF page size, page count, font embedding, transparency, and render match the PPTX.
- [ ] Frozen regions match the accepted checkpoint.
