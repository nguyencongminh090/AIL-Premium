---
name: paper-summary
description: Produces a faithful, section-by-section summary of an academic paper in papers/. Use when the user wants to summarize, condense, or "tóm tắt" a specific paper identified by id (e.g. 003), filename, path, or "all". This skill condenses — it does not critique (use methodology-read for that). Output is Vietnamese academic prose with original English terms preserved plus a glossary, saved to notes/<id>-summary.md. Triggers: summarize paper, summary of 003, tóm tắt bài báo, condense this paper, what does paper X say, recap the paper.
argument-hint: <paper id | filename | path | all>
---

# Paper Summary Worker

This skill produces a faithful, section-by-section summary of one academic paper
(or every paper when given `all`). It is a reading aid: it condenses the paper, it
does not evaluate or critique it. For critical analysis the user should be directed
to `methodology-read`.

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding — input
resolution, Vietnamese-with-preserved-terms output, the `notes/` output location,
and fidelity rules all come from there. It reads that file before producing output.

## Procedure
1. **Resolve the target.** It interprets `$ARGUMENTS` per the shared input rules.
   If empty, it lists `papers/` and asks which paper. For `all`, it repeats the
   whole procedure once per paper and writes one file each.
2. **Read the PDF.** It reads the resolved file with the Read tool, covering the
   full text (using page ranges for long PDFs).
3. **Map the structure.** It identifies the paper's sections (abstract,
   introduction, related work, method, experiments/results, discussion, conclusion).
4. **Condense each section** in 2–5 sentences, keeping the original argument order
   and preserving exact quantitative results, dataset names, and metrics.
5. **Capture the essentials** separately: the problem, the core idea, the
   contributions, and the headline results.
6. **Apply the language convention** (Vietnamese + inline English terms) and build
   the glossary of every preserved term.
7. **Save and preview.** It writes `notes/<id>-summary.md` using the template
   below, then prints a 5–8 line preview plus the saved path in chat.

## Output template (`notes/<id>-summary.md`)
```
# Tóm tắt — <id> · <Title>
> Nguồn: <filename> · Worker: paper-summary · Ngày: <YYYY-MM-DD>

## TL;DR (3 câu)
## Vấn đề (Problem)
## Ý tưởng cốt lõi (Core idea)
## Tóm tắt theo mục (Section-by-section)
### <Tên mục>
## Kết quả chính (Key results)   ← bảng số liệu khi có
## Đóng góp (Contributions)
## Hạn chế tác giả tự nêu (Author-stated limitations)
## Thuật ngữ (Glossary)
```
