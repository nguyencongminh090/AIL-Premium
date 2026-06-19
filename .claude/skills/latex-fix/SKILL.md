---
name: latex-fix
description: Reviews and fixes LaTeX formatting in notes/ artifacts for cross-platform rendering (VS Code KaTeX + GitHub MathJax). Detects plain-text math (L_total, ||x||, theta, argmin), wrong delimiters, malformed notation, and platform incompatibilities — \tag{} partial in KaTeX, \label{}/\ref{}/\eqref{} unsupported in KaTeX, ```math blocks unsupported in VS Code, \[...\]/\(...\) delimiters unsupported in VS Code, \boldsymbol{} edge cases. Rewrites files in-place and reports every change. Use for: fix LaTeX, review LaTeX, sửa LaTeX, kiểm tra công thức, fix \tag, fix delimiters, latex-fix 003, fix all notes. Takes a notes/ file path, paper id, or "all" via $ARGUMENTS.
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

2. **Wrong delimiter choice / display block formatting**
   - Standalone equation on its own line wrapped in `$...$` → should be `$$...$$`
   - `$$...$$` used mid-sentence (inline) → should be `$...$`
   - `$$...$$` display block **not surrounded by blank lines** — markdown-it (the
     parser used by VS Code and many editors) requires an empty line before and after
     a display math block to recognise it as math; without blank lines, the parser
     treats the content as plain markdown, `\mathbf{P}` becomes **P**, and the whole
     block renders as raw text.
     Fix: ensure one blank line before the opening `$$` and one blank line after the
     closing `$$`.
   - Preferred display math format for maximum robustness across renderers:
     ```
     $$
     \text{equation here}
     $$
     ```
     Single-line `$$equation$$` is valid in standard VS Code/GitHub but fails in
     some third-party renderers. Flag single-line blocks as **"cần xác nhận"** if
     the file was authored for use outside VS Code/GitHub.

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

5. **Platform rendering incompatibilities**

   Notes are read in two contexts with different engines:
   - **VS Code Markdown preview** — **KaTeX** (~v0.13–0.16): fast subset of LaTeX;
     unsupported commands silently break the entire `$$` block.
   - **GitHub** — **MathJax 4.1.1**: full TeX; supports more commands.

   Target: the safe intersection. Fix anything that fails in VS Code, even if it
   works on GitHub.

   | Pattern | GitHub | VS Code | Fix |
   |---------|--------|---------|-----|
   | `\tag{N}` inside `$$` | ✓ | ⚠️ partial | Remove `\tag{N}`; append `*(phương trình N trong paper)*` after closing `$$` |
   | `\label{...}` | ✓ | ✗ | Remove silently |
   | `\ref{...}` / `\eqref{...}` | ✓ | ✗ | Remove or replace with plain equation number |
   | `` ```math...``` `` fenced block | ✓ | ✗ | Replace with `$$...$$` block |
   | `\[...\]` delimiter | ✓ | ✗ | Replace delimiter with `$$...$$` |
   | `\(...\)` delimiter | ✓ | ✗ | Replace delimiter with `$...$` |
   | `\boldsymbol{...}` | ✓ | ⚠️ edge cases | Replace with `\mathbf{}` for latin letters; `\pmb{}` for greek/symbols |
   | `\operatorname{custom}` | ✓ | ⚠️ version-dependent | Replace with `\mathrm{custom}` — supported in all KaTeX versions without amsopn extension; use only for custom single-word operators (score, attn, etc.); predefined operators (`\max`, `\min`, `\arg`) are always fine |
   | `\text{<non-ASCII>}` inside `\begin{cases}` / `\begin{array}` | ⚠️ | ⚠️ unstable | Non-ASCII Unicode (Vietnamese diacritics, CJK, etc.) in `\text{}` within tabular math environments is unstable across KaTeX versions — may render blank, garbled, or break the whole block. **Fix:** keep condition column pure math; move Vietnamese/non-ASCII annotations to prose outside the `$$` block. See pattern below. |
   | `\xrightarrow{\text{<long>}}` | ✓ | ✓ (may overflow) | Flag only if visually broken; suggest `\longrightarrow \quad \text{(...)}` |

   Example fixes:
   ```
   \tag{1} removal:
     Before: $$\mathcal{L} = \lambda_1 \mathcal{L}_{rec} \tag{1}$$
     After:  $$\mathcal{L} = \lambda_1 \mathcal{L}_{rec}$$
             *(phương trình 1 trong paper)*

   \boldsymbol{} replacement:
     Before: \boldsymbol{v}      →  After: \mathbf{v}     (latin letter)
     Before: \boldsymbol{\theta} →  After: \pmb{\theta}   (greek symbol)

   Delimiter replacement:
     Before: \[E = mc^2\]        →  After: $$E = mc^2$$
     Before: \(E = mc^2\)        →  After: $E = mc^2$

   \text{non-ASCII} inside \begin{cases} — move annotation to prose:
     Before:
       $$f(x) = \begin{cases} 1 & \text{nếu } x > 0 \\ 0 & \text{ngược lại} \end{cases}$$

     After:
       $$f(x) = \begin{cases} 1 & x > 0 \\ 0 & \text{otherwise} \end{cases}$$
       trong đó trường hợp đầu áp dụng khi $x > 0$, trường hợp sau khi $x \leq 0$.

     Rule: condition column → pure math or ASCII-only \text{}; Vietnamese/non-ASCII
     annotations → prose sentence after the closing $$.
   ```

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
