# README_VERSIONNING — E1 v1 (SQLite)

Ce document trace les évolutions applicables à la ligne de notebooks `datasens_E1_v1/*`.
Il complète le `CHANGELOG.md` global et renvoie aux tags Git SemVer.

## Stratégie
- Versionnage: SemVer (`vX.Y.Z`).
- Traçabilité: commits conventionnels + tags Git + images GHCR (`ghcr.io/<org>/datasens:vX.Y.Z`).
- Périmètre: notebooks `02_schema_create.ipynb`, `03_ingest_sources.ipynb`, `05_snapshot_and_readme.ipynb` (et associés v1).

## Versions

### v3.0.0 — 2025-11-03
- Sécurité
  - Ajout de `assert_valid_identifier()` et validation des identifiants dans `02_schema_create.ipynb` et `03_ingest_sources.ipynb`.
  - Requêtes SQL adaptées SQLite et contrôles sur les noms de tables.
- Visualisations / Storytelling
  - Tableau de bord narratif de démarrage, timeline, sections avant/après collecte (Kaggle CSV).
- Export
  - Export datasets Parquet/CSV finalisé dans `05_snapshot_and_readme.ipynb`.
- Documentation
  - Alignement avec `SECURITY.md`, `CONTRIBUTING.md`, `docs/GUIDE_TECHNIQUE_E1.md` (détail des visualisations).

Références:
- Tag Git: `v3.0.0` (mettre le lien vers la release lorsque disponible).
- Historique global: voir `CHANGELOG.md` à la racine du dépôt.

### v3.1.0 — 2025-11-10 (préparation)
- Sécurité: (exemple) contrôle renforcé sur les identifiants de colonnes.
- Storytelling: (exemple) ajout d’une mini-viz X dans 03_ingest_sources.ipynb.
- Export: (exemple) export CSV filtré supplémentaire.
Référence: tag `v3.1.0` (lors de la release), détails dans `CHANGELOG.md`.

## Comment mettre à jour ce fichier
1. Lorsqu’un changement impacte v1 (sécurité, logique, storytelling, export), ajoutez une entrée sous la nouvelle version.
2. Synchronisez la date et le tag (`git tag vX.Y.Z && git push --tags`).
3. Vérifiez que `CHANGELOG.md` contient la même version (global) et des sections cohérentes.

DataSens E1_v1 — Versionning exécution (journal)
=================================================

Objectif: journal simple et pédagogique des étapes exécutées (date/heure, action, détail) pour tracer l'avancement.

Format: une ligne par action, au format Markdown.

Exemples:
- **2025-10-30 10:15:04** | `INIT` | Création arborescence `data/raw|silver|gold`, `logs`, `docs`
- **2025-10-30 10:21:36** | `SCHEMA` | Création tables v1 (10 tables SQLite) + index
- **2025-10-30 10:29:12** | `INGEST` | Ingestion données simulées (Faker) → 100 docs
- **2025-10-30 10:32:58** | `QA` | Normalisation + SHA256 + dédup (−5%)
- **2025-10-30 10:35:40** | `CRUD` | Insert/Select/Update/Delete OK
- **2025-10-30 10:38:05** | `EXPORT` | Export SQLite: `data/gold/datasens_v1.db`

---

Ajoutez vos entrées ci-dessous au fur et à mesure:
- **2025-11-03 14:35:40** | `INIT` | Création de la structure projet et versionning
- **2025-11-03 14:36:27** | `DB_SCHEMA` | Création des 18 tables principales
- **2025-11-03 14:38:06** | `DB_SEED` | Insertion du jeu de données minimal
- **2025-11-03 14:50:34** | `INIT` | Création de la structure projet et versionning
- **2025-11-03 14:50:58** | `DB_SCHEMA` | Création des 18 tables principales
- **2025-11-03 14:52:05** | `DB_SEED` | Insertion du jeu de données minimal
