# Changelog

All notable changes to eventhub-otlp-mapper will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.3] - 2026-07-29

### Changed

Dependency and workflow updates merged since 1.1.2:

- chore(ci): bump the actions group across 1 directory with 4 updates

---

## [1.1.2] - 2026-07-28

### Changed

- CodeQL moved from GitHub's default setup to an advanced setup with a committed `.github/workflows/codeql.yml`. The default setup skips pull requests that touch no code of a given language, so a dependency pull request changing only a lock file reported `skipping` on the required `Analyze (...)` checks forever and could never be merged. The workflow runs on every pull request regardless of what changed and uses the `security-extended` query suite, which the default setup does not allow choosing. Required checks are unchanged.
- The CodeQL job requests only `security-events: write` beyond the workflow-level `contents: read`. Repeating read grants at job level is what OpenSSF Scorecard counts as excessive token permissions, and it costs the full `Token-Permissions` score.
- Dependabot now groups only minor and patch updates per ecosystem; majors arrive as individual pull requests. The previous grouping bundled breaking changes with urgently needed security patches into one unreviewable diff. Actions stay grouped wholesale. Follows `engineering-standards` v0.11.0.

## [1.1.1] - 2026-07-28

### Added

- `.github/dependabot.yml`, with grouped weekly updates. The file was missing, and without it there are no version updates at all: repository security alerts only fire for disclosed vulnerabilities, which is how action pins across this portfolio quietly went stale. Follows `engineering-standards` v0.10.0.

### Fixed

- 4 action references used a mutable version tag rather than a commit SHA. A tag can be moved to point at different code after the fact without the workflow file changing; a SHA cannot. All are now pinned, with the version in the comment, per `standards/ci-cd.md` section 2. Pinned at the version that was actually running rather than upgraded, so any major bump arrives as its own reviewable Dependabot PR.
- `actions/checkout` pins now carry the full version in the comment instead of a bare major, and all workflows use the same SHA.

## [1.1.0] - 2026-07-28

### Added

- `ruff format --check` in CI, which did not exist. Formatting was therefore never enforced. Enabling it reformatted 4 files, all cosmetic; 20 tests pass unchanged.

### Changed

- `ruff` is pinned to 0.16.0 instead of `>=0.4`. The format check just added would otherwise be able to turn red on unchanged source whenever a new ruff changes what it considers formatted, per `engineering-standards` v0.7.0.

Note on the lint scope: CI runs `--select E9,F821,F822,F823` and `pyproject.toml` configures exactly the same set, so unlike some sibling repositories the configuration here describes what actually runs. The narrow set is a deliberate choice, not an oversight, and is left as is.

## [1.0.1] - 2026-07-20

### Changed

- OpenSSF Scorecard workflow and badge.
- `copilot-instructions.md` for consistent AI-assisted contributions.
- Unified the EN/DE language-switch link format.
- Coverage reporting in CI (pytest-cov).
- Split the README's security/CI badges onto their own line, separate from the platform/tech/AI badges (they were rendering as a single merged line).

## [1.0.0] - 2026-07-17

First stable release: a real release pipeline now builds a real wheel/sdist
and attaches it to every GitHub Release, the prerequisite for a 1.0 release
per this portfolio's own SemVer discipline.

### Added
- Release workflow (`release.yml`) that builds a wheel and sdist on every `v*` tag push and attaches them to a GitHub Release. Previously there was no packaged distribution; users had to install from source.

## [0.1.6] - 2026-07-17

### Changed
- CI: added an explicit `permissions: contents: read` block to the workflow(s) that were missing one (CodeQL `actions/missing-workflow-permissions`), narrowing the default GITHUB_TOKEN scope.

## [0.1.5] - 2026-07-12

### Added

- README/README.de.md: "How it runs" callout, "In practice" paragraph, and "Uninstall/Cleanup" section, which this repo was missing entirely in both languages. Added a "Roadmap" section to README.de.md to match README.md.

### Fixed

- Removed em-dashes/en-dashes from LICENSE and GETTING_STARTED.md (Swiss German orthography rule).
- Removed ASCII-substituted umlauts from README.de.md ("Unterstuetzt"/"Unterstuetzung" to "Unterstützt"/"Unterstützung", "faehige" to "fähige", "fuer" to "für").

## [0.1.4] - 2026-07-11

### Added

- Documented Dual-Licensing assessment (Community-only) in ROADMAP.md.

## [0.1.3] - 2026-07-11

### Fixed

- Updated actions/checkout and actions/setup-python to their latest major versions in CI, since GitHub is deprecating the Node.js 20 runtime and older action versions were being forced onto Node 24 and crashing during post-run cleanup.

## [0.1.2] - 2026-07-10

### Fixed

- Changed the language-switch link from a blockquote to plain text
