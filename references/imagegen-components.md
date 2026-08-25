# ImageGen Component Production

Use this reference only when the figure needs generated or edited raster components. The active `$imagegen` skill remains authoritative for tool mode, save paths, model selection, and transparency support.

## Decide the asset boundary first

Generate the smallest coherent semantic unit that can be positioned, scaled, or replaced independently. Good units include:

- a scientific pictogram;
- a stylized arrow with a fixed direction;
- a hub with its inseparable branch paths;
- a small mechanism illustration;
- a non-quantitative calibrated-support schematic or decision badge that functions as one visual unit.

Do not generate a whole slide, a whole multi-subplot figure, or final labels inside a bitmap. Do not split one tightly coupled visual into fragments if seams and alignment would become fragile.

## Quantitative graphics are not generative art

If a visual encodes real data or a numerical claim, do not ask ImageGen to draw the curve, band, axis, ticks, distributions, values, or calibration result. Reconstruct it deterministically from supplied data, use editable native/vector objects, or tightly crop a traceable source-derived element when the source is the only ground truth.

ImageGen may create a non-quantitative editorial frame, pictogram, or stylized support concept around such a graphic, but it must not invent or perturb the encoded evidence. If the source does not establish which marks are scientifically meaningful, stop at the component gate and request the caption, manuscript passage, or data.

## Reference roles

Label every image input as one of:

- **structural reference:** preserve composition and relationships;
- **style reference:** match palette, stroke, perspective, and detail density;
- **edit target:** change only the named part and preserve all invariants;
- **supporting input:** insert or combine a specific object.

When reconstructing an existing paper figure, preserve geometry and scientific identity before applying aesthetic improvement. Never replace a reference with a merely similar scene.

## Prompt template

```text
Use case: scientific-educational
Asset type: transparent PowerPoint component for a publication figure
Primary request: <one semantic component>
Input images: <roles of references, if any>
Style/medium: clean scientific editorial illustration, restrained detail
Composition/framing: <target aspect ratio, orientation, direction, and padding>
Color palette: <declared figure colors>
Line system: <stroke weight and outline character>
Text: none
Constraints: preserve <scientific invariants>; transparent background; isolated subject; no cast shadow; no watermark
Avoid: extra objects, labels, legends, decorative particles, gradients that conflict with the figure system
```

Specify the final PowerPoint bounding box before generation. Generate the correct orientation rather than rotating or stretching an unsuitable result.

## Consistency rules

- Define one style sheet for palette, outline color, stroke weight, perspective, shadow strength, and detail density.
- Reuse the same master asset for repeated symbols.
- For distinct components, use distinct prompts or calls; do not ask one variant parameter to represent unrelated subjects.
- A sparse asset sheet is acceptable only for a genuinely uniform icon family. Leave generous separation so assets do not share shadows or touch after splitting.
- Project-bound assets must be copied into the run directory and recorded in the asset manifest.

## Transparency and crop QA

Request genuine transparent output under the active ImageGen workflow. Before assembly, verify:

- an alpha channel exists;
- all four corners are transparent;
- the subject is not clipped;
- no white, dark, green, or magenta halo remains;
- semi-transparent regions were preserved intentionally;
- transparent padding is minimal but does not cut antialiasing;
- the asset remains clean on both a light and a dark test background.

If transparency is defective, repair or regenerate the asset. Do not conceal the defect with a matching PowerPoint rectangle.

## Resolution and scaling

- Prepare assets at roughly 2–4 times their final pixel footprint.
- Target at least 300 effective ppi for color or grayscale art; fine line art may need 450–600 ppi.
- Preserve aspect ratio in PowerPoint.
- If the asset's approved box and intrinsic ratio disagree, recrop or regenerate.

## Iteration discipline

Inspect semantics, direction, crop, alpha, style, and resolution after every generation. Revise one property per iteration: for example, arrow thickness, component orientation, or edge cleanup. Repeat all preservation invariants in edit prompts.

Record the final prompt, tool mode, source references, file hash, dimensions, and intended PowerPoint box in the asset manifest.
