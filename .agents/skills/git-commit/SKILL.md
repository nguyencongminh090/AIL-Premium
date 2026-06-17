---
name: git-commit
description: "This skill is used when the user wants to stage, review, and commit changes with a properly formatted Conventional Commits message. It should be invoked when the user says commit, save changes to git, or when a feature/fix is complete and ready to be recorded."
argument-hint: "<optional: commit message hint or scope>"
---

# Git Commit Worker

This skill guides a safe, standards-compliant Git commit workflow — deliberate staging, safety checks, and a Conventional Commits message.

## Conventions
This skill treats `.agents/rules/git-management.md` as binding for commit message format, staging safety, and secret-leak prevention.

## Procedure

1. **Inspect current state.**
   ```bash
   git status
   git diff --staged
   ```
   If nothing is staged, run `git diff` and ask the user which files to include.

2. **Stage files deliberately.** Never use `git add .` blindly. Prefer:
   ```bash
   git add <specific-file>
   # or interactive:
   git add -p
   ```
   Confirm staging with `git diff --staged` before continuing.

3. **Validate safety checks.**
   - No `.env` or secret files are staged.
   - No unresolved conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
   - No unintended binary or large files are staged.
   If any check fails, unstage the problematic file and warn the user.

4. **Construct commit message** using Conventional Commits format:
   ```
   <type>(<scope>): <short imperative summary ≤ 72 chars>

   [optional body — explain WHY]

   [optional footer — Closes #42, BREAKING CHANGE: ...]
   ```
   If `$ARGUMENTS` is provided, use it as the scope or summary hint.
   If `$ARGUMENTS` is empty, infer type and scope from staged file paths.

5. **Commit.**
   ```bash
   git commit -m "<message>"
   ```
   Print the commit hash and summary after success.

6. **Offer to push.** Ask: "Do you want to push this commit to remote?"
   If yes, run `git push origin <current-branch>`.
   If on `main` or `master`, warn and abort the push.
