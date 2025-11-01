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
