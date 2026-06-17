# Research Worker Conventions

Shared, binding conventions for every paper-analysis **Worker** skill in this
project (`paper-summary`, `paper-overview`, `methodology-read`, `vi-translate`,
`research-orchestrator`, and any future worker). Each Worker applies these rules
unless its own `SKILL.md` explicitly overrides one of them.

## 1. Project context
- This is an academic research project on **photographic aesthetics / aesthetic
  viewpoint & composition recommendation**.
- Source papers live in `papers/`, named `NNN_Title_With_Underscores.pdf`.
- The 3-digit prefix is the paper's **canonical id**. Current papers:
  - `001` — Photography Perspective Composition Towards Aesthetic Perspective Recommendation
  - `003` — Geometric Viewpoint Learning with Hyper-Rays and Harmonics Encoding
  - `004` — Image Aesthetic Assessment Based on Pairwise Comparison
  - `008` — Aesthetic Camera Viewpoint Suggestion with 3D Aesthetic Field

## 2. Input resolution (`$ARGUMENTS`)
A Worker interprets `$ARGUMENTS` as one of:
- a **paper id** — `003`
- a **filename or partial title** — `pairwise`, `004_Image_Aesthetic`
- a **path** — `papers/003_Geometric_Viewpoint...pdf`
- the literal `all` — operate on every paper in `papers/`

If `$ARGUMENTS` is empty, the Worker lists `papers/` and asks which paper to use
**before doing anything else**. It never guesses silently.

## 3. Language & terminology (output style)
- Write all output in **Vietnamese, academic register (học thuật)**. This covers
  not only saved artifacts but also **conversational interaction** — clarifying
  questions, plans, progress updates, chat previews, and final reports are all in
  Vietnamese. (Code, commands, paths, and the preserved English terms stay as-is.)
- **Preserve original English technical terms.** On first use in a document write
  `thuật ngữ tiếng Việt (English term)`; afterwards the Vietnamese form may be used
  alone, but the English term must stay recoverable.
- Never invent a Vietnamese term for a concept with no settled translation — keep
  the English term and gloss it.
- End every output with a `## Thuật ngữ (Glossary)` table:
  `| English | Tiếng Việt | Giải thích ngắn |`.
- `vi-translate` is the only Worker that translates prose **continuously**; the
  others write Vietnamese **analysis** *about* an English paper.

## 4. Output location
- All artifacts go to a flat **`notes/`** folder at the project root (create it if
  missing).
- Naming:
  - single-paper worker → `notes/<id>-<worker>.md` (e.g. `notes/003-summary.md`)
  - cross-paper worker → `notes/<worker>-<slug>.md` (e.g. `notes/research-gap-viewpoint.md`)
- Each file opens with a header block: paper id, title, source filename, worker
  name, date (`YYYY-MM-DD`).
- After writing the file, print a **short preview** in chat (key points only) plus
  the saved path. Do not dump the whole file into chat.

## 5. Fidelity
- Read the actual PDF with the Read tool. Never analyze from the title alone.
- Do not fabricate numbers, citations, or claims. If the paper does not state
  something, write "bài báo không nêu (not stated in the paper)".
- Quote sparingly and mark quotes; prefer paraphrase + section/page reference.
- Preserve all quantitative results exactly (metrics, dataset sizes, ablation deltas).

## 6. Relationship to the ARS plugin
These Workers are **lightweight, single-pass** tools for reading and distilling
individual papers. For heavy multi-agent work — full literature synthesis,
simulated peer review, end-to-end paper writing — defer to the ARS plugin
(`/ars-full`, `/ars-reviewer`, `/ars-lit-review`, …) rather than reimplementing it.
