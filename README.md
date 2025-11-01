DataSens — Projet
=================

Voir le guide technique: docs/GUIDE_TECHNIQUE_E1.md

![GitHub Release](https://img.shields.io/github/v/release/ALMAGNUS/datasens?include_prereleases)
![GitHub Stars](https://img.shields.io/github/stars/ALMAGNUS/datasens?style=social)
![GitHub Issues](https://img.shields.io/github/issues/ALMAGNUS/datasens)
![Code Size](https://img.shields.io/github/languages/code-size/ALMAGNUS/datasens)
![License](https://img.shields.io/github/license/ALMAGNUS/datasens)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Last Commit](https://img.shields.io/github/last-commit/ALMAGNUS/datasens)
[![Security](https://img.shields.io/badge/Security-Policy-blue.svg)](SECURITY.md)
[![Contributing](https://img.shields.io/badge/Contributing-Guide-orange.svg)](CONTRIBUTING.md)

Liens rapides
-------------

- 📦 **Dépôt** : https://github.com/ALMAGNUS/datasens
- 🐛 **Issues** : https://github.com/ALMAGNUS/datasens/issues
- 🚀 **Releases** : https://github.com/ALMAGNUS/datasens/releases
- 💬 **Discussions** : https://github.com/ALMAGNUS/datasens/discussions
- 🔀 **Pull Requests** : https://github.com/ALMAGNUS/datasens/pulls
- 🔒 **Sécurité** : [SECURITY.md](SECURITY.md)
- 🤝 **Contribuer** : [CONTRIBUTING.md](CONTRIBUTING.md)

Description
-----------

**DataSens** est un **pipeline ETL complet d'annotation et de structuration de dataset pour l'IA**.

### 🎯 Vision du Projet

DataSens est un **bouffeur de données** et un **classifieur performant** qui :

1. **Collecte** depuis **6 types de sources** :
   - 📄 **Fichier plat** (CSV Kaggle)
   - 🗄️ **Base de données** (SQLite/PostgreSQL)
   - 🌐 **API REST** (OpenWeatherMap, NewsAPI)
   - 🕷️ **Web Scraping** (Reddit, YouTube, Vie-publique, data.gouv)
   - 🌍 **Big Data** (GDELT GKG - Global Knowledge Graph)
   - 📊 **Baromètres d'opinion** (INSEE, IFOP, ADEME - en préparation E2)

2. **Transforme et Structure** :
   - **Déduplication** SHA256 pour éviter les doublons
   - **Nettoyage** et normalisation (texte, dates, langues)
   - **Classification professionnelle** selon standards Médiamétrie (Nomenclature, Données Maîtres, Opérationnelles, Décisionnelles, Métadonnées)
   - **Annotation simple** (E1_v3) : nettoyage, déduplication, QA de base
   - **Annotation IA avancée** (E2) : CamemBERT, FlauBERT pour sentiment, NER, keywords

3. **Charge et Stocke** :
   - **PostgreSQL** : Données structurées (36/37 tables Merise) pour requêtes SQL
   - **MinIO DataLake** : Données brutes (S3-like) pour analyses Big Data
   - **Stockage hybride** : 50/50 split selon type de source

4. **CRUD Complet** :
   - **CREATE** : Insertion multi-sources avec traçabilité
   - **READ** : Requêtes jointes complexes avec visualisations
   - **UPDATE** : Mise à jour contrôlée
   - **DELETE** : Suppression avec intégrité référentielle

### 🚀 Pipeline ETL Multi-Sources

**Extract → Transform → Load** avec :
- ✅ Logging structuré (fichiers + traceback)
- ✅ Gestion d'erreurs robuste (try/except + fallback)
- ✅ Déduplication automatique (SHA256 fingerprinting)
- ✅ Traçabilité complète (flux, manifests JSON, versioning Git)
- ✅ Visualisations à chaque étape (pandas + matplotlib)
- ✅ Contrôles qualité (doublons, NULL, intégrité FK)

### 📊 Export Dataset Structuré pour IA

Le pipeline génère un **dataset nettoyé et annoté**, prêt pour enrichissement IA :
- Format **Parquet** (optimisé pour ML/IA)
- Format **CSV** (compatibilité)
- Export dans `data/gold/dataset_ia/`
- Métadonnées complètes (source, type, thèmes, territoire)

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
- `E1_v2`: Ingestion réelle (18 tables, 6 sources)
- `E1_v3`: Pipeline complet (36/37 tables, MinIO + PostgreSQL) - **Dataset structuré pour IA**

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
4. Vérifier l'insertion PostgreSQL et un CRUD minimal (SELECT/UPDATE/DELETE).
5. Afficher 1–2 graphiques (documents par source/date/langue).

Configuration Flexible des Sources
-----------------------------------

**🎯 Toutes les sources sont configurées dans `config/sources_config.json`**

- **Pour ajouter/modifier une source** : Éditez simplement le JSON selon `config/README_SOURCES.md`, puis implémentez la collecte dans `03_ingest_sources.ipynb`
- **Structure académique** : Le notebook reste organisé source par source pour la clarté pédagogique
- **Types de collecteurs** : CSV, API REST, RSS, Web Scraping, GDELT Big Data, PDF

Voir `docs/AUDIT_E1_V3.md` pour l'état complet des sources implémentées.

Variables d'environnement
-------------------------

**📄 Template** : Copier `.env.example` vers `.env` et remplir vos valeurs.

Variables principales :
- **PostgreSQL** : `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASS`
- **MinIO DataLake** : `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET`
- **API Keys** (optionnelles) : `OWM_API_KEY`, `NEWSAPI_KEY`, `KAGGLE_USERNAME`, `KAGGLE_KEY`, `REDDIT_CLIENT_ID`, `YOUTUBE_API_KEY`

**🔒 Sécurité** : 
- Le fichier `.env` est ignoré par Git
- Requêtes SQL paramétrées pour prévenir injection SQL
- Fonctions de validation implémentées (`assert_valid_identifier`, `load_whitelist_tables`)
- Voir [SECURITY.md](SECURITY.md) pour les détails complets

Annotation Simple (E1_v3) - Préparation Dataset pour E2
--------------------------------------------------------

**E1_v3** : Annotation simple pour préparer le dataset à l'enrichissement IA (E2)

- **Nettoyage** : Normalisation de base (texte, encodage)
- **Détection de langue** : Identification automatique (priorité FR)
- **Déduplication** : SHA256 fingerprint pour éviter doublons
- **QA de base** : Validation format, longueur minimale, champs requis

**E2** (à venir) : Annotation IA avancée avec CamemBERT et FlauBERT
- Sentiment/polarité (modèles FR)
- NER (spaCy modèle FR)
- Mots-clés (YAKE FR)

Classification Types de Données (Médiamétrie)
---------------------------------------------

Les types de données suivent la classification professionnelle :
- **Nomenclature** : Données de classification (mensuelle)
- **Données Maîtres** : Données de référence (quotidienne)
- **Données Opérationnelles** : Données d'activité (secondes)
- **Données Décisionnelles** : Données d'analyse (quotidienne)
- **Métadonnées** : Données sur les données (variable)

Export Dataset Préparé (E1_v3)
-------------------------------

- **E1_v3** : Dataset nettoyé et annoté simplement, prêt pour enrichissement IA (E2)
- Parquet partitionné (date/langue/source), ex:
  - `data/gold/annotated/date=YYYY-MM-DD/langue=fr/source=reddit/part.parquet`
- **E2** : Enrichissement IA avec CamemBERT et FlauBERT sur le dataset E1_v3

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


