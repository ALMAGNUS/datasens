DataSens — Projet
=================

Voir le guide technique: docs/GUIDE_TECHNIQUE_E1.md
Voir la référence technique étendue: docs/GUIDE_TECHNIQUE_JURY.md

![GitHub Release](https://img.shields.io/github/v/release/ALMAGNUS/datasens?include_prereleases)
![GitHub Stars](https://img.shields.io/github/stars/ALMAGNUS/datasens?style=social)
![GitHub Issues](https://img.shields.io/github/issues/ALMAGNUS/datasens)
![Code Size](https://img.shields.io/github/languages/code-size/ALMAGNUS/datasens)
![License](https://img.shields.io/github/license/ALMAGNUS/datasens)
![Last Commit](https://img.shields.io/github/last-commit/ALMAGNUS/datasens)

Liens rapides
-------------

- Dépôt: https://github.com/ALMAGNUS/datasens
- Sujets (issues): https://github.com/ALMAGNUS/datasens/issues
- Releases: https://github.com/ALMAGNUS/datasens/releases
- Discussions: https://github.com/ALMAGNUS/datasens/discussions
- Pull Requests: https://github.com/ALMAGNUS/datasens/pulls

Description
-----------

Structure académique DataSens. Pilotage par notebooks Jupyter, versionné sur GitHub.

Arborescence du dépôt
---------------------

- `data/`
  - `raw/` Zone Bronze (sources brutes)
  - `silver/` Jeux de données nettoyés
  - `gold/` Jeux finaux enrichis
  - `tmp/` Zone tampon
- `notebooks/` Notebooks d’exécution par blocs/versions
- `docs/` Modèles de données, dictionnaires, READMEs
- `logs/` Manifests et journaux d’exécution
- `scripts/` Scripts (ingestion, contrôles, CRUD, pipeline)

Versionnage
-----------

Utiliser des tags pour les jalons:

- `E1_v1`: Schéma prototype (10 tables) données simulées
- `E1_v2`: Ingestion réelle (18 tables, 5 sources)
- `E1_v3`: Pipeline complet (36 tables, Prefect + MinIO + PostgreSQL)

Démarrage rapide (Docker - recommandé)
---------------------------------------

**Pour le jury / démonstration (2 minutes):**

```bash
# 1. Cloner le dépôt
git clone https://github.com/ALMAGNUS/datasens.git
cd datasens

# 2. Lancer le stack complet (Jupyter + Postgres + MinIO)
docker compose up -d --build

# 3. Accéder à Jupyter Lab
# Ouvrir: http://localhost:8888
# Token affiché dans les logs: docker compose logs app | grep token
```

**Stack Docker:**
- Jupyter Lab: http://localhost:8888
- PostgreSQL: localhost:5433 (user: `postgres`, pwd: `postgres`, db: `postgres`)
- MinIO Console: http://localhost:9003 (user: `minioadmin`, pwd: `minioadmin`)
- MinIO API: http://localhost:9002

**Arrêter le stack:**
```bash
docker compose down
```

Démarrage local (sans Docker)
-----------------------------

1. Créer un environnement Python 3.10+
2. Installer les dépendances: `pip install -r requirements.txt`
3. Démarrer PostgreSQL et MinIO localement (ou utiliser les services Docker)
4. Ouvrir les notebooks sous `notebooks/datasens_E1_v3/`

Mode Démo (10–15 min)
---------------------

Objectif: exécuter un notebook unique (sans `.py` externe) montrant ingestion multi-sources → normalisation → QA → stockage → CRUD → visualisations.

- Notebook conseillé: `notebooks/datasens_E1_v3/03_ingest_sources.ipynb` (ou la dernière version E1 disponible)

Étapes:
1. Ouvrir le notebook et exécuter toutes les cellules.
2. Suivre le logging inline (console) et vérifier les fichiers `logs/` (`collecte_*.log`, `errors_*.log`).
3. Vérifier le schéma normalisé: `titre, texte, source_site, url, date_publication, langue` + `hash_fingerprint` (SHA256) et dédoublonnage.
4. Vérifier l’insertion PostgreSQL et un CRUD minimal (SELECT/UPDATE/DELETE).
5. Afficher 1–2 graphiques (documents par source/date/langue).

Variables d’environnement
-------------------------

- `DATASENS_PG_DSN` (défaut: `postgresql+psycopg2://postgres:postgres@localhost:5432/postgres`)
- `NEWSAPI_KEY`, `OPENWEATHER_API_KEY`, etc. (facultatives)
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET` (facultatif; fallback local dans `data/raw/`)

Annotation FR (CamemBERT / FlauBERT)
------------------------------------

- Modèles par défaut (priorité FR): CamemBERT puis FlauBERT
- Nettoyage + détection de langue (priorité FR)
- Sentiment/polarité: modèles FR en priorité (CamemBERT, FlauBERT). Si indisponible, heuristique simple.
- NER: spaCy modèle FR (fallback neutre si absent)
- Mots-clés: YAKE FR (fallback TF-IDF simple)
- Dédoublonnage SHA256 et QA de base

Export prêt-IA
--------------

- Parquet partitionné (date/langue/source), ex:
  - `data/gold/annotated/date=YYYY-MM-DD/langue=fr/source=reddit/part.parquet`

Tolérance aux manques (démo)
----------------------------

- Clés API absentes: la source est sautée (log) et l’exécution continue.
- MinIO absent: écriture locale sous `data/raw/`.
- PostgreSQL absent: définir `DATASENS_PG_DSN` ou démarrer une DB locale (erreurs explicites sinon).

Sécurité & Secrets
------------------

- Ne jamais committer de secrets: `.env` est ignoré.
- SQL paramétré (`text("... :param")` + dict). Éviter concaténations/f-strings pour les valeurs/identifiants.
- Si noms de tables dynamiques, valider via liste blanche.

Publication & Image conteneur
-----------------------------

- Tag sémantique: `git tag -a vX.Y.Z -m "release" && git push --tags`
- Lancer le stack: `docker compose up -d --build`

Workflow de release GitHub (recommandé)
---------------------------------------

1. Créer une branche de release: `git checkout -b release/vX.Y.Z`
2. Mettre à jour version/changelog si besoin
3. Ouvrir une PR → squash & merge
4. Créer la Release GitHub: https://github.com/ALMAGNUS/datasens/releases/new
   - Tag: `vX.Y.Z`
   - Titre: `DataSens vX.Y.Z`
   - Notes: changements clés, compat, run (`docker compose up -d --build`)

Image GHCR (publication auto sur tag)
-------------------------------------
- Pull `latest`: `docker pull ghcr.io/almagnus/datasens:latest`
- Pull version: `docker pull ghcr.io/almagnus/datasens:${TAG}` (ex: `v0.2.0`)
- Run via compose: `IMAGE=ghcr.io/almagnus/datasens:latest docker compose up -d`


