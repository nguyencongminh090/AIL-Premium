---
name: knowledge-systemize
description: Organizes knowledge across several papers (or a topic) into a structured system — a taxonomy of approaches, the key dimensions along which they differ, and a side-by-side comparison table — turning a pile of papers into one organized map. Cross-paper by default. Use for: systematize, organize these papers, build a taxonomy, comparison framework, structure the field, hệ thống hóa kiến thức, dựng khung phân loại, sắp xếp các bài báo. Takes paper ids / "all" / a topic via $ARGUMENTS. Output is Vietnamese (terms preserved) to notes/knowledge-systemize-<slug>.md.
argument-hint: <paper ids | all | topic>
---

# Knowledge Systemize Worker (Hệ thống hóa)

This skill imposes structure on a set of papers (or a topic): it derives the
dimensions that distinguish approaches, groups the papers into a taxonomy, and lays
them out in a comparison table. It is cross-paper synthesis — distinct from
`problem-expand` (which zooms out on a single problem) and `research-gap` (which
hunts for what is missing).

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, Vietnamese-with-preserved-terms output, `notes/` location, and fidelity.

## Procedure
1. **Scope the set.** `$ARGUMENTS` may be a list of paper ids, `all`, or a topic. It
   reads the relevant PDFs for fidelity, and may reuse existing `notes/<id>-summary.md`
   to save effort when those notes already exist.
2. **Derive the organizing dimensions** relevant to the set (for this project, e.g.
   representation, learning paradigm, aesthetic signal, output type, evaluation
   protocol). It states why these dimensions matter.
3. **Build a taxonomy:** group the approaches into named categories/branches with a
   short rationale for each grouping.
4. **Build a comparison table:** rows = papers, columns = the dimensions.
5. **Narrate the structure:** what it reveals — clusters, trends, outliers,
   convergence/divergence across the set.
6. **Glossary, save, preview** to `notes/knowledge-systemize-<slug>.md` (slug from the
   topic or paper set).

## Output template (`notes/knowledge-systemize-<slug>.md`)
```
# Hệ thống hóa — <slug>
> Phạm vi: <paper ids / topic> · Worker: knowledge-systemize · Ngày: <YYYY-MM-DD>

## Các chiều phân loại (Organizing dimensions) & lý do chọn
## Phân loại (Taxonomy)
### <Nhóm 1>
## Bảng so sánh (Comparison table)
| Bài báo | <Chiều 1> | <Chiều 2> | ... |
## Nhận định về cấu trúc (What the structure reveals)
## Thuật ngữ (Glossary)
```
