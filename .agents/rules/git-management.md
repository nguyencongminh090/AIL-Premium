---
trigger: always_on
glob: 
description: "Binding rules for all Git operations — branching strategy, Conventional Commits format, safety guards against force-push and secret leaks, merge/rebase policy, and semantic versioning for releases."
---

# Git Management Rules

Binding rules for all Git operations in this workspace. These apply to every
commit, branch, push, merge, or deploy action unless a skill explicitly
overrides a specific clause.

---

## 1. Branch Strategy

- `main` (or `master`) is **protected** — never push directly to it.
- Work always happens on a **feature branch**:
  - Format: `<type>/<short-slug>` — e.g., `feat/add-ppc-pipeline`, `fix/qa-route-null`, `docs/update-readme`
  - Valid types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `hotfix`
- Branches must be branched off the latest `main`. Always `git pull origin main` before creating a new branch.
- Delete merged branches after the PR/MR is closed.

---

## 2. Commit Message Standard (Conventional Commits)

All commit messages must follow the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short summary in imperative mood>

[optional body — explain WHY, not WHAT]

[optional footer — BREAKING CHANGE, closes #issue]
```

**Rules:**
- Summary line ≤ 72 characters, lowercase after the colon.
- Use imperative mood: "add feature" not "added feature".
- Never use vague messages: `fix`, `update`, `misc`, `wip`, `temp` alone are forbidden.
- One logical change per commit — do not bundle unrelated changes.

**Examples:**
```
feat(notes): add paper-overview output for paper 001
fix(qa-route): handle null user_id in get_history
docs(rules): add git management rules
chore(deps): bump fastapi to 0.115.0
```

---

## 3. Safety — Never Break, Never Lose

- **Never force-push** (`git push --force`) to shared branches (`main`, `develop`, `staging`).
  - Force-push is only allowed on your own feature branch before a PR is opened, with explicit intent.
- **Never `git reset --hard`** on shared branches.
- **Never delete remote branches** that others may be working on without team confirmation.
- **Never commit secrets**: API keys, `.env` files, private credentials, or tokens must never appear in commits.
  - Add `.env`, `*.local`, `secrets/` to `.gitignore` before first commit.
- Before any destructive operation (rebase, reset, amend), create a backup tag:
  ```bash
  git tag backup/<branch>-<YYYYMMDD-HHMM>
  ```

---

## 4. Staging & Review Before Commit

- Always run `git diff --staged` to review exactly what is being committed.
- Always run `git status` before committing to confirm no unintended files are staged.
- Never use `git add .` blindly — prefer `git add <specific-file>` or `git add -p` for interactive staging.
- If tests exist, all tests must pass before committing to `main` or `develop`.

---

## 5. `.gitignore` Requirements

The following must always be ignored:

```
# Environment & secrets
.env
.env.*
*.local
secrets/

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
*.egg-info/

# IDE & OS
.DS_Store
.vscode/settings.json
*.swp

# Build artifacts
dist/
build/
*.log
```

---

## 6. Merge & Rebase Policy

- Prefer **squash-and-merge** for feature branches into `main` to keep history clean.
- Use **rebase** (not merge) when syncing a feature branch with `main`:
  ```bash
  git fetch origin
  git rebase origin/main
  ```
- Resolve all merge conflicts locally — never commit unresolved conflict markers (`<<<<<<`, `======`, `>>>>>>`).

---

## 7. Tagging & Releases

- Use **semantic versioning** for tags: `vMAJOR.MINOR.PATCH` (e.g., `v1.2.0`).
- Tags are only created on `main` after a successful merge.
- Annotated tags are preferred over lightweight tags:
  ```bash
  git tag -a v1.2.0 -m "Release v1.2.0: add PPC pipeline skill"
  git push origin v1.2.0
  ```

---

## 8. Deploy Safety

- Deploy only from tagged commits on `main`.
- Always verify the deployed commit hash matches the intended tag.
- Keep a `CHANGELOG.md` updated with every release — entries grouped by `feat`, `fix`, `breaking`.
