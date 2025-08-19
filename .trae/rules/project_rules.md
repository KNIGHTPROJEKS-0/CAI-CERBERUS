# Project Rules for TRAE (CAI-CERBERUS)

Audience: TRAE (and any agents, bots, or contributors acting on behalf of this project)

Status: Authoritative. If anything here conflicts with the repository’s README.md, follow README.md as the source of truth and open an issue/PR to reconcile this document.

---

## 1) Purpose

These rules ensure TRAE operates consistently with this repository’s standards, follows the README.md guidelines, and respects the project’s heritage and licensing while CAI-CERBERUS evolves as a standalone project.

- You must comply with all policies, workflows, and instructions in:
  - README: ./README.md (source of truth)
  - LICENSE: ./LICENSE (license terms and attribution must be preserved)
  - CONTRIBUTING: ./CONTRIBUTING.md (if present)
  - CODE_OF_CONDUCT: ./CODE_OF_CONDUCT.md (if present)
  - Any SECURITY, GOVERNANCE, or policy docs (if present)

If a document is referenced but not present, do not assume—open an issue to clarify.

---

## 2) Heritage and Attribution

- Origin: This project was originally forked from https://github.com/aliasrobotics/cai.git.
- Status: The fork was detached to become a standalone project. It has been rebuilt, restructured, and upgraded as CAI-CERBERUS.
- Requirements:
  - Preserve and respect original licensing and attribution as required by LICENSE and any upstream NOTICE files.
  - Avoid introducing or restoring dependencies on the original repository unless explicitly approved.
  - When porting or reusing code/commentary from upstream, include clear attributions in commit messages and file headers where required by license.

---

## 3) Follow the README (Source of Truth)

- Before starting any task, read and follow ./README.md completely.
- If README instructions differ from legacy practices (from the original cai repo), follow CAI-CERBERUS README.
- If you detect inconsistencies or missing guidance in README:
  - Pause the change.
  - Open an issue proposing updates to README.
  - Optionally submit a PR that first updates README, then implements the change.

---

## 4) Branching, Commits, and PRs

- Branches:
  - Use short, descriptive names: feature/<scope>, fix/<scope>, chore/<scope>, docs/<scope>, refactor/<scope>.
- Commits:
  - Use Conventional Commits where possible: feat:, fix:, docs:, style:, refactor:, perf:, test:, chore:, build:, ci:, revert:
  - Keep commits atomic, with clear rationale and scope.
- Pull Requests (PRs):
  - Ensure the PR description summarizes the “what” and “why,” links related issues, and lists breaking changes if any.
  - Include test coverage and documentation updates as part of the same PR whenever feasible.
  - Pass all CI checks before requesting review.
  - Reference README sections you followed (e.g., “Implements per README: Build > Steps 1–3”).

---

## 5) Coding, Architecture, and Style

- Conform to language/stack standards documented in README or CONTRIBUTING.
- Follow project directory structure and module boundaries defined by CAI-CERBERUS (not upstream), unless a migration plan says otherwise.
- Prefer incremental, backwards-compatible changes unless a known breaking change has been approved and documented.

If style or linting rules exist (e.g., configs in the repo), they are mandatory.

---

## 6) Testing and Quality

- Minimum expectations:
  - Unit tests for new logic.
  - Integration tests when touching system/IO boundaries.
  - No failing or flaky tests—quarantine and fix.
- Coverage targets:
  - Follow README/CONTRIBUTING targets. If none are specified, aim for meaningful coverage and justify any gaps in the PR.
- CI:
  - All CI checks must pass before merging.
  - Add or update CI workflows if new components require them.

---

## 7) Security and Secrets

- Never commit secrets, tokens, or credentials. Use environment variables, GitHub Secrets, or approved secret managers.
- Follow SECURITY.md if present; otherwise:
  - Report vulnerabilities privately as per standard responsible disclosure practices.
  - Apply dependency updates for critical/high vulnerabilities promptly.

---

## 8) Dependencies and Upgrades

- When upgrading or restructuring:
  - Prefer minimal, well-justified changes with a clear migration note.
  - Document version bumps, motivations, and potential impacts in the PR.
  - Remove unused dependencies and update lockfiles deterministically.
- If replacing upstream components, document parity gaps and new behavior clearly.

---

## 9) Documentation

- Update README and in-repo docs with:
  - New commands, config flags, environment variables, and endpoints.
  - Any breaking changes or notable behavior changes.
- Include examples and quickstart snippets when adding new capabilities.
- Keep CHANGELOG.md (if present) current; if not present, summarize changes in PRs.

---

## 10) Compatibility and Migration

- For breaking changes:
  - Provide migration steps in PR description and, if needed, in README.
  - Consider deprecation periods or feature flags when feasible.
- For restructuring:
  - Maintain clear mapping from old paths/names to new ones (e.g., in docs or a MIGRATION.md).
  - Update all internal references and links.

---

## 11) Provenance and Linking

- Replace upstream links with CAI-CERBERUS equivalents unless attributing or citing the origin.
- Ensure internal links in docs are relative and valid.
- Do not rely on upstream CI, badges, or vendor configs; migrate to local equivalents.

---

## 12) Issue Management

- Open issues for:
  - Missing or unclear instructions in README or this file.
  - Security concerns.
  - Significant design or architectural changes prior to implementation.
- Use labels and milestones consistently per repository conventions (see README/CONTRIBUTING if defined).

---

## 13) Operating as an Agent (TRAE-specific)

When acting autonomously or semi-autonomously:

- Respect task scope. If a task’s scope is ambiguous, pause and request clarification via an issue or PR comment.
- Never bypass required reviews or CI.
- Prefer smallest viable PRs that are independently reviewable.
- Provide a checklist in each PR (see §14) indicating README compliance and tests.
- Leave clear breadcrumbs:
  - Why was the change needed?
  - What alternatives were considered?
  - How can it be reverted safely?

---

## 14) PR Checklist (copy into each PR description)

- [ ] I have followed all relevant instructions in ./README.md.
- [ ] I have preserved licensing and attribution as required by ./LICENSE and upstream references.
- [ ] This change aligns with CAI-CERBERUS structure and not the original cai layout.
- [ ] Tests added/updated and all CI checks pass.
- [ ] Documentation (README and/or other docs) updated for new/changed behavior.
- [ ] No secrets or sensitive data introduced.
- [ ] Links and badges point to CAI-CERBERUS (not upstream), except where attribution is required.
- [ ] If this is a breaking change, migration steps are documented.

---

## 15) Acknowledgements

CAI-CERBERUS originated from https://github.com/aliasrobotics/cai.git and has since been detached, rebuilt, restructured, and upgraded as a standalone project. We acknowledge and respect the contributions of the original authors and maintainers. All licensing and attribution obligations are preserved.

---

## 16) Questions or Conflicts

- If any rule conflicts with README or LICENSE, follow README and LICENSE, then open an issue to correct this file.
- When unsure, stop, document your assumptions, and seek confirmation via issue or PR discussion.

End of rules.