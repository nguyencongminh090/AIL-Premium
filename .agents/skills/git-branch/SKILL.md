---
name: git-branch
description: This skill is used to create, switch, or manage Git branches following the project's branching strategy. Activate when the user wants to start a new feature, fix, or task on a fresh branch, or when switching between branches.
argument-hint: <type/branch-slug> e.g. feat/add-pipeline
---

# Git Branch Worker

This skill manages branch creation and switching following the project's `<type>/<short-slug>` naming convention. It always syncs from `main` before creating a new branch.

## Conventions
This skill treats `.agents/rules/git-management.md` as binding for branch naming, base-sync requirements, and safety rules.

## Procedure

1. **Sync with remote.** Run `git fetch origin && git checkout main && git pull origin main` to ensure the base is up to date.

2. **Resolve branch name from `$ARGUMENTS`.**
   - If `$ARGUMENTS` is provided, validate it matches `<type>/<short-slug>` format (lowercase, hyphens only).
   - If `$ARGUMENTS` is empty, ask the user: what type (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `hotfix`) and a short 2–4 word slug.

3. **Create and switch.**
   ```bash
   git checkout -b <branch-name>
   ```
   Confirm with `git branch --show-current`.

4. **Report.** Print the new branch name, the base branch (`main`), and suggest the next step: make changes, then run `/git-commit`.
