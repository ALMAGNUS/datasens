# 🧾 **FICHE TECHNIQUE — DUMPS EN IT & DATA (Projet DataSens)**

### *(Projet DataSens — Novembre 2025)*

---

## 🧠 **1️⃣ Définition**

Dans le cadre du projet **DataSens**, un **dump** désigne une **extraction brute et intégrale** d’une composante du système de données (base PostgreSQL, DataLake MinIO, pipeline Prefect, ou logs).

Il capture **l’état exact des données ou du pipeline à un instant T** afin d’assurer :

- la **traçabilité** (audit et conformité RGPD),
- la **sauvegarde technique** (rollback ou migration),
- et le **debug** (diagnostic de flux ETL).

> 🧩 Les dumps constituent un point de contrôle entre les couches raw, silver et gold du DataLake.

---

## 🗃️ **2️⃣ Typologie des dumps DataSens**

| Type | Description | Localisation / Format | Usage |
| --- | --- | --- | --- |
| **Database dump (PostgreSQL)** | Export structure + contenu des tables DataSens. | `data/backups/sql/*.sql` | Sauvegarde, migration ou rollback |
| **Object dump (MinIO)** | Copie brute des fichiers RAW (CSV, JSON, Parquet). | `data/raw/...` ou bucket MinIO | Préservation du brut avant transformation |
| **Log dump** | Export des logs ETL / Prefect. | `logs/*.log` | Debugging et audit des exécutions |
| **Metric dump** | Export des métriques techniques du pipeline. | `metrics/*.json` | Monitoring Grafana/Prometheus |
| **Vector dump** | Sauvegarde locale des embeddings IA. | `data/ai/faiss_index/` | Préservation du contexte sémantique |
| **Import trace** | Enregistrement des fichiers chargés en base. | `t38_dump_audit.table_cible` | Gouvernance RGPD / audit imports |

---

## 🧩 **3️⃣ Commandes types**

### 📦 **Dump PostgreSQL (utilitaire Python)**

```python
from pathlib import Path
from scripts.dump_restore_utils import dump_postgresql

dump_postgresql(
    engine=engine,
    output_dir=Path("data/backups/sql"),
    tables=["t04_document", "t05_annotation"],
    commentaire="Dump jury RAW→GOLD"
)
```

### 🔄 **Restauration contrôlée**

```python
from scripts.dump_restore_utils import restore_postgresql

restore_postgresql(
    engine=engine,
    dump_file=Path("data/backups/sql/datasens_dump_2025-11-04.sql")
)
```

### ☁️ **Dump MinIO (objets RAW)**

```python
from scripts.dump_restore_utils import dump_minio_objects

dump_minio_objects(
    minio_client=minio_client,
    bucket="datasens-raw",
    prefix="rss/",
    output_dir=Path("data/backups/raw"),
    commentaire="Snapshot flux RSS"
)
```

### 🧠 **Import supervisé**

```python
from scripts.dump_restore_utils import import_file_to_table

import_file_to_table(
    engine=engine,
    file_path=Path("data/external/barometre.csv"),
    table_name="t29_document_baro",
    schema="public",
    commentaire="Import baromètre Q4"
)
```

---

## ⚙️ **4️⃣ Intégration dans l'architecture DataSens**

```
        ┌───────────────┐
        │    Sources     │
        │ (API, CSV, Web)│
        └──────┬─────────┘
               │
        🔻 DUMP RAW (MinIO)
               │
        ┌──────┴─────────┐
        │  Préparation    │  →  ETL Prefect
        │ (Silver Layer)  │
        └──────┬─────────┘
               │
        🔻 DUMP SQL (PostgreSQL)
               │
        ┌──────┴──────────┐
        │   Data Gold      │  →  Streamlit / Grafana
        └──────────────────┘
```

> 📘 Chaque couche du DataLake peut générer un dump versionné et horodaté, enregistré dans `t38_dump_audit`.

---

## 🔐 **5️⃣ Bonnes pratiques DataSens**

| Recommandation | Description | Outil / Commande |
| --- | --- | --- |
| 🕓 **Nommer et horodater** | `datasens_pgsql_dump_YYYY-MM-DD.sql` | Bash / Prefect |
| 🔒 **Chiffrer les dumps sensibles** | Données nominatives → chiffrement AES-256 | MinIO / GPG |
| 🌀 **Automatiser la rotation** | Garder les 7 derniers dumps | Cron / Prefect |
| 🔍 **Vérifier la restauration** | Test hebdo sur base de staging | PostgreSQL |
| 📊 **Centraliser les métadonnées** | Cataloguer les dumps dans `t38_dump_audit` | SQLAlchemy |
| 📈 **Monitorer les dumps** | Durée, taille, fréquence | Grafana + Prometheus |

---

## 🧱 **6️⃣ Exemple de table de traçabilité (`t38_dump_audit`)**

| dump_id | type | chemin | taille_mb | date_creation | table_cible | utilisateur | commentaire |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 101 | SQL | `data/backups/sql/datasens_dump_2025-11-04.sql` | 142 | 2025-11-04 10:32 | `*` | `alan_jaffre` | Dump avant migration silver |
| 118 | RAW | `data/backups/raw/minio_rss_2025-11-04/` | 23 | 2025-11-04 10:45 | `NULL` | `prefect_bot` | Snapshot RSS |
| 125 | IMPORT | `data/external/barometre.csv` | 5 | 2025-11-04 11:02 | `public.t29_document_baro` | `analyste_gold` | Import baromètre Q4 |

---

## 🧩 **7️⃣ Gouvernance et sécurité**

- Conformité **RGPD** : renseigner `date_expiration` et purger régulièrement via `t38_dump_audit`.
- Validation manuelle obligatoire avant **réimport** en environnement Gold.
- Sauvegardes stockées sur **MinIO** (versioning activé) + copie locale `data/backups`.
- Audit central : `t38_dump_audit` + logs `dump_restore_utils`.

---

## 🔁 **8️⃣ Usage opérationnel**

| Rôle | Action | Objectif |
| --- | --- | --- |
| **Data Engineer** | Lance `dump_postgresql`, `dump_minio_objects`, configure rotation | Traçabilité technique |
| **Data Analyst** | Utilise les dumps/imports pour tests et validation | Vérification cohérence |
| **Data Steward** | Suit `t38_dump_audit`, gère `date_expiration`, statut | Gouvernance/RGPD |
| **Responsable IA** | Archive vector dumps, supervise imports IA | Réentraînement modèle IA |

---

## 📘 **9️⃣ Synthèse finale**

> 🧠 Dans DataSens, un dump est un **événement de gouvernance** : il déclenche log, audit et scripts de restauration.
>
> ✅ **Objectif** : garantir la transparence et la reproductibilité des transformations CTM.
>
> 📊 *Chaque dump/import = un jalon auditable, réversible et monitoré dans `t38_dump_audit`.*
>
> **Stack concernée** : VS Code Notebooks · PostgreSQL · MinIO · Prefect · Grafana.

---

## 🚀 **🔟 Implémentation DataSens**

### **Table `t38_dump_audit` (PostgreSQL)**

```sql
CREATE TABLE IF NOT EXISTS t38_dump_audit (
    dump_id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,  -- 'SQL', 'RAW', 'LOG', 'METRIC', 'VECTOR'
    chemin TEXT NOT NULL,
    taille_mb FLOAT,
    date_creation TIMESTAMP DEFAULT NOW(),
    utilisateur VARCHAR(100),
    commentaire TEXT,
    checksum_sha256 VARCHAR(64),
    statut VARCHAR(20) DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'ARCHIVE', 'SUPPRIME')),
    date_expiration TIMESTAMP
);
```

### **Fonctions Python pour dumps**

Centralisées dans `scripts/dump_restore_utils.py` et importées dans les notebooks (`02_schema_create`, `03_ingest_sources`, `05_snapshot_and_readme`, `06_dump_and_restore`).

### **Automation Prefect**

Les flows Prefect (E2) incluront automatiquement des dumps avant chaque étape critique du pipeline.

