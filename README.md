DataSens Project
================

Academic project scaffold for the DataSens platform. Managed via Jupyter notebooks and versioned on GitHub.

Repository layout
-----------------

- `data/`
  - `raw/` Bronze layer (raw sources)
  - `silver/` Cleaned datasets
  - `gold/` Final enriched datasets
  - `tmp/` Staging area
- `notebooks/` Execution notebooks grouped by blocks and versions
- `docs/` Data models, dictionaries, and generated READMEs
- `logs/` Snapshots, manifests, and execution logs
- `scripts/` Automation scripts (ingestion, checks, CRUD tests, pipeline)

Versioning
----------

Use tags to mark milestones:

- `E1_v1`: Prototype schema (10 tables) with simulated data
- `E1_v2`: Real data ingestion (18 tables, 5 sources)
- `E1_v3`: Full pipeline (36 tables, Prefect + MinIO + PostgreSQL)

Quickstart
----------

1. Create and activate a Python 3.10+ environment
2. Install dependencies: `pip install -r requirements.txt`
3. Open notebooks under `notebooks/datasens_E1_v1/`
4. Run `scripts/generate_readme.py` after completing a run to snapshot metadata


