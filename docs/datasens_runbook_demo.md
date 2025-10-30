DataSens — Runbook Démo (10–15 min)
===================================

Objectif
--------
Démontrer ingestion → normalisation → QA → stockage → CRUD → viz dans un seul notebook, sans `.py` externes pendant la démo.

Prérequis
--------
- Python 3.10+
- `pip install -r requirements.txt`
- Optionnel: PostgreSQL local via `DATASENS_PG_DSN`
- Optionnel: MinIO (fallback `data/raw/`)

Variables d’environnement (optionnel)
-------------------------------------
- `DATASENS_PG_DSN` (défaut: `postgresql+psycopg2://postgres:postgres@localhost:5432/postgres`)
- `NEWSAPI_KEY`, `OPENWEATHER_API_KEY`, etc.
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET`

Étapes
------
1. Ouvrir le dernier notebook E1 et exécuter toutes les cellules.
2. Observer le logging inline et vérifier `logs/collecte_*.log` et `logs/errors_*.log`.
3. Confirmer le schéma normalisé: `titre, texte, source_site, url, date_publication, langue` + `hash_fingerprint` (SHA256) et dédoublonnage.
4. Vérifier le QA (longueur minimale, nettoyage de base).
5. Vérifier l’insert PostgreSQL et un CRUD minimal (SELECT/UPDATE/DELETE).
6. Afficher 1–2 graphiques (documents par source/date/langue).

Note E2 — Annotation FR
-----------------------
- Modèles par défaut: CamemBERT puis FlauBERT (priorité FR)
- Sentiment/Polarité et NER en français; heuristiques si modèles absents

Tolérances
----------
- Clés API manquantes: sources sautées (log), exécution continue.
- MinIO manquant: écriture locale `data/raw/`.
- PostgreSQL manquant: définir `DATASENS_PG_DSN` ou démarrer une instance locale.


