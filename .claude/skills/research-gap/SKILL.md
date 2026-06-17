---
name: research-gap
description: Synthesizes research gaps and future directions across a set of papers (or all papers analyzed so far) — unanswered questions, weaknesses recurring across the set, under-explored settings and assumptions everyone shares, evaluation/data gaps, and the white space no paper covers — then turns each gap into a concrete, actionable research opportunity. Feeds directly into a thesis or proposal. Cross-paper. Use for: research gaps, find gaps, gap analysis, future directions, what's missing in this area, khoảng trống nghiên cứu, hướng nghiên cứu tương lai. Takes paper ids / "all" / topic via $ARGUMENTS. Output is Vietnamese (terms preserved) to notes/research-gap-<slug>.md.
argument-hint: <paper ids | all | topic>
---

# Research Gap Worker

This skill looks across multiple papers and identifies what is **missing** — open
questions, shared blind spots, and white space — then converts those gaps into
actionable research opportunities. It is cross-paper, and it complements
`knowledge-systemize` (which organizes what exists).

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, Vietnamese-with-preserved-terms output, `notes/` location, and fidelity.

## Procedure
1. **Scope the set.** `$ARGUMENTS` may be paper ids, `all`, or a topic. It reads the
   relevant PDFs and/or reuses existing `notes/<id>-summary.md` and
   `notes/<id>-methodology.md` when present.
2. **Collect per-paper limitations** — each paper's stated limitations and future
   work, plus weaknesses it observes.
3. **Aggregate cross-cutting gaps:** weaknesses that recur across the set, settings
   or regimes nobody tests, assumptions everyone shares, and evaluation/data gaps.
4. **Identify white space:** what no paper in the set attempts at all.
5. **Turn each gap into an opportunity:** for each, state the gap → why it matters →
   a concrete possible direction (and which paper(s) it builds on).
6. **Note ARS hand-off:** for an exhaustive literature-grounded gap analysis it
   recommends `/ars-lit-review` or `/ars-full`.
7. **Glossary, save, preview** to `notes/research-gap-<slug>.md`.

## Output template (`notes/research-gap-<slug>.md`)
```
# Khoảng trống nghiên cứu — <slug>
> Phạm vi: <paper ids / topic> · Worker: research-gap · Ngày: <YYYY-MM-DD>

## Hạn chế theo từng bài (Per-paper limitations)
## Khoảng trống xuyên suốt (Cross-cutting gaps)
## Khoảng trắng (White space — chưa ai làm)
## Cơ hội nghiên cứu (Opportunities)
| Gap | Vì sao quan trọng | Hướng khả thi | Dựa trên bài |
## Thuật ngữ (Glossary)
```
