# 🔗 **Intégration des Dumps dans le Plan DataSens E1_v3**

## ✅ **Intégration réalisée**

### **1. Table `t38_dump_audit` dans le DDL PostgreSQL**

✅ **Ajoutée dans `docs/datasens_MPD.sql`** :
- Table `t38_dump_audit` (T38 selon nomenclature E1_v3)
- Index pour performance (type, date, statut, table_cible)
- Contraintes d'intégrité (unique_chemin)
- Support pour tous les types de dumps (SQL, RAW, LOG, METRIC, VECTOR, IMPORT)

### **2. Module utilitaire Python**

✅ **Créé `scripts/dump_restore_utils.py`** :
- `dump_postgresql()` : Génère dump SQL + enregistre dans `t38_dump_audit`
- `restore_postgresql()` : Restaure dump SQL avec vérification checksum
- `import_file_to_table()` : Importe CSV/JSON/Parquet → PostgreSQL + audit
- `dump_minio_objects()` : Dump objets MinIO → local + audit
- `list_dumps()` : Liste les dumps enregistrés

### **3. Utilisation dans les notebooks**

#### **Dans `02_schema_create.ipynb`** :
- La table `t38_dump_audit` est créée automatiquement avec le DDL complet

#### **Dans `03_ingest_sources.ipynb`** (à ajouter) :
- Option de dump avant chaque collecte critique
- Import de fichiers externes vers tables PostgreSQL

#### **Dans `05_snapshot_and_readme.ipynb`** (à ajouter) :
- Consultation de `t38_dump_audit` pour traçabilité
- Export des métadonnées de dumps

---

## 📋 **Exemple d'utilisation dans un notebook**

```python
# Dans n'importe quel notebook E1_v3
from pathlib import Path
from scripts.dump_restore_utils import import_file_to_table, dump_postgresql, list_dumps

# 1. Importer un fichier CSV dans une table PostgreSQL
import_file_to_table(
    engine=engine,
    file_path=Path("data/external/dataset_externe.csv"),
    table_name="t04_document",
    schema="public",
    if_exists="append",
    commentaire="Import dataset externe pour enrichissement"
)

# 2. Créer un dump PostgreSQL avant une opération critique
dump_file = dump_postgresql(
    engine=engine,
    output_dir=Path("data/backups/sql"),
    tables=["t04_document", "t05_annotation"],  # Tables spécifiques
    commentaire="Dump avant migration silver → gold"
)

# 3. Lister tous les dumps
df_dumps = list_dumps(engine, type_filter="IMPORT", statut="ACTIF")
print(df_dumps)
```

---

## 🔄 **Workflow intégré dans le pipeline E1_v3**

```
01_setup_env.ipynb
    ↓
02_schema_create.ipynb
    → Crée t38_dump_audit automatiquement
    ↓
03_ingest_sources.ipynb
    → Option: dump avant collecte
    → Option: import fichiers externes → tables
    ↓
04_crud_tests.ipynb
    → Tests incluant vérification t38_dump_audit
    ↓
05_snapshot_and_readme.ipynb
    → Consultation t38_dump_audit pour traçabilité
    → Export métadonnées dumps
```

---

## 📊 **Structure de la table `t38_dump_audit`**

| Colonne | Type | Description |
| --- | --- | --- |
| `dump_id` | INT | PK auto-incrémenté |
| `type` | VARCHAR(50) | 'SQL', 'RAW', 'LOG', 'METRIC', 'VECTOR', 'IMPORT' |
| `chemin` | TEXT | Chemin local ou URI MinIO |
| `taille_mb` | FLOAT | Taille en MB |
| `date_creation` | TIMESTAMP | Date/heure du dump |
| `utilisateur` | VARCHAR(100) | Utilisateur qui a créé le dump |
| `commentaire` | TEXT | Commentaire libre |
| `checksum_sha256` | VARCHAR(64) | Checksum pour vérification intégrité |
| `statut` | VARCHAR(20) | 'ACTIF', 'ARCHIVE', 'SUPPRIME' |
| `date_expiration` | TIMESTAMP | Date d'expiration (RGPD) |
| `minio_uri` | TEXT | URI MinIO si stocké dans DataLake |
| `table_cible` | VARCHAR(100) | Table PostgreSQL si type='IMPORT' |

---

## 🎯 **Avantages de l'intégration**

1. **Traçabilité complète** : Tous les dumps sont enregistrés dans PostgreSQL
2. **Réutilisable** : Module `dump_restore_utils.py` utilisable dans tous les notebooks
3. **Cohérent** : Respecte la nomenclature T01-T38 du MPD
4. **Flexible** : Fonctions autonomes, pas besoin de notebook dédié
5. **Auditable** : Consultation de `t38_dump_audit` pour gouvernance

---

## 🚀 **Prochaines étapes**

- ✅ Table `t38_dump_audit` ajoutée au DDL
- ✅ Module `dump_restore_utils.py` créé
- 🔄 Tester `import_file_to_table()` dans un notebook
- 🔄 Ajouter consultation `t38_dump_audit` dans `05_snapshot_and_readme.ipynb`

---

## 📝 **Références**

- `docs/FICHE_DUMPS_DATASENS.md` : Fiche technique complète
- `docs/IMPLEMENTATION_DUMPS.md` : Plan d'implémentation détaillé
- `docs/datasens_MPD.sql` : DDL complet avec `t38_dump_audit`
- `scripts/dump_restore_utils.py` : Module utilitaire

