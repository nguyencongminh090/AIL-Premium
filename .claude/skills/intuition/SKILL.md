---
name: intuition
description: Explains the core idea of a paper in plain, intuitive language — stripping jargon, using an analogy and a small worked example, and contrasting with the naive approach — to build understanding before a deep read. Use for: intuition, explain simply, ELI5, explain the idea of 003 like I'm new, what's the intuition behind paper X, giải thích đơn giản, trực giác, giải thích dễ hiểu. Output is Vietnamese with English terms preserved but always explained in plain words; saved to notes/<id>-intuition.md.
argument-hint: <paper id | filename | path>
---

# Intuition Worker

This skill explains a paper's core idea simply, to build intuition before a rigorous
read. It is deliberately accessible — analogies and toy examples over formalism. For
the precise mechanics the user should use `methodology-read` or `pipeline-extract`.

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, `notes/` location, and fidelity. It still preserves English technical
terms, but each one is **immediately explained in plain words** rather than assumed.

## Procedure
1. **Resolve the target** from `$ARGUMENTS` per the shared rules; if empty, it asks.
2. **Read enough** to grasp the core idea — abstract, introduction, the method
   overview, and the key figure.
3. **State the one core idea** in a single plain sentence.
4. **Explain the key insight** — *why* it works — using a concrete analogy.
5. **Walk a tiny example** with toy numbers or a simple scenario. Any math in the
   example — even simplified — must use LaTeX (`$...$`), not raw ASCII.
6. **Contrast with the naive approach** to show what the idea buys.
7. **Add "Một câu cho người mới"** (one sentence for a newcomer) and
   **"Khi nào trực giác này sai"** (when the intuition breaks down).
8. **Glossary, save, preview** to `notes/<id>-intuition.md`.

## Output template (`notes/<id>-intuition.md`)
```
# Trực giác — <id> · <Title>
> Nguồn: <filename> · Worker: intuition · Ngày: <YYYY-MM-DD>

## Ý tưởng cốt lõi trong một câu (Core idea in one sentence)
## Vì sao nó hiệu quả — phép ẩn dụ (Why it works — analogy)
## Ví dụ nhỏ (Tiny worked example)
## So với cách ngây thơ (Vs the naive approach)
## Một câu cho người mới (One sentence for a newcomer)
## Khi nào trực giác này sai (When the intuition breaks)
## Thuật ngữ (Glossary)
```
