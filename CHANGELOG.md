# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]
### Added
- **E1_v3 Pipeline Complet** : Architecture 36/37 tables avec toutes les sources réelles (Kaggle, OpenWeatherMap, RSS, NewsAPI, Web Scraping, GDELT)
- **Classification professionnelle types de données** : Standards Médiamétrie (Nomenclature, Données Maîtres, Opérationnelles, Décisionnelles, Métadonnées)
- **Configuration flexible des sources** : `config/sources_config.json` pour gérer toutes les sources sans modifier le code
- **Export Dataset IA** : Export Parquet/CSV structuré dans `data/gold/dataset_ia/` prêt pour enrichissement E2
- **Visualisations complètes** : Pandas DataFrames + Matplotlib à chaque étape (MinIO, PostgreSQL, CRUD, QA)
- **Dockerfile and docker-compose** : Stack complet Jupyter + PostgreSQL + MinIO
- **LICENSE** : MIT License ajoutée
- **.env.example** : Template complet avec toutes les variables d'environnement
- **Extended technical guide** : Guide technique complet avec glossaire, KPIs, troubleshooting, roadmap

### Changed
- **requirements.txt** : Complété avec toutes les dépendances (feedparser, beautifulsoup4, praw, google-api-python-client, tenacity, tqdm, pyarrow, matplotlib)
- **README** : Vision complète du projet (bouffeur de données + classifieur professionnel), référence corrigée
- **.gitignore** : Amélioré (datasens.db, *.db, versions/), .env.example n'est plus ignoré
- **CI/CD** : Workflow corrigé (référence datasens_audit.py supprimée)
- **README and guide clarified** : E1_v3 = annotation simple (préparation dataset), E2 = annotation IA avancée (CamemBERT, FlauBERT)

### Fixed
- Notebook sanitization for invalid surrogate characters
- Référence obsolète dans README (GUIDE_TECHNIQUE_JURY.md → GUIDE_TECHNIQUE_E1.md)

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


