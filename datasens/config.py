"""
Configuration centralisée pour DataSens
Gestion de PROJECT_ROOT, .env, et chemins
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """
    Détecte PROJECT_ROOT de manière intelligente.
    
    Ordre de priorité:
    1. Dossier .git (si repo git)
    2. Fichier docker-compose.yml
    3. Fichier pyproject.toml
    4. Dossier datasens/ (package Python)
    5. Dossiers docs/ + notebooks/ ensemble
    
    Returns:
        Path: Chemin absolu de la racine du projet
        
    Raises:
        FileNotFoundError: Si la racine n'est pas trouvée
    """
    # Commencer par le fichier actuel si possible, sinon cwd
    try:
        current = Path(__file__).resolve().parent.parent
    except NameError:
        current = Path.cwd()
    
    # Chercher dans le dossier courant et ses parents
    for candidate in [current] + list(current.parents):
        # Priorité 1: dossier .git
        if (candidate / ".git").exists():
            logger.debug(f"PROJECT_ROOT détecté via .git: {candidate}")
            return candidate
        
        # Priorité 2: docker-compose.yml
        if (candidate / "docker-compose.yml").exists():
            logger.debug(f"PROJECT_ROOT détecté via docker-compose.yml: {candidate}")
            return candidate
        
        # Priorité 3: pyproject.toml
        if (candidate / "pyproject.toml").exists():
            logger.debug(f"PROJECT_ROOT détecté via pyproject.toml: {candidate}")
            return candidate
        
        # Priorité 4: dossier datasens/ (package)
        if (candidate / "datasens" / "__init__.py").exists():
            logger.debug(f"PROJECT_ROOT détecté via datasens/: {candidate}")
            return candidate
        
        # Priorité 5: docs/ + notebooks/
        if (candidate / "docs").exists() and (candidate / "notebooks").exists():
            logger.debug(f"PROJECT_ROOT détecté via docs+notebooks: {candidate}")
            return candidate
    
    raise FileNotFoundError(
        "PROJECT_ROOT introuvable. Assurez-vous d'être dans le projet DataSens "
        "ou qu'il contient .git, docker-compose.yml, ou datasens/"
    )


# Détection automatique de PROJECT_ROOT au chargement du module
try:
    PROJECT_ROOT = get_project_root()
    logger.info(f"✅ PROJECT_ROOT: {PROJECT_ROOT}")
except FileNotFoundError as e:
    logger.error(f"❌ {e}")
    PROJECT_ROOT = Path.cwd()


def load_config() -> Dict[str, Any]:
    """
    Charge la configuration depuis .env
    
    Returns:
        Dict: Configuration avec toutes les variables d'environnement
    """
    env_path = PROJECT_ROOT / ".env"
    
    if not env_path.exists():
        logger.warning(f"⚠️ Fichier .env introuvable: {env_path}")
        logger.info("💡 Copiez .env.example vers .env et remplissez les credentials")
        return {}
    
    # Charger .env
    load_dotenv(env_path)
    logger.info(f"✅ Configuration chargée depuis {env_path}")
    
    # Retourner un dict avec toutes les variables importantes
    config = {
        # PostgreSQL
        "PG_HOST": os.getenv("POSTGRES_HOST", os.getenv("PG_HOST", "localhost")),
        "PG_PORT": int(os.getenv("POSTGRES_PORT", os.getenv("PG_PORT", "5432"))),
        "PG_USER": os.getenv("POSTGRES_USER", os.getenv("PG_USER", "datasens_user")),
        "PG_PASS": os.getenv("POSTGRES_PASS", os.getenv("POSTGRES_PASSWORD", os.getenv("PG_PASS", ""))),
        "PG_DB": os.getenv("POSTGRES_DB", os.getenv("PG_DB", "datasens")),
        
        # MinIO
        "MINIO_ENDPOINT": os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        "MINIO_ACCESS_KEY": os.getenv("MINIO_ACCESS_KEY", "minio"),
        "MINIO_SECRET_KEY": os.getenv("MINIO_SECRET_KEY", "minio123"),
        "MINIO_BUCKET": os.getenv("MINIO_BUCKET", "datasens-raw"),
        
        # APIs
        "OWM_API_KEY": os.getenv("OWM_API_KEY", ""),
        "NEWSAPI_KEY": os.getenv("NEWSAPI_KEY", ""),
        "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID", ""),
        "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET", ""),
        "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY", ""),
        
        # Chemins
        "PROJECT_ROOT": PROJECT_ROOT,
        "DATA_DIR": PROJECT_ROOT / "data",
        "RAW_DIR": PROJECT_ROOT / "data" / "raw",
        "SILVER_DIR": PROJECT_ROOT / "data" / "silver",
        "GOLD_DIR": PROJECT_ROOT / "data" / "gold",
        "LOGS_DIR": PROJECT_ROOT / "logs",
        "MANIFESTS_DIR": PROJECT_ROOT / "data" / "raw" / "manifests",
    }
    
    return config


# Configuration globale chargée automatiquement
CONFIG = load_config()

# Exports des variables de configuration comme constantes de module
PG_HOST = CONFIG.get("PG_HOST", "localhost")
PG_PORT = CONFIG.get("PG_PORT", 5432)
PG_USER = CONFIG.get("PG_USER", "datasens_user")
PG_PASS = CONFIG.get("PG_PASS", "")
PG_DB = CONFIG.get("PG_DB", "datasens")

MINIO_ENDPOINT = CONFIG.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = CONFIG.get("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = CONFIG.get("MINIO_SECRET_KEY", "minio123")
MINIO_BUCKET = CONFIG.get("MINIO_BUCKET", "datasens-raw")

OWM_API_KEY = CONFIG.get("OWM_API_KEY", "")
NEWSAPI_KEY = CONFIG.get("NEWSAPI_KEY", "")
REDDIT_CLIENT_ID = CONFIG.get("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = CONFIG.get("REDDIT_CLIENT_SECRET", "")
YOUTUBE_API_KEY = CONFIG.get("YOUTUBE_API_KEY", "")

DATA_DIR = CONFIG.get("DATA_DIR", PROJECT_ROOT / "data")
RAW_DIR = CONFIG.get("RAW_DIR", PROJECT_ROOT / "data" / "raw")
SILVER_DIR = CONFIG.get("SILVER_DIR", PROJECT_ROOT / "data" / "silver")
GOLD_DIR = CONFIG.get("GOLD_DIR", PROJECT_ROOT / "data" / "gold")
LOGS_DIR = CONFIG.get("LOGS_DIR", PROJECT_ROOT / "logs")
MANIFESTS_DIR = CONFIG.get("MANIFESTS_DIR", PROJECT_ROOT / "data" / "raw" / "manifests")


def get_db_url() -> str:
    """
    Retourne l'URL de connexion PostgreSQL.
    
    Returns:
        str: URL PostgreSQL (postgresql://user:pass@host:port/db)
    """
    return f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"


def get_minio_config() -> Dict[str, str]:
    """
    Retourne la configuration MinIO.
    
    Returns:
        Dict: Configuration MinIO (endpoint, access_key, secret_key, bucket)
    """
    return {
        "endpoint": MINIO_ENDPOINT,
        "access_key": MINIO_ACCESS_KEY,
        "secret_key": MINIO_SECRET_KEY,
        "bucket": MINIO_BUCKET
    }
