---
name: paper-overview
description: Gives a high-altitude orientation of an academic paper — its one-line thesis, why it matters, headline results, and how it positions itself against prior work — to help decide whether and how deeply to read it. Lighter and more strategic than paper-summary (which condenses every section). Use for: overview of 003, what's this paper about, is paper X worth reading, give me the gist, tổng quan bài báo, bài này nói về gì, có đáng đọc không. Output is Vietnamese with preserved English terms, saved to notes/<id>-overview.md.
argument-hint: <paper id | filename | path | all>
---

# Paper Overview Worker

This skill gives a bird's-eye orientation of a paper so the user can decide whether,
and how deeply, to read it. It stays high-altitude — it does **not** condense every
section (that is `paper-summary`) nor scrutinize the method (that is
`methodology-read`).

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, Vietnamese-with-preserved-terms output, `notes/` location, and fidelity.

## Procedure
1. **Resolve the target** from `$ARGUMENTS` per the shared input rules; if empty,
   it lists `papers/` and asks. For `all`, it produces one overview per paper.
2. **Read strategically.** It reads the abstract, introduction, conclusion, figure
   captions, and section headings first, skimming the method only enough to state
   the approach. Full-text deep reading is out of scope here.
3. **Extract the orientation signals:** one-line thesis, the problem and motivation,
   the approach in 1–2 sentences, the headline results, the paper's positioning
   versus prior work, its claimed novelty, who should care, and a recommended
   read-depth.
4. **Apply the language convention** and build the glossary.
5. **Save and preview.** It writes `notes/<id>-overview.md` using the template,
   then prints a short preview plus the saved path.

## Output template (`notes/<id>-overview.md`)
```
# Tổng quan — <id> · <Title>
> Nguồn: <filename> · Worker: paper-overview · Ngày: <YYYY-MM-DD>

## Một câu (One-line thesis)
## Dành cho ai / khi nào đọc (Who & when to read)
## Bối cảnh & động lực (Context & motivation)
## Cách tiếp cận (Approach — 1–2 câu)
## Kết quả nổi bật (Headline results)
## Định vị so với công trình trước (Positioning vs prior work)
## Điểm mới tuyên bố (Claimed novelty)
## Khuyến nghị mức độ đọc (Read-depth: skim / read method / deep read)
## Thuật ngữ (Glossary)
```
