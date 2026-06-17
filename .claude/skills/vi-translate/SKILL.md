---
name: vi-translate
description: Academic Vietnamese translator. Translates a passage, a section, or a whole academic paper into Vietnamese in academic register, keeping original English technical terms inline and appending a glossary at the end. Faithful and complete — it translates, it does not summarize. Use when the user asks to translate, dịch, dịch bài báo, dịch sang tiếng Việt, translate paper X to Vietnamese, or pastes English academic text to translate. Input via $ARGUMENTS is a paper id/filename/path OR pasted text. Whole-paper translations are saved to notes/<id>-vi.md.
argument-hint: <paper id | filename | path | pasted English text>
---

# Vietnamese Academic Translator Worker

This skill translates academic text into Vietnamese, faithfully and in full. Unlike
the other Workers, it renders prose **continuously** rather than analyzing it — it
must not summarize, omit, or reorder content.

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, terminology handling, `notes/` location, and fidelity.

## Procedure
1. **Identify the source.** If `$ARGUMENTS` is a paper reference (id / filename /
   path), it resolves and reads the PDF. If `$ARGUMENTS` is pasted English prose,
   it translates that text directly. If `$ARGUMENTS` is empty, it asks for either
   a paper reference or the text to translate.
2. **Scope a full paper.** For a whole PDF it translates section by section in
   original order. If the paper is long, it may confirm scope (whole paper vs a
   named section) before starting, but defaults to translating what was given.
3. **Translate under these rules** (in addition to the shared language rule):
   - academic register, faithful and complete — no summarizing or omission;
   - preserve every technical term as `bản dịch (English term)` on first occurrence
     within each section;
   - keep equations, symbols, in-text citations, and figure/table references
     unchanged;
   - do **not** translate proper nouns, dataset names, model names, or method names;
   - preserve paragraph breaks and the heading hierarchy.
4. **Append the glossary** of every preserved term.
5. **Deliver.** For a whole-paper translation it saves `notes/<id>-vi.md` and prints
   the saved path plus the first lines as preview. For a pasted snippet it returns
   the translation inline and offers to save it.

## Output template (`notes/<id>-vi.md`, whole-paper)
```
# Bản dịch tiếng Việt — <id> · <Title>
> Nguồn: <filename> · Worker: vi-translate · Ngày: <YYYY-MM-DD>

## <Tên mục gốc>
<bản dịch trung thành, thuật ngữ gốc giữ trong ngoặc>
...
## Thuật ngữ (Glossary)
```
