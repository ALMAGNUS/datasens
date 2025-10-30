# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]
### Added
- Dockerfile and docker-compose with Postgres and MinIO.
- One-file notebook auditor/fixer `datasens_audit.py` (+ viz, annotation, Parquet export).
- Extended technical guide with glossary, KPIs, troubleshooting, roadmap.
- Demo runbook and enriched README (quick links, release workflow, security notes).

### Changed
- README aligned with technical reference; added ML-ready export section.

### Fixed
- Notebook sanitization for invalid surrogate characters.

## [0.1.0] - 2025-10-30
### Added
- Initial public structure with notebooks, docs, and scripts scaffolding.

## [0.2.0] - 2025-10-30
### Added
- MLD (`docs/datasens_MLD.md`) and MPD SQL (`docs/datasens_MPD.sql`).
- Dictionaries: tables (`docs/datasens_tables_dictionary.md`), relations (`docs/datasens_relations_dictionary.md`), sources (`docs/datasens_sources_dictionary.md`), naming/arbo (`docs/datasens_naming_dictionary.md`).
- Barometric themes reference (`docs/datasens_barometer_themes.md`).
- CI: GitHub Actions for lint and Docker build; release workflow scaffold.
- Ruff config (`pyproject.toml`) and exclusions for notebooks/data/logs.
- `.env.example` at project root.

### Changed
- README professionalized (badges, quick links, security/CI notes) and aligned with guide.
- Notebooks standardized to root paths for `data/`, `docs/`, and `logs/`.

### Removed
- External Python auditor file from demo scope; focus on self-contained notebooks.


