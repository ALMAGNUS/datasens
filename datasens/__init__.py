"""
DataSens - Pipeline ETL Multi-Sources
Version E1_v3
"""

__version__ = "1.0.0"
__author__ = "ALMAGNUS"

# Imports différés pour éviter les problèmes de rechargement de modules
# Les utilisateurs doivent importer explicitement: from datasens.config import ...
__all__ = [
    "PROJECT_ROOT",
    "get_project_root",
    "load_config",
    "get_db_url",
    "get_minio_config",
    "get_engine",
    "execute_query",
    "insert_documents",
    "create_flux",
    "get_source_id",
    "MinIOClient",
    "sha256_hash",
    "ts",
    "ensure_directory",
    "collect_kaggle_csv",
]
