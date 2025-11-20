# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning (SemVer).

## [Unreleased]
### Added
- Inventaire consolidé des sources dans `05_snapshot_and_readme.ipynb` (scan DataLake + tables PostgreSQL par source).
- Nouvelle cellule d'export automatisé (Parquet/CSV) avec journalisation `LAST_EXPORT_FILES`.
- Pipeline d'upload des exports vers MinIO, AWS S3 et artefacts locaux (manifest JSON).
- Script `scripts/apply_annotation_pipeline.py` (annotation spaCy+YAKE + export annoté + insertion optionnelle t05).
- Dépendance `boto3` pour activer l'upload S3.

### Changed
- `05_snapshot_and_readme.ipynb` détecte désormais la racine projet via `detect_project_root()` comme les autres notebooks.
- Inventaire des fichiers bruts étendu (`baro_*`, `source_*`) et requêtes DB forcées sur `datasens` via `SET search_path`.
- Section export IA restructure la logique (timestamp, stats, exposé clair des chemins).

### Fixed
- Comptes inventaire qui restaient à `N/A` à cause du `search_path` sur `public`.
- TypeError lors de l'aperçu CRUD delete (`pd.read_sql_query` remplacé par `conn.execute` + DataFrame).
- Export Parquet qui n'affichait pas correctement les warnings `datetime.utcnow()` (passage à `datetime.now(UTC)`).

### Security
- Rappel explicite des variables `.env` manquantes lors du chargement dans `05_snapshot_and_readme.ipynb`.

## [3.1.0] - 2025-11-10
### Added
- (exemple) Nouvelle visualisation X dans `03_ingest_sources.ipynb` (v1/v2/v3).

### Changed
- (exemple) Ajustement des performances chargement CSV.

### Fixed
- (exemple) Correction d'un chemin relatif d'export.

### Security
- (exemple) Durcissement validation des identifiants colonnes.

## [3.0.0] - 2025-11-03
### Added
- Visual storytelling complet (v1/v2/v3): dashboard narratif, timeline, sections avant/après collecte.
- Script de vérification robuste `scripts/verify_project_complete.py` (rapport possible dans `reports/`).
- Export datasets Parquet/CSV final dans les notebooks `05_snapshot_and_readme.ipynb` (v1/v2/v3).

### Changed
- Sécurité consolidée (v2/v3): `assert_valid_identifier()`, `load_whitelist_tables()`, requêtes SQL paramétrées.
- Documentation mise à jour: `SECURITY.md`, `CONTRIBUTING.md`, `README.md`, `docs/GUIDE_TECHNIQUE_E1.md` (détail des visualisations).
- Arborescences v1/v2/v3 alignées et nettoyées.

### Fixed
- Suppression des cellules storytelling dupliquées dans `notebooks/datasens_E1_v3/03_ingest_sources.ipynb`.
- Corrections d'encodage dans les scripts (Windows `cp1252` → UTF-8, suppression d’emojis dans la console).

### Security
- Gestion des secrets via `.env` + `os.getenv()` et `.gitignore`.
- Renforcement CI/CD Docker GHCR (authentification et taggage versionné).

[Unreleased]: https://github.com/<owner>/<repo>/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/<owner>/<repo>/releases/tag/v3.0.0

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


