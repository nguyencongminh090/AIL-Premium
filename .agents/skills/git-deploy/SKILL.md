---
name: git-deploy
description: This skill is used when the user wants to tag a release and deploy from the main branch. It should be invoked when a feature set is complete and merged to main, and the user wants to create a versioned release. It enforces deploy-only-from-main and semantic versioning rules.
argument-hint: <version> e.g. v1.2.0
---

# Git Deploy Worker

This skill orchestrates a safe release tagging and deployment process, enforcing deploy-only-from-`main` and semantic versioning (`vMAJOR.MINOR.PATCH`).

## Conventions
This skill treats `.agents/rules/git-management.md` as binding for tagging format, deploy safety, and CHANGELOG requirements.

## Procedure

1. **Verify branch.** Run `git branch --show-current`.
   If not on `main`, stop immediately and warn:
   > "Deploys must only happen from `main`. Please merge your changes via PR first."

2. **Sync remote.**
   ```bash
   git fetch origin
   git pull origin main
   ```
   Confirm local `main` is up-to-date with remote.

3. **Resolve version tag from `$ARGUMENTS`.**
   - If `$ARGUMENTS` is provided, validate it matches `vMAJOR.MINOR.PATCH`.
   - If `$ARGUMENTS` is empty, list the last 5 tags (`git tag --sort=-version:refname | head -5`) and ask the user for the new version.
   - Reject any non-conforming tag (no `v` prefix, non-numeric, etc.).

4. **Create safety backup.**
   ```bash
   git tag backup/pre-deploy-<YYYYMMDD-HHMM>
   ```

5. **Create annotated tag.** Ask for a one-line release summary if not provided.
   ```bash
   git tag -a <version> -m "Release <version>: <summary>"
   git push origin <version>
   ```

6. **Update CHANGELOG.md.** Check if `CHANGELOG.md` exists at the project root.
   - If it exists, prepend a new `## [<version>] - <YYYY-MM-DD>` section with `### Features` and `### Fixes` subsections.
   - If it doesn't exist, create it with this release as the first entry.

7. **Report.** Print:
   - Tag created and commit hash tagged
   - CHANGELOG updated: Yes / No
   - Remote push: success / failure
