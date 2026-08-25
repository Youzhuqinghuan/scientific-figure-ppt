# Layout, Typography, and Density System

Use this reference while defining subplot geometry, text hierarchy, line weights, or whitespace.

## Physical-size first

Set the slide to the intended publication dimensions before placing objects. Judge readability at the final printed or on-page size, not only at an enlarged editing zoom.

Take page dimensions, permitted fonts, font sizes, line weights, color rules, and export requirements from the target journal's current author guidelines or explicit user instructions. If a required value is unavailable, record it as unresolved rather than claiming compliance with a generic default. Do not silently resize the page later to solve a local collision.

## Geometry

Allocate area according to scientific importance, information density, and the minimum size required to recognize components. Do not divide the page equally by default.

Subplots may use different pale background colors when that improves grouping. Avoid visible border boxes unless the border encodes structure.

## Alignment system

- Establish a small set of shared horizontal and vertical guides.
- Align repeated objects to a common baseline or centerline.
- Use equal sizes and gaps for repeated semantic units unless meaning requires a difference.
- Check visual centering in addition to geometric centering; asymmetric components can look off-center even when coordinates match.
- Keep arrows away from labels and avoid crossings unless the crossing itself has clear notation.

## Typography tokens

Translate the journal requirements into named roles for subplot letters, subplot titles, stage headings, ordinary labels, micro-labels, and mathematics. Keep each role consistent across subplots. Avoid shrinking an isolated label to solve a fit problem; revise wording or geometry instead.

All final labels, numbers, units, Greek letters, and equations remain native PowerPoint text or equation objects. Do not accept generated raster text.

## Line and arrow tokens

Derive outline, connector, dashed-line, and arrowhead specifications from the journal requirements and the declared visual system. They must survive the final-size render. Use a generated arrow component when a native arrow cannot meet the agreed visual style, but keep directions and weights consistent.

## Non-functional whitespace audit

For every empty region, identify one function: margin, inter-subplot separation, within-group separation, reading path, or deliberate emphasis. If none applies, treat the region as a layout defect.

Check:

- content bounding box versus subplot bounds;
- title bands that consume disproportionate height;
- crowded content beside unused space;
- visual weight on the left versus right and top versus bottom;
- a secondary subplot enlarged beyond its narrative importance;
- excessive transparent padding inside component files;
- repeated connectors or labels that create clutter rather than information.

Optimize by deleting redundancy and reallocating area, not by distorting images or reducing text below the declared minimum.
