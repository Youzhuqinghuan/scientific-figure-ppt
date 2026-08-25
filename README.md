# scientific-figure-ppt

A Codex Skill for creating, reconstructing, revising, and validating editable scientific-paper figures in PowerPoint.

它将科研配图制作固化为由大到小的流程：先确定投稿画布和子图比例，再确定每个子图的内部骨架与组件边界，使用 ImageGen 生成无文字的透明科研组件，通过 OfficeCLI 精确组装 PPT，最后统一字体字号、压缩无功能空白，并完成 PPTX 与 PDF 双重检查。

## What it produces

- editable PowerPoint source (`.pptx`);
- publication-size PDF;
- high-resolution preview;
- project-local ImageGen assets and provenance;
- deterministic QA report.

## Required capabilities

- Codex with the `imagegen` Skill available;
- OfficeCLI on `PATH` with the `officecli` Skill available;
- a PDF renderer/inspector for final export QA.

The Skill does not copy or vendor OfficeCLI or ImageGen. It composes the current installed versions so their tool-specific behavior stays up to date.

## Install

Clone this repository into the Codex skills directory:

```bash
git clone https://github.com/Youzhuqinghuan/scientific-figure-ppt.git \
  ~/.codex/skills/scientific-figure-ppt
```

Restart or refresh Codex skill discovery, then invoke:

```text
Use $scientific-figure-ppt to reconstruct this paper figure as an editable PPTX and publication-ready PDF.
```

## Workflow

```text
output contract
  -> whole-figure subplot layout
  -> subplot skeletons
  -> component specifications
  -> ImageGen components
  -> OfficeCLI assembly
  -> native typography
  -> whitespace and balance pass
  -> structural + visual QA
  -> PDF delivery
```

The key invariant is progressive freezing: once a higher-level layout or an approved subplot passes review, later repairs should change only the smallest failing object or region.

## Repository structure

```text
SKILL.md
agents/openai.yaml
references/
assets/templates/
scripts/
```

- `SKILL.md` contains routing, constraints, and completion gates.
- `references/` contains detailed workflow, layout, ImageGen, OfficeCLI, and QA guidance loaded only when relevant.
- `assets/templates/` provides reusable specification, manifest, and QA-report templates.
- `scripts/` provides run initialization and deterministic delivery checks.

## Helper scripts

Initialize a traceable run:

```bash
python3 scripts/init_figure_run.py figure-runs/example \
  --name example \
  --mode new \
  --width-mm 170 \
  --height-mm 90 \
  --subplots A,B,C
```

Validate final artifacts:

```bash
python3 scripts/validate_delivery.py \
  --pptx figure-runs/example/final/example_editable.pptx \
  --assets-dir figure-runs/example/assets/imagegen \
  --pdf figure-runs/example/final/example.pdf \
  --output figure-runs/example/qa/validation.json
```

Deterministic checks complement, but never replace, rendered visual review.
