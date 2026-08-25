# Workflow and Gate Criteria

Use this reference for every scientific-figure task. It defines the execution order, stage outputs, and stopping conditions.

## 1. Intake and grounding

Collect only the inputs needed to preserve scientific meaning:

- manuscript passages and figure caption;
- current figure or sketch, if one exists;
- journal physical-size and file-format requirements;
- required labels, notation, palette, and font rules;
- which regions are approved and must remain unchanged;
- whether the user wants staged approval or an autonomous end-to-end build.

Classify each source image as an edit target, a structural reference, a style reference, or a reusable source-derived asset. A full-figure reference is never the final slide background unless the user explicitly requests a non-editable output.

Create a figure specification before drawing. Resolve mismatches between caption, manuscript, and source figure by reporting them; do not silently choose a scientific interpretation.

For a targeted revision, write a freeze map before implementation. When a requested area has nested content, use the smallest stable named object or bounding box as the editable scope. Titles, arrows, connectors, siblings, and parent layout stay frozen unless explicitly included. Record conditional unlocks separately rather than quietly expanding the patch.

## 2. Gate 1: whole-figure layout

Start with a blank physical-size slide and rectangles representing subplot bounds. Decide:

- subplot reading order;
- relative importance and area;
- shared alignment lines;
- outer margins and inter-subplot gaps;
- whether subtle background colors are useful;
- which subplot boundaries should remain visually open.

Do not place final icons or detailed text yet. Use placeholders only.

**Pass when:** the skeleton alone makes the visual hierarchy and reading order obvious, and no subplot is oversized merely to accommodate a weak internal arrangement.

For ambiguous or expensive builds, render this skeleton for user review. If the user requested autonomous completion, preserve it as a versioned checkpoint and continue.

## 3. Gate 2: subplot skeletons

Treat each subplot as its own information architecture. Identify:

- inputs, transformations, outputs, and decisions;
- the main visual path and optional secondary paths;
- rows, columns, hubs, axes, panels, or repeated units;
- exactly where arrows begin and end;
- title, label, formula, and annotation regions;
- component bounding boxes and aspect ratios.

Use simple placeholders and routes. Avoid final visual polish. Give objects stable names based on subplot and role, such as `B-center-hub`, `B-arrow-context`, or `C-support-plot`.

**Pass when:** every future component has an approved box and direction, and the subplot can be understood after placeholder text is removed.

## 4. Gate 3: implementation decisions

For each object, choose one implementation:

- native text or equation;
- native primitive or line;
- generated transparent component;
- tightly cropped source-derived component when identity must be preserved;
- composite semantic component when separating it would create fragile alignment.

Any object that encodes real quantitative evidence must use supplied data, editable deterministic construction, or a traceable source-derived element. ImageGen cannot invent data-shaped curves, uncertainty bands, axes, ticks, or values.

Record the decision before asset generation. Avoid changing implementation type after assembly unless a rendered defect proves it necessary.

**Pass when:** the asset list and native-object list fully cover the skeleton without whole-figure rasterization.

## 5. Gate 4: component production

Generate or prepare assets at the approved orientation and aspect ratio. Validate each asset before PowerPoint assembly. Use one targeted revision per iteration.

**Pass when:** each component has correct semantics, transparent alpha where requested, clean edges, suitable resolution, and a traceable source or prompt.

## 6. Gate 5: assembly

Assemble from back to front:

1. page and subplot backgrounds;
2. structural containers and separators;
3. background visual components;
4. primary and secondary components;
5. arrows and relationship lines;
6. native text and equations;
7. final micro-labels and calibration marks.

Do not distort components. Do not add default arrowheads on top of generated arrow components.

**Pass when:** all objects are inside their approved bounds, layering is correct, and no placeholder remains.

## 7. Gate 6: typography

Apply the typography system only after geometry is stable. Confirm exact wording against the manuscript and caption. Check true subscripts, superscripts, Greek letters, mathematical italics, and units.

**Pass when:** every readable string is native and editable, text hierarchy is consistent, and the minimum-size render remains legible.

## 8. Gate 7: density and balance

Optimize in this order:

1. remove redundant labels, arrows, and decoration;
2. reduce excessive gaps within groups;
3. enlarge components whose meaning is hard to read;
4. redistribute subplot width or height by information density;
5. change total canvas size only when publication constraints permit and internal re-layout cannot solve the problem.

Whitespace is functional only if it separates groups, preserves a reading path, or creates deliberate emphasis. Do not stretch art to occupy unused space.

**Pass when:** there is no unexplained large blank region, no crowded corner beside an empty region, and no secondary subplot dominates the visual weight.

## 9. Gate 8: regression and delivery

Freeze accepted areas with a checkpoint render and object-level reference. For targeted revisions, compare frozen regions against the last-known-good version.

Run structural, visual, and PDF checks. A clean OfficeCLI report is necessary but not sufficient. Rendered review is always required.

After a repair, rerun:

- the gate that failed;
- regression checks for frozen areas;
- the final whole-figure render.

Stop after three non-converging repair cycles and report the remaining defect and likely root cause instead of accumulating compensating changes.
