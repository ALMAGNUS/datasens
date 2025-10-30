# DataSens – Dictionnaire de nommage & arborescence officielle

# 🧩 1️⃣ Structure globale du projet

```text
datasens_project/
│
├── data/                          # Datalake local (3 zones)
│   ├── raw/        ← Bronze : données brutes
│   ├── silver/     ← Silver : données nettoyées
│   └── gold/       ← Gold : données finales prêtes à l'analyse
│
├── notebooks/                     # Exécution pas à pas (.ipynb)
│   ├── datasens_E1_v1.ipynb
│   ├── datasens_E2_v1.ipynb
│   ├── datasens_E3_v1.ipynb
│   └── ... (autres versions si mises à jour)
│
├── docs/                          # Documentation du projet
│   ├── datasens_dictionary.md
│   ├── datasens_sources_dictionary.md
│   ├── datasens_MCD.md
│   ├── datasens_MLD.md
│   ├── datasens_MPD.sql
│   └── README_E1.md
│
├── logs/                          # Logs d’exécution, manifestes JSON
│   ├── manifest_2025_10_29.json
│   └── exec_logs_YYYYMMDD.txt
│
├── scripts/                       # Scripts utilitaires et batch
│   ├── fetch_sources_summary.py
│   ├── load_to_postgres.py
│   └── quality_checks.py
│
└── .env                           # Variables d’environnement locales
```

# 📗 2️⃣ Nommage des notebooks officiels (.ipynb)

| **Notebook** | **Nommage standard** | **Rôle / contenu principal** | **Zone du datalake** |
| --- | --- | --- | --- |
| E1 – Base de données & Ingestion | datasens_E1_v1.ipynb | Création DB, CRUD, ingestion 5 sources | raw/, silver/ |
| E2 – Annotation IA & émotions | datasens_E2_v1.ipynb | Traitement NLP, détection des émotions | silver/, gold/ |
| E3 – Visualisation & dashboards | datasens_E3_v1.ipynb | Grafana, Streamlit, analyse temporelle | gold/ |
| E4 – Orchestration & monitoring | datasens_E4_v1.ipynb | Prefect Flow, Prometheus, logs | gold/ |
| E5 – IA responsable & audit | datasens_E5_v1.ipynb | RGPD, transparence, rapports finaux | gold/ |

🔁 Les versions ultérieures suivent le schéma : `datasens_EX_v2.ipynb`, `datasens_EX_v3.ipynb` etc. (toujours incrémentées lors des remaniements importants)

# 📙 3️⃣ Nommage des notebooks E1 détaillés (sous-découpage pas à pas)

Pour garder la granularité des 5 notebooks internes E1 définis :

| **Étape** | **Nom fichier** | **Description** |
| --- | --- | --- |
| 1️⃣ | 01_setup_env.ipynb | Préparation de l’environnement, arborescence, .env, Git init |
| 2️⃣ | 02_schema_create.ipynb | Création du schéma SQL (DDL) + index + référentiels |
| 3️⃣ | 03_ingest_sources.ipynb | Ingestion des 5 sources réelles + tracking flux |
| 4️⃣ | 04_crud_tests.ipynb | Tests CRUD, lecture, update, suppression |
| 5️⃣ | 05_snapshot_and_readme.ipynb | Sauvegardes, bilans, exports et versionning Git |

Ces notebooks internes sont contenus logiquement dans le notebook principal `datasens_E1_v1.ipynb` (qui sert de “table des matières”).

# 🧱 4️⃣ Nommage des datasets & fichiers DataLake

**📂 Zone Raw (Bronze)** — Données brutes, non transformées (`data/raw/`)

```text
data/raw/
├── kaggle_media_2025_10.csv
├── openweather_2025_10.json
├── monaviscitoyen_2025_10.html
├── gdelt_gkg_2025_10.tsv
└── insee_indicateurs_2025_10.csv
```

**📂 Zone Silver** — Données nettoyées, structurées et validées (`data/silver/`)

```text
data/silver/
├── documents_clean_2025_10.csv
├── meteo_normalized_2025_10.csv
├── indicateurs_joined_2025_10.csv
└── themes_mapping_2025_10.csv
```

**📂 Zone Gold** — Données finales, prêtes pour IA / visualisation (`data/gold/`)

```text
data/gold/
├── barometre_emotions_fr_2025_10.csv
├── dataset_annotated_v1.parquet
└── dashboard_export_2025_10.json
```

# 🗂️ 5️⃣ Nommage des fichiers de documentation

| **Fichier** | **Description** |
| --- | --- |
| datasens_dictionary.md | Dictionnaire complet des tables |
| datasens_sources_dictionary.md | Inventaire des sources collectées |
| datasens_MCD.md | Modèle Conceptuel de Données (Mermaid + explications) |
| datasens_MLD.md | Modèle Logique de Données |
| datasens_MPD.sql | Script SQL complet de création de la BDD |
| README_E1.md | Fiche projet E1 (objectifs, livrables, environnement) |
| README_global.md | Présentation générale du projet DataSens |

# 🧭 6️⃣ Nommage des fichiers logs & manifests

| **Fichier** | **Contenu** | **Format** |
| --- | --- | --- |
| logs/manifest_YYYY_MM_DD.json | Résumé des flux collectés (chemins, volume, temps, erreurs) | JSON |
| logs/exec_logs_YYYYMMDD.txt | Journal d’exécution notebook ou pipeline | TXT |
| logs/errors_YYYYMMDD.txt | Logs d’erreurs SQL / ingestion | TXT |

Exemple :

```json
{
  "date_run": "2025-10-29T16:45:00",
  "flux_ingérés": ["kaggle_media", "owm_meteo"],
  "documents_crees": 1520,
  "erreurs": 0,
  "auteur": "Alan Jaffré",
  "version": "E1_v1"
}
```

# 🧮 7️⃣ Convention de versionning & commit Git

| **Élément** | **Règle** |
| --- | --- |
| Version | E{bloc}_v{num} (ex: E1_v1, E1_v2, E2_v1) |
| Tag Git | E1_REAL_YYYYMMDD pour chaque jalon majeur |
| Message commit | feat(E1): ajout CRUD meteo / fix: correction FK indicateur |
| Branch principale | main (livrable validé) |
| Branch de dev | dev_e1, dev_e2 etc. |
| Rollback | retour via tag précédent (`git checkout tags/E1_REAL_2025_10_29`) |

# 🧠 8️⃣ Récapitulatif visuel global

```text
datasens_project/
│
├── data/
│   ├── raw/        → Données brutes (Bronze)
│   ├── silver/     → Données nettoyées (Silver)
│   └── gold/       → Données finales (Gold)
│
├── notebooks/
│   ├── datasens_E1_v1.ipynb
│   ├── datasens_E2_v1.ipynb
│   ├── ...
│   ├── 01_setup_env.ipynb
│   ├── 02_schema_create.ipynb
│   ├── 03_ingest_sources.ipynb
│   ├── 04_crud_tests.ipynb
│   └── 05_snapshot_and_readme.ipynb
│
├── docs/
│   ├── datasens_dictionary.md
│   ├── datasens_sources_dictionary.md
│   ├── datasens_MCD.md
│   ├── datasens_MLD.md
│   ├── datasens_MPD.sql
│   └── README_E1.md
│
├── logs/
│   ├── manifest_2025_10_29.json
│   └── exec_logs_2025_10_29.txt
│
├── scripts/
│   ├── fetch_sources_summary.py
│   ├── load_to_postgres.py
│   └── quality_checks.py
│
└── .env
```
