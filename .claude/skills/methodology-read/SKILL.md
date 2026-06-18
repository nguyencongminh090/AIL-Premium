---
name: methodology-read
description: Performs a deep, critical read of an academic paper's methodology — its problem formulation, formal setup and notation, model/algorithm design, training and data pipeline, loss functions and math, claimed novelty, limitations, and a reproducibility checklist. Use when the user wants to truly understand or scrutinize HOW a method works, not just what it claims. Triggers: methodology read, đọc kỹ phương pháp, phân tích phương pháp, how does the method work, explain the math of paper X, is this reproducible, critique the method. Output is Vietnamese with preserved English terms, saved to notes/<id>-methodology.md.
argument-hint: <paper id | filename | path>
---

# Methodology Read Worker

This skill performs a deep, critical read of a paper's **method**: it reconstructs
how the method works precisely enough to reason about (and ideally reimplement) it,
then assesses assumptions, novelty, limitations, and reproducibility. It is the
analytical counterpart to `paper-summary`.

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, Vietnamese-with-preserved-terms output, `notes/` location, and fidelity.
Critical assessment is encouraged, but every claim must be grounded in the paper —
no fabricated steps, numbers, or weaknesses.

**LaTeX (§7 of shared rule — strictly enforced here).** This skill is the most
math-dense worker. Every equation, loss function, objective, and formula must be
written in LaTeX: inline with `$...$`, display with `$$...$$`. Plain-text math
(`L_rec`, `||x||`, `theta`) is never acceptable in this output.

## Procedure
1. **Resolve the target** from `$ARGUMENTS` per the shared rules; if empty, it asks.
2. **Read in full**, concentrating on the method and experimental-setup sections
   while using the rest of the paper for context.
3. **Reconstruct the method precisely:**
   - problem formulation — notation, inputs/outputs, the objective being optimized;
   - the key components/modules and how they connect;
   - the algorithm or training procedure, step by step;
   - the loss functions and core equations — stated in words **and** in LaTeX
     display math (`$$...$$`), exactly as derived from the paper;
   - the architecture, the data, and the preprocessing;
   - the evaluation protocol (datasets, metrics, baselines, ablations).
4. **Surface assumptions** the method relies on and where they might break.
5. **Assess novelty** versus the prior methods the paper compares against, and
   **limitations** (both author-stated and ones it observes), each marked as such.
6. **Build a reproducibility checklist** — code released? hyperparameters given?
   datasets accessible? compute stated? enough detail to reimplement? — each marked
   yes / partial / no with a short note.
7. **List open questions / unclear steps** that would block reimplementation.
8. **Apply the language convention**, build the glossary, save
   `notes/<id>-methodology.md`, and print a short preview plus the saved path.

## Output template (`notes/<id>-methodology.md`)
```
# Đọc phương pháp — <id> · <Title>
> Nguồn: <filename> · Worker: methodology-read · Ngày: <YYYY-MM-DD>

## Phát biểu bài toán (Problem formulation & notation)
## Tổng quan pipeline (Method overview)
## Các thành phần chính (Key components)
## Thuật toán / quy trình (Algorithm / training procedure)
## Hàm mất mát & công thức (Loss & core equations)
## Dữ liệu & tiền xử lý (Data & preprocessing)
## Giao thức đánh giá (Evaluation protocol)
## Giả định (Assumptions) & rủi ro khi giả định sai
## Điểm mới (Novelty vs prior methods)
## Hạn chế (Limitations — author-stated / observed)
## Checklist tái lập (Reproducibility): code / hyperparams / data / compute / đủ để reimplement?
## Câu hỏi mở (Open questions)
## Thuật ngữ (Glossary)
```
