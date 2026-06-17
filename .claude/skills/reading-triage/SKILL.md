---
name: reading-triage
description: Ranks and queues the papers in papers/ by relevance to a research question or focus the user provides, so they know what to read first. For each paper it gives a relevance score, a one-line rationale, a suggested action (deep-read / skim / skip), and which Worker to run next. Cross-paper. Use for: triage, what should I read first, reading order, prioritize papers, rank papers by relevance, xếp thứ tự đọc, đọc cái nào trước, ưu tiên đọc bài nào. Takes the research question/focus via $ARGUMENTS. Output is Vietnamese (terms preserved) to notes/reading-triage-<slug>.md.
argument-hint: <your research question or focus>
---

# Reading Triage Worker

This skill prioritizes the reading list: given a research question, it scores every
paper in `papers/` for relevance and tells the user what to read first and how. It
is a fast, abstract-level pass — not a deep read of any single paper.

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for the `notes/`
location, Vietnamese-with-preserved-terms output, and fidelity.

## Procedure
1. **Get the focus.** It reads the research question/focus from `$ARGUMENTS`. Triage
   is meaningless without a target, so if `$ARGUMENTS` is empty it asks for the
   question before proceeding.
2. **List the candidates.** It lists every paper in `papers/` (id + title from the
   filename).
3. **Cheap relevance pass.** For each paper it reads the abstract plus the
   introduction/conclusion (not the full text) to judge fit to the question.
4. **Score and recommend.** For each paper it assigns a relevance level
   (Cao / Trung bình / Thấp — High/Med/Low), a one-line rationale, a suggested action
   (đọc kỹ / lướt / bỏ qua), and which Worker to run next (`paper-overview`,
   `paper-summary`, `methodology-read`, `pipeline-extract`, …).
5. **Rank.** It sorts the table by relevance and proposes a concrete reading order.
6. **Glossary, save, preview** to `notes/reading-triage-<slug>.md` (slug from the
   question).

## Output template (`notes/reading-triage-<slug>.md`)
```
# Phân loại ưu tiên đọc — <slug>
> Câu hỏi: "<research question>" · Worker: reading-triage · Ngày: <YYYY-MM-DD>

## Bảng xếp hạng (Ranked)
| Hạng | Bài | Mức liên quan | Lý do (1 dòng) | Hành động | Worker kế tiếp |

## Thứ tự đọc đề xuất (Suggested reading order)
1. ...

## Thuật ngữ (Glossary)
```
