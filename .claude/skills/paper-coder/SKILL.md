---
name: paper-coder
description: Generates a Jupyter Notebook (.ipynb) from an academic paper — either a full reproduction of the method from scratch (Mode 1: reproduce) or a run-results notebook that loads the authors' pretrained weights and reproduces their reported numbers (Mode 2: run-results). Searches GitHub / Papers With Code / HuggingFace for official code before writing from scratch. Always includes environment setup (pip installs, GPU check, Colab detection) and parallel multithreaded dataset/weight downloads. Output goes to notebooks/. Use for: code the paper, implement 003, reproduce results, run pretrained model, viết code, tái lập thí nghiệm, chạy kết quả bài báo. Takes paper id + optional mode + optional repo URL via $ARGUMENTS.
argument-hint: <paper id> [reproduce|run-results] [repo-url]
---

# Paper Coder Worker

This skill produces a ready-to-run Jupyter Notebook for an academic paper. It has
two modes that the user selects explicitly (or is asked to choose):

- **Mode 1 — `reproduce`:** Full code reproduction of the paper's method. Searches
  for an existing implementation first; clones and adapts it if found; writes from
  scratch if not.
- **Mode 2 — `run-results`:** Loads the authors' pretrained weights, sets up the
  environment per the official repo, and runs inference / evaluation to reproduce
  the reported numbers.

The notebook is always designed to run on **Google Colab or a rented GPU instance**
(not local): it detects the runtime, installs all dependencies in cells, and uses
parallel multithreaded download for datasets and weights.

## Conventions
This skill treats `.claude/rules/research-conventions.md` as binding for input
resolution, Vietnamese conversational output, and fidelity. **Exception:** the
Jupyter Notebook itself (`.ipynb`) is written in **English** — all cell markdown,
comments, and variable names are English, since the notebook is executable code
intended for sharing and reproducibility, not a Vietnamese analysis artifact.
The chat interaction (plan, progress, report) remains Vietnamese per the shared rule.

## Input resolution
`$ARGUMENTS` is parsed left to right:
- **Paper id / path** (required): resolved per the shared input rules.
- **Mode** (optional keyword): `reproduce` or `run-results`. If absent, it shows
  the two options and asks the user to choose before doing anything else.
- **Repo URL** (optional): a GitHub / HuggingFace URL the user already knows. If
  provided, it skips the search step and uses this URL directly.

Example invocations:
```
003                                        → asks mode
003 reproduce                              → Mode 1, search for repo
003 run-results                            → Mode 2, search for repo
003 reproduce https://github.com/foo/bar   → Mode 1, use known repo
```

## Preparation (both modes)
1. **Read the paper.** It checks for `notes/<id>-pipeline.md` and
   `notes/<id>-methodology.md` first (reuse existing Worker output if available).
   If absent, it reads the PDF directly, focusing on the method, architecture,
   training, and evaluation sections.
2. **Extract implementation facts:**
   - model architecture and key hyper-parameters;
   - dataset(s) name, size, download source;
   - evaluation metrics and protocol;
   - any official code / pretrained weights URLs mentioned in the paper.
3. **Search for code** (WebSearch + WebFetch):
   - Query Papers With Code (`paperswithcode.com`) for the paper title.
   - Query GitHub for `<paper title> implementation` / `<paper acronym>`.
   - Check the paper's project page if one is linked.
   - Check HuggingFace Hub for pretrained weights.
   It records what it finds (official repo / third-party / nothing) and tells the
   user before writing the notebook.

---

## Mode 1 — Reproduce

### Goal
A notebook that re-implements the paper's method end-to-end: data loading →
preprocessing → model definition → training loop → evaluation → results table.

### Strategy
- **If an official or high-quality third-party repo is found:** clone it, adapt
  imports and paths for Colab, add missing environment cells, and wrap the training
  command in a notebook cell with progress logging.
- **If no usable repo is found:** write the full implementation from scratch,
  strictly following the paper's pipeline. Every architectural choice is annotated
  with the paper section it comes from (e.g. `# Section 3.2 — Hyper-Ray encoder`).

### Notebook structure (Mode 1)
```
## 0. Runtime & GPU Check
## 1. Install Dependencies
## 2. Clone Repository  [if repo found; skip if writing from scratch]
## 3. Dataset Download  [multithreaded — see pattern below]
## 4. Data Preprocessing & Dataloader
## 5. Model Architecture  [annotated with paper section refs]
## 6. Loss Functions & Objectives
## 7. Training Loop
## 8. Evaluation
## 9. Results & Visualisation
```

---

## Mode 2 — Run Results

### Goal
A notebook that sets up the official environment, downloads the authors' pretrained
weights, loads the model, runs inference or evaluation, and reproduces the numbers
the paper reports.

### Strategy
1. Find the official repo and its README / setup instructions.
2. Follow the authors' exact setup (Python version, framework version, dependencies).
3. Download pretrained weights with a progress bar.
4. Run the evaluation command / script the authors provide, wrapped in notebook
   cells.
5. Display results alongside the paper's reported numbers for comparison.

### Notebook structure (Mode 2)
```
## 0. Runtime & GPU Check
## 1. Install Dependencies  [from official repo requirements]
## 2. Clone Official Repository
## 3. Download Pretrained Weights  [multithreaded if multiple files]
## 4. Environment Configuration  [paths, config files, env vars]
## 5. Load Model & Weights
## 6. Dataset Download / Sample Data  [multithreaded if large]
## 7. Inference / Evaluation
## 8. Results vs Paper  [side-by-side comparison table]
```

---

## Using the script (`nb_builder.py`)

All boilerplate cells (GPU check, pip install, parallel downloader) are pre-built
in `.claude/skills/paper-coder/scripts/nb_builder.py`. This skill **must** use the
script to write the `.ipynb` file — never write raw notebook JSON by hand.

### How it works
1. This skill gathers all paper-specific facts (dependencies, URLs, architecture
   code, section text).
2. It assembles a **JSON spec** (see schema below) in a temporary file at
   `/tmp/nb_spec_<id>_<mode>.json` (id + mode in the name so parallel workers
   for the same paper never collide).
3. It runs the builder script via Bash:
   ```bash
   python .claude/skills/paper-coder/scripts/nb_builder.py /tmp/nb_spec_<id>_<mode>.json
   ```
4. The script writes the finished `.ipynb` to `notebooks/<id>-<mode>.ipynb` and
   prints a one-line confirmation. This skill reads that confirmation and reports
   to the user.

### JSON spec schema
```json
{
  "paper_id":    "003",
  "title":       "Full paper title",
  "mode":        "reproduce",
  "output":      "notebooks/003-reproduce.ipynb",
  "repo_url":    "https://github.com/author/repo",
  "dependencies": ["torch>=2.0", "torchvision", "numpy", "matplotlib", "tqdm"],
  "dataset_files": [
    {"url": "https://...", "dest": "data/train.zip"},
    {"url": "https://...", "dest": "data/val.zip"}
  ],
  "weight_files": [
    {"url": "https://...", "dest": "weights/checkpoint.pth"}
  ],
  "hf_repo": "author/model-name",
  "sections": [
    {
      "title":    "Data Preprocessing & Dataloader",
      "markdown": "Explanation of what this section implements...",
      "code":     "# full Python code for this section"
    },
    {
      "title":    "Model Architecture",
      "markdown": "Implements Section 3.2 — Hyper-Ray Encoder.",
      "code":     "class HyperRayEncoder(nn.Module):\n    ..."
    }
  ],
  "manual_steps": [
    "Accept the dataset license at https://... before running cell 4."
  ]
}
```

**Rules for populating the spec:**
- `dependencies`: include every pip package needed; add version pins where the
  paper or repo specifies them.
- `dataset_files` / `weight_files`: populate from URLs found in the paper or
  repo README; leave as `[]` if none found (the script writes placeholder cells).
- `sections`: one entry per major section of the notebook body. The `code` field
  is the **complete, working Python code** for that section — not a stub.
  For Mode 1 with a cloned repo, the code is the adapted invocation; for Mode 1
  from scratch or Mode 2, it is the full implementation.
- `manual_steps`: list anything the user must do by hand that cannot be automated.

### What the script handles automatically (do not duplicate in sections[])
The script always inserts these cells before the `sections` array:
- Runtime & Colab detection
- `!pip install` cell from `dependencies`
- `git clone` cell (if `repo_url` given)
- Parallel download utility function (`download_file` + `parallel_download`)
- Dataset download cell from `dataset_files`
- Weight download cell from `weight_files` / `hf_repo` (Mode 2 only)

---

## Output
- **File:** `notebooks/<id>-reproduce.ipynb` or `notebooks/<id>-run-results.ipynb`,
  written by the script.
- **Chat report (Vietnamese):** after the script confirms success, it prints:
  - what repo was found (or "written from scratch"),
  - the notebook path,
  - a brief section map,
  - any manual steps from `manual_steps`.

## Failure modes & recovery
- **Repo found but private / paywalled:** it notes this and falls back to writing
  from scratch using the paper.
- **Dataset requires login / license agreement:** it writes a placeholder cell with
  the manual download instruction and the official URL, rather than silently failing.
- **Paper lacks architectural detail:** it notes every missing detail with a
  `# TODO: paper does not specify — verify` comment and suggests running
  `methodology-read` first.
- **Weights URL is broken:** it tries alternative sources (HuggingFace, Google
  Drive backup links in the repo README) and reports which it used.
