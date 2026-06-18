#!/usr/bin/env python3
"""
nb_builder.py — Jupyter Notebook builder for paper-coder skill.

Reads a JSON spec from a file path (first argument) or stdin, and writes a
valid nbformat-4 .ipynb file. All boilerplate cells (GPU check, package
install, parallel download utility) are pre-baked here so the LLM only needs
to supply paper-specific content in the spec.

Concurrency-safe: build_notebook() is a pure function with no global state.
Multiple parallel invocations are safe as long as each uses a distinct spec
file path and a distinct "output" value in the spec — which is guaranteed when
the caller names the spec file /tmp/nb_spec_<id>_<mode>.json and the output
notebooks/<id>-<mode>.ipynb (different paper ids or different modes → no
shared files, no locks needed).

Usage:
    python nb_builder.py /tmp/nb_spec_003_reproduce.json
    cat spec.json | python nb_builder.py

Spec schema (all fields except paper_id, title, mode, output are optional):
{
  "paper_id":    "003",
  "title":       "Geometric Viewpoint Learning ...",
  "mode":        "reproduce" | "run-results",
  "output":      "notebooks/003-reproduce.ipynb",
  "repo_url":    "https://github.com/author/repo",   // optional
  "dependencies": ["torch", "torchvision", ...],     // pip packages
  "dataset_files": [                                 // for parallel download
    {"url": "https://...", "dest": "data/train.zip"},
    ...
  ],
  "weight_files": [                                  // run-results mode
    {"url": "https://...", "dest": "weights/ckpt.pth"},
    ...
  ],
  "hf_repo":     "author/model-name",               // HuggingFace repo id
  "sections": [                                      // paper-specific cells
    {
      "title":    "Model Architecture",              // becomes a ## heading
      "markdown": "Explanation text ...",            // optional markdown cell
      "code":     "class MyModel(nn.Module): ..."   // optional code cell
    },
    ...
  ],
  "manual_steps": [                                  // things user must do manually
    "Accept dataset license at https://...",
    ...
  ]
}
"""

import json
import sys
import textwrap
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Notebook cell helpers
# ---------------------------------------------------------------------------

def md_cell(source: str) -> dict:
    lines = [l + "\n" for l in source.splitlines()]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines,
    }


def code_cell(source: str) -> dict:
    lines = [l + "\n" for l in source.splitlines()]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines,
    }


def section_header(title: str, level: int = 2) -> dict:
    prefix = "#" * level
    return md_cell(f"{prefix} {title}")


# ---------------------------------------------------------------------------
# Boilerplate cells (always included)
# ---------------------------------------------------------------------------

CELL_RUNTIME_CHECK = code_cell(textwrap.dedent("""\
    import os, sys, subprocess

    # ── Detect runtime ────────────────────────────────────────────────────
    IN_COLAB = False
    try:
        import google.colab
        IN_COLAB = True
        print("Runtime: Google Colab")
        # Uncomment to mount Google Drive for persistence:
        # from google.colab import drive
        # drive.mount('/content/drive')
    except ImportError:
        print("Runtime: Non-Colab (rented GPU / local)")

    # ── GPU check ────────────────────────────────────────────────────────
    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("⚠️  No GPU detected — training will be slow on CPU.")

    print(f"Python: {sys.version.split()[0]}")
"""))

PARALLEL_DOWNLOAD_CODE = textwrap.dedent("""\
    import requests
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from tqdm.notebook import tqdm

    def download_file(url: str, dest, chunk_size: int = 1 << 20):
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            return dest                           # skip if already on disk
        r = requests.get(url, stream=True, timeout=120)
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(dest, 'wb') as f, tqdm(
            desc=dest.name, total=total, unit='B',
            unit_scale=True, leave=False
        ) as bar:
            for chunk in r.iter_content(chunk_size):
                f.write(chunk)
                bar.update(len(chunk))
        return dest

    def parallel_download(file_list: list, max_workers: int = 8):
        \"\"\"file_list: list of (url, dest_path) tuples.\"\"\"
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(download_file, url, dest): dest
                       for url, dest in file_list}
            for fut in tqdm(as_completed(futures), total=len(futures),
                            desc='Downloading', unit='file'):
                dest = futures[fut]
                try:
                    fut.result()
                    print(f"  ✓  {Path(dest).name}")
                except Exception as e:
                    print(f"  ✗  {Path(dest).name}: {e}")
""")

HF_DOWNLOAD_CODE = textwrap.dedent("""\
    # Alternative: HuggingFace Hub download (parallel internally)
    # !pip install -q huggingface_hub
    # from huggingface_hub import snapshot_download
    # snapshot_download(repo_id="{hf_repo}", local_dir="weights/")
""")


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_notebook(spec: dict) -> dict:
    paper_id   = spec.get("paper_id", "???")
    title      = spec.get("title", "Unknown Paper")
    mode       = spec.get("mode", "reproduce")
    repo_url   = spec.get("repo_url", "")
    deps       = spec.get("dependencies", [])
    dataset_files = spec.get("dataset_files", [])
    weight_files  = spec.get("weight_files", [])
    hf_repo       = spec.get("hf_repo", "")
    sections      = spec.get("sections", [])
    manual_steps  = spec.get("manual_steps", [])

    mode_label = "Reproduce" if mode == "reproduce" else "Run Results"
    date_str   = datetime.today().strftime("%Y-%m-%d")

    cells = []

    # ── Title ──────────────────────────────────────────────────────────────
    cells.append(md_cell(
        f"# [{paper_id}] {title}\n"
        f"> **Mode:** {mode_label} &nbsp;·&nbsp; **Generated:** {date_str}\n\n"
        + (f"> **Repository:** [{repo_url}]({repo_url})\n" if repo_url else "")
    ))

    # ── 0. Runtime & GPU check ─────────────────────────────────────────────
    cells.append(section_header("0. Runtime & GPU Check"))
    cells.append(CELL_RUNTIME_CHECK)

    # ── 1. Install dependencies ────────────────────────────────────────────
    cells.append(section_header("1. Install Dependencies"))
    if deps:
        pip_line = "!pip install -q " + " ".join(deps)
        cells.append(code_cell(pip_line))
    else:
        cells.append(code_cell("# No additional dependencies specified\n# !pip install -q <packages>"))

    # ── 2. Clone repository (if repo_url given) ────────────────────────────
    if repo_url:
        cells.append(section_header("2. Clone Repository"))
        repo_name = repo_url.rstrip("/").split("/")[-1]
        cells.append(code_cell(
            f"import os\n"
            f"if not os.path.exists('{repo_name}'):\n"
            f"    !git clone {repo_url}\n"
            f"os.chdir('{repo_name}')\n"
            f"print('Repo ready.')"
        ))

    # ── 3. Parallel download utility ───────────────────────────────────────
    cells.append(section_header("3. Download Utilities"))
    cells.append(md_cell(
        "Parallel multi-threaded downloader — reuse for datasets, weights, or any large files."
    ))
    dl_code = PARALLEL_DOWNLOAD_CODE
    if hf_repo:
        dl_code += "\n" + HF_DOWNLOAD_CODE.format(hf_repo=hf_repo)
    cells.append(code_cell(dl_code))

    # ── 4. Dataset download ────────────────────────────────────────────────
    cells.append(section_header("4. Dataset Download"))
    if dataset_files:
        file_list_repr = "[\n" + "".join(
            f'    ("{f["url"]}", "{f["dest"]}"),\n'
            for f in dataset_files
        ) + "]"
        cells.append(code_cell(
            f"DATASET_FILES = {file_list_repr}\n"
            f"parallel_download(DATASET_FILES, max_workers=8)"
        ))
    else:
        cells.append(code_cell(
            "# Specify dataset files:\n"
            "# DATASET_FILES = [\n"
            "#     (\"https://...\", \"data/train.zip\"),\n"
            "#     (\"https://...\", \"data/val.zip\"),\n"
            "# ]\n"
            "# parallel_download(DATASET_FILES, max_workers=8)"
        ))

    # ── 5. Weights download (run-results mode) ─────────────────────────────
    if mode == "run-results":
        cells.append(section_header("5. Download Pretrained Weights"))
        if weight_files:
            wf_repr = "[\n" + "".join(
                f'    ("{f["url"]}", "{f["dest"]}"),\n'
                for f in weight_files
            ) + "]"
            cells.append(code_cell(
                f"WEIGHT_FILES = {wf_repr}\n"
                f"parallel_download(WEIGHT_FILES, max_workers=4)"
            ))
        elif hf_repo:
            cells.append(code_cell(
                f"from huggingface_hub import snapshot_download\n"
                f"snapshot_download(repo_id='{hf_repo}', local_dir='weights/')\n"
                f"print('Weights ready.')"
            ))
        else:
            cells.append(code_cell(
                "# Add weight download here:\n"
                "# WEIGHT_FILES = [(url, dest), ...]\n"
                "# parallel_download(WEIGHT_FILES)"
            ))

    # ── Paper-specific sections ────────────────────────────────────────────
    section_num = 6 if mode == "run-results" else 5
    for sec in sections:
        sec_title = sec.get("title", "Section")
        cells.append(section_header(f"{section_num}. {sec_title}"))
        section_num += 1
        if sec.get("markdown"):
            cells.append(md_cell(sec["markdown"]))
        if sec.get("code"):
            cells.append(code_cell(sec["code"]))

    # ── Manual steps note ─────────────────────────────────────────────────
    if manual_steps:
        steps_md = "## ⚠️ Manual Steps Required\n\n" + "\n".join(
            f"{i+1}. {s}" for i, s in enumerate(manual_steps)
        )
        cells.append(md_cell(steps_md))

    # ── Notebook JSON ──────────────────────────────────────────────────────
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0",
            },
        },
        "cells": cells,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    # Read spec from file arg or stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            spec = json.load(f)
    else:
        spec = json.load(sys.stdin)

    notebook = build_notebook(spec)

    output_path = Path(spec.get("output", f"notebooks/{spec.get('paper_id', 'paper')}-{spec.get('mode', 'notebook')}.ipynb"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f"✓ Notebook written: {output_path}")
    print(f"  Cells: {len(notebook['cells'])}")
    print(f"  Mode:  {spec.get('mode', '?')}")


if __name__ == "__main__":
    main()
