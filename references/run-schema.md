# Run Directory and Manifest Schema

Use this reference when a figure benefits from explicit checkpoints and asset provenance. `scripts/init_figure_run.py` creates this structure.

## Directory layout

```text
<run>/
├── input/
├── planning/
│   ├── figure-spec.json
│   └── layout-blueprint.json
├── assets/
│   ├── imagegen/
│   ├── source-derived/
│   └── asset-manifest.json
├── build/
├── qa/
└── final/
```

Use versioned filenames in `build/`. Put only accepted deliverables in `final/`.

## Figure specification

Record:

- figure name and operating mode;
- physical width and height in millimetres;
- output formats;
- manuscript and caption sources;
- declared fonts, minimum text size, line system, and palette;
- subplot IDs, purpose, reading order, and frozen state;
- journal or user constraints;
- known uncertainties that require author confirmation.

## Layout blueprint

For every subplot and component, record bounds in one consistent coordinate system:

```json
{
  "id": "B-center-hub",
  "type": "imagegen-component",
  "subplot": "B",
  "bounds_mm": {"x": 30.4, "y": 72.0, "w": 13.2, "h": 12.6},
  "aspect_locked": true,
  "status": "approved"
}
```

Recommended statuses are `planned`, `approved`, `built`, `validated`, and `frozen`.

## Asset manifest

For every raster asset, record:

- stable asset ID and semantic purpose;
- final project-local path;
- ImageGen prompt or source region;
- input-image roles;
- generation or edit mode;
- pixel dimensions, alpha status, and file hash;
- intended PowerPoint bounds and orientation;
- validation notes and known limitations.

Do not reference an asset that exists only in a global generated-images location or an OS temporary directory.

## QA evidence

Keep machine-readable reports and human visual evidence in `qa/`:

- OfficeCLI validate and issue results;
- extracted text and placeholder scan;
- PPTX package-integrity result;
- component transparency report;
- high-resolution preview;
- frozen-region comparison when revisions are targeted;
- final PDF metadata and rendered preview.

Completion requires real artifacts and passing evidence, not a status field edited by hand.
