# 🚀 Guide Technique DataSens E1 – Notebook Académique

> Public cible: Jury + apprenant. Objectif: transparence, traçabilité, reproductibilité.

## 📦 Table des Matières
1. Vue d’ensemble du projet
2. Approche « code inline » (sans .py)
3. Dépendances expliquées (par familles)
4. Architecture du notebook (01→05) et pipeline ETL
5. Logging et Troubleshooting (production-ready)
6. Ingest multi-sources (5 types) et normalisation
7. Base de données (Merise→Relationnel) et CRUD/QA
8. Visualisations et métriques
9. Docker, GitHub, Versioning (tags/releases)
10. Glossaire et Questions Jury

---

## 🎯 Vue d’ensemble
- E1_v1: 10 tables Pareto, données simulées (Faker), CRUD + snapshot
- E1_v2: 18 tables, 5 sources réelles (RSS, API, Scraping, Kaggle, GDELT), MinIO + PostgreSQL
- E1_v3: 36 tables, pipeline Prefect, stockage objet (MinIO) + SGBD (PostgreSQL)

Valeur: démontrer une collecte multi-sources robuste, traçable, et lisible pour audit.

---

## 💡 Approche « code inline »
- Transparence: tout le code dans les cellules (pas de modules .py)
- Simplicité: debugging immédiat, logs in-notebook
- Robustesse: try/except par source, fallback gracieux
- Reproductibilité: 1 .ipynb + requirements → exécution

Exemple: API Reddit/YouTube directement dans la cellule (pas de « boîte noire »).

---

## 🧱 Dépendances (pourquoi et quand)
- Données: pandas, numpy → DataFrames/ops
- DB: SQLAlchemy, psycopg2-binary → PostgreSQL (DDL/DML), text() paramétré
- Collecte: requests, feedparser, bs4 → APIs/RSS/HTML
- Stockage objet: minio → DataLake S3-like
- Orchestration (E1_v3): prefect → flows
- Viz: matplotlib, seaborn → graphiques
- Utilitaires: hashlib (SHA256), datetime, dotenv (.env)

---

## 🧭 Architecture notebook (01→05)
1) Setup env + logging + versioning (manifest, README_VERSIONNING)
2) Schéma BDD (SQLite E1_v1 / PostgreSQL E1_v2-v3)
3) Ingestion sources (simulées vs réelles) + normalisation
4) CRUD/QA: dédup, nulls, intégrité, counts
5) Snapshot + manifest JSON + affichage historique

ETL: EXTRACT → TRANSFORM (clean/annotate/dedup) → LOAD (PG + MinIO) → Viz/QA → Snapshot.

---

## 🧾 Logging & Troubleshooting
- Fichiers: logs/collecte_YYYYMMDD_HHMMSS.log (INFO), logs/errors_*.log (ERROR+traceback)
- Console: messages lisibles pour la démo
- Tips: vérifier .env (clés), services (PostgreSQL/MinIO), quotas APIs; redémarrer kernel si besoin

Bénéfices: traçabilité jury, audit, débogage sans rerun complet.

---

## 🌐 Ingestion multi-sources (5 types)
- Fichier plat (Kaggle CSV)
- Base de données (Kaggle DB)
- Web Scraping (Reddit, YouTube, SignalConso, Trustpilot, Vie Publique, Data.gouv)
- APIs (OpenWeatherMap, NewsAPI, RSS Multi)
- Big Data (GDELT GKG France)

Principes:
- Format unifié → {titre, texte, date_publication, langue, source}
- Déduplication → SHA256 (titre + texte[:500])
- Stockage dual → PostgreSQL (structuré) + MinIO (raw)
- Manifest JSON → traçabilité run (bucket, sources, timestamps)

---

## 🗄️ Base de données & CRUD/QA
- Merise→Relationnel: type_donnee, source, flux, document, territoire, indicateur, meteo, etc.
- Clés: PK SERIAL, FKs, index UNIQUE(hash_fingerprint)
- CRUD demo: insert/select/update/delete document
- QA checks: doublons, nulls, intégrité FK, counts par source

E1_v1: SQLite (faciliter la démo) → E1_v2/v3: PostgreSQL (productisation).

---

## 📊 Visualisations
- Volumes par source/type
- Distributions (longueurs, catégories)
- Time-series (évolution)
- Heatmap (sentiment moyen par source/catégorie)

Objectif: montrer la valeur métier et la qualité pipeline.

---

## 🐳 Docker, GitHub, Versioning
- Docker Compose (optionnel) → Postgres + Jupyter + MinIO
- Git: commits clairs, tags jalons: E1_v0 (scaffold), E1_v1, E1_v2, E1_v3
- Releases GitHub: titre + description (fonctionnalités, livrables, installation)
- Badges README: release, stars, issues, code size

---

## 📚 Glossaire rapide
ETL, Pipeline, Fingerprint (SHA256), ORM, DataFrame, Regex, Hash, Cardinalité, Context Manager, UPSERT.

---

## 🎤 Questions Jury (exemples)
- Pourquoi RSS plutôt que scraping agressif? → légal, stable, structuré
- Montée en charge? → pooling SQLAlchemy, index, batching; E1_v3: orchestration Prefect
- Déduplication fiable? → hash SHA256, normalisation texte, upsert UNIQUE
- Robustesse? → try/except par source, logs erreurs + fallback

---

## ✅ Checklist démo
- Services OK (PostgreSQL/MinIO), .env rempli
- `pip install -r requirements.txt`
- Exécuter notebooks 01→05 (E1_v1 puis E1_v2)
- Vérifier logs, manifest, badges, tags

Références: notebooks `notebooks/datasens_E1_v*/` et ce guide.
