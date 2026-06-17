---
name: problem-expand
description: Zooms out from a paper (or a topic) to situate and generalize its problem — the broader problem class it belongs to, its abstract formulation, the assumptions/constraints that could be relaxed for a more general problem, neighboring/related problems, where it sits in the wider research landscape, and the open sub-problems it implies. This is the "khái quát / nhìn rộng / hệ thống hóa vấn đề" worker. Use for: expand the problem, generalize this problem, broaden the scope, bigger picture of paper X, khái quát vấn đề, nhìn rộng vấn đề, hệ thống hóa vấn đề. Output is Vietnamese (terms preserved) to notes/<id>-expand.md.
argument-hint: <paper id | filename | path | topic in your own words>
---

# Problem Expand Worker (Khái quát / Nhìn rộng vấn đề)

This skill takes the narrow, specific problem a paper solves and **zooms out**: it
generalizes the problem, situates it in the field, and surfaces the larger structure
of related and open problems around it. It is conceptual — it does not summarize the
paper's solution (that is `paper-summary`).

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, Vietnamese-with-preserved-terms output, `notes/` location, and fidelity.

## Procedure
1. **Resolve the input.** `$ARGUMENTS` may be a paper reference (resolve + read) or a
   topic phrase (work from the topic plus any existing `notes/` analysis). If empty,
   it asks for a paper or topic.
2. **State the specific problem** the paper/topic actually tackles, precisely.
3. **Generalize it:** name the broader **problem class**, give an abstract
   formulation, and list the assumptions/constraints that — if relaxed — yield a
   more general problem.
4. **Map neighboring problems:** adjacent or related problems and how they connect to
   this one (specializations, generalizations, duals, prerequisites).
5. **Position in the landscape:** where this sits among approaches and sub-fields,
   and what schools/lines of work it touches.
6. **Surface open sub-problems** and research directions the framing implies.
7. **Glossary, save, preview** to `notes/<id>-expand.md`.

## Output template (`notes/<id>-expand.md`)
```
# Khái quát vấn đề — <id | topic> · <Title>
> Nguồn: <filename | topic> · Worker: problem-expand · Ngày: <YYYY-MM-DD>

## Vấn đề cụ thể (Specific problem)
## Lớp vấn đề tổng quát (General problem class) & phát biểu trừu tượng
## Giả định có thể nới lỏng (Assumptions that could be relaxed)
## Vấn đề lân cận (Neighboring / related problems)
## Định vị trong bức tranh lớn (Landscape positioning)
## Vấn đề con còn mở (Open sub-problems & directions)
## Thuật ngữ (Glossary)
```
