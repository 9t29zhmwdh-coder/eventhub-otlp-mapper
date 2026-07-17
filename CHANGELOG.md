# Changelog

All notable changes to eventhub-otlp-mapper will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
