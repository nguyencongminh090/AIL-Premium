---
name: latex-fix
description: Reviews and fixes LaTeX formatting in notes/ artifacts produced by other Workers. Detects plain-text math that should be LaTeX (e.g. L_total, ||x||, theta, argmin), malformed delimiters, display equations that are not on their own line, and other violations of §7 of research-conventions.md — then rewrites the file in-place and reports every change. Use for: fix LaTeX, review LaTeX, sửa LaTeX, kiểm tra công thức, fix math formatting, latex-fix 003, fix all notes. Takes a notes/ file path, a paper id (fixes all notes/<id>-*.md for that paper), or "all" (fixes every file in notes/) via $ARGUMENTS.
argument-hint: <notes/ file path | paper id | all>
---

# LaTeX Fix Worker

This skill audits and repairs LaTeX formatting in `notes/` artifacts. It enforces
§7 of `.claude/rules/research-conventions.md` after the fact — catching violations
that slipped through during initial generation. It rewrites files in-place and
always reports a structured diff so the user knows exactly what changed.

## Conventions
This skill treats `.claude/rules/research-conventions.md` §7 as its primary
specification. It does **not** change prose, structure, Vietnamese phrasing, or
glossary entries — only mathematical notation. All interaction is in Vietnamese.

## Violation catalogue (what it hunts for)
The worker scans for the following patterns, in order of severity:

1. **Plain-text math — no delimiters at all**
   - Subscripted identifiers outside LaTeX: `L_total`, `x_i`, `W_ij`, `f_theta`
   - Greek letters spelled out: `theta`, `alpha`, `beta`, `lambda`, `sigma`,
     `mu`, `epsilon`, `phi`, `psi`, `omega`, `rho`, `tau`, `eta`, `delta`,
     `gamma`, `pi` (when used as math variables, not prose words)
   - Norms written as `||x||`, `|x|`, `||W||_F`
   - `argmin`, `argmax`, `softmax`, `sigmoid` used as math operators outside `$`
   - Fractions / divisions clearly in a math context: `a/b` where `a`, `b` are
     variable names

2. **Wrong delimiter choice**
   - Standalone equation on its own line wrapped in `$...$` → should be `$$...$$`
   - `$$...$$` used mid-sentence (inline) → should be `$...$`

3. **Malformed LaTeX**
   - Unmatched `$` delimiters
   - ASCII substitutes inside existing `$...$`: `||` instead of `\|`, `*` instead
     of `\cdot`, `->` instead of `\rightarrow`, `<=` instead of `\leq`,
     `>=` instead of `\geq`, `!=` instead of `\neq`

4. **Non-standard notation inside `$...$`**
   - `argmin` / `argmax` without backslash → `\arg\min` / `\arg\max`
   - `norm` or `||` for norms → `\|\cdot\|`
   - Superscripts / subscripts without braces when more than one character:
     `x^{-1}` is correct, `x^-1` is not

## Procedure
1. **Resolve the target.**
   - If `$ARGUMENTS` is a path starting with `notes/`: operate on that single file.
   - If `$ARGUMENTS` is a paper id (e.g. `003`): collect every `notes/003-*.md`.
   - If `$ARGUMENTS` is `all`: collect every `.md` file in `notes/`.
   - If `$ARGUMENTS` is empty: list `notes/` contents and ask which to fix.
2. **Read each target file.**
3. **Scan for violations** using the catalogue above. For each violation it records:
   - location (section heading + approximate line context),
   - the original text,
   - the corrected LaTeX.
4. **Apply fixes** — rewrite the file with all corrections in one pass. It does not
   touch prose, structure, glossary tables, Mermaid code blocks, or file headers.
   Inside Mermaid fenced blocks (`\`\`\`mermaid ... \`\`\``), it makes no changes.
5. **Write the fixed file** back to the same path (overwrite).
6. **Report** a structured fix-log in chat (see template below). If a file had no
   violations, it says so explicitly — it does not silently skip.

## Fix-log template (chat output)
```
## Kết quả latex-fix — <target>
Ngày: <YYYY-MM-DD>

### <notes/filename.md>
| # | Vị trí (mục) | Gốc | Sửa thành |
|---|---|---|---|
| 1 | Hàm mất mát | `L_total = L_rec + L_perceptual` | `$\mathcal{L}_{total} = \mathcal{L}_{rec} + \mathcal{L}_{perceptual}$` |
| 2 | Phát biểu bài toán | `theta*` | `$\theta^*$` |

Tổng: <N> lỗi đã sửa.

### <notes/filename2.md>
Không phát hiện vi phạm LaTeX.
```

## Boundaries
- It only fixes LaTeX in `notes/` files — not in SKILL.md files, rules, or PDFs.
- It does not rewrite or improve prose. If a sentence is grammatically fine but
  happens to contain a math term, it fixes only the math term.
- When a fix is ambiguous (e.g. `pi` could be the Greek letter or the English word
  "pi" in prose), it flags it in the report as **"cần xác nhận (needs confirmation)"**
  rather than applying the change automatically.
- If a file has more than 20 violations, it reports the first 20, applies all fixes,
  and notes the total count — it does not truncate the fixes, only the report preview.
