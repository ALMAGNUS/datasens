"""
Collecteur Kaggle CSV
Ingestion de datasets Kaggle avec split 50/50
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
import logging
from sqlalchemy import text

from ..config import PROJECT_ROOT, RAW_DIR
from ..db import get_engine
from ..storage import MinIOClient
from ..utils import sha256_hash, ts

logger = logging.getLogger(__name__)


def _get_source_id(conn, nom: str) -> Optional[int]:
    """Récupère l'ID d'une source depuis t02_source"""
    result = conn.execute(
        text("SELECT id_source FROM datasens.t02_source WHERE nom = :nom"), 
        {"nom": nom}
    ).scalar()
    return result


def _create_flux(conn, source_nom: str, format_type: str = "csv", manifest_uri: str = None) -> int:
    """Crée un flux dans t03_flux"""
    sid = _get_source_id(conn, source_nom)
    if not sid:
        # Créer la source si elle n'existe pas
        tid = conn.execute(text("SELECT id_type_donnee FROM datasens.t01_type_donnee WHERE libelle = 'csv_file' LIMIT 1")).scalar()
        if not tid:
            tid = 1  # Fallback
        sid = conn.execute(text("""
            INSERT INTO datasens.t02_source(id_type_donnee, nom, url, fiabilite) 
            VALUES (:tid, :nom, '', 0.8) RETURNING id_source
        """), {"tid": tid, "nom": source_nom}).scalar()
    
    return conn.execute(text("""
        INSERT INTO datasens.t03_flux(id_source, format, manifest_uri, date_collecte)
        VALUES (:sid, :format, :manifest, NOW()) RETURNING id_flux
    """), {"sid": sid, "format": format_type, "manifest": manifest_uri}).scalar()


def _insert_documents(conn, df: pd.DataFrame, flux_id: int) -> int:
    """Insertion batch dans t04_document"""
    inserted = 0
    for _, row in df.iterrows():
        try:
            result = conn.execute(text("""
                INSERT INTO datasens.t04_document(id_flux, titre, texte, langue, date_publication, hash_fingerprint)
                VALUES(:fid, :titre, :texte, :langue, :date, :hash)
                ON CONFLICT (hash_fingerprint) DO NOTHING
                RETURNING id_document
            """), {
                "fid": flux_id,
                "titre": row.get("titre", ""),
                "texte": row.get("texte", ""),
                "langue": row.get("langue", "fr"),
                "date": row.get("date_publication"),
                "hash": row.get("hash_fingerprint", "")
            })
            if result.fetchone():
                inserted += 1
        except Exception as e:
            logger.warning(f"⚠️ Erreur insertion: {e}")
            continue
    return inserted


def collect_kaggle_csv(
    csv_path: Path,
    source_name: str = "Kaggle CSV",
    split_ratio: float = 0.5,
    max_rows: Optional[int] = None,
    engine = None
) -> Tuple[int, int, str]:
    """
    Collecte un dataset Kaggle CSV avec split PostgreSQL/MinIO.
    
    Args:
        csv_path: Chemin du fichier CSV Kaggle
        source_name: Nom de la source dans t02_source
        split_ratio: Ratio du split (0.5 = 50/50)
        max_rows: Nombre max de lignes à charger (None = tout)
        engine: SQLAlchemy engine (optionnel, en crée un si None)
        
    Returns:
        Tuple[int, int, str]: (nb_postgresql, nb_minio, minio_uri)
    """
    logger.info(f"📦 Collecte Kaggle CSV: {csv_path.name}")
    
    # Charger CSV
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {csv_path}")
    
    df = pd.read_csv(csv_path, nrows=max_rows)
    logger.info(f"📊 {len(df)} lignes chargées")
    
    # Split 50/50
    half = len(df) // 2
    df_postgresql = df[:half].copy()
    df_minio = df[half:].copy()
    
    # Préparer colonnes pour PostgreSQL
    if 'titre' not in df_postgresql.columns and 'texte' in df_postgresql.columns:
        df_postgresql['titre'] = df_postgresql['texte'].str[:100]
    if 'hash_fingerprint' not in df_postgresql.columns:
        df_postgresql['hash_fingerprint'] = df_postgresql.apply(
            lambda row: sha256_hash(str(row.get('titre', '')) + " " + str(row.get('texte', ''))), 
            axis=1
        )
    if 'langue' not in df_postgresql.columns:
        df_postgresql['langue'] = 'fr'
    if 'date_publication' not in df_postgresql.columns:
        df_postgresql['date_publication'] = pd.Timestamp.now(tz='UTC')
    
    logger.info(f"✂️ Split: {len(df_postgresql)} PostgreSQL + {len(df_minio)} MinIO")
    
    # Connexion et insertion PostgreSQL
    if engine is None:
        engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("SET search_path TO datasens, public"))
        
        # Créer flux
        flux_id = _create_flux(conn, source_name, "csv", f"s3://datasens-raw/kaggle/{csv_path.name}")
        
        # Insérer documents
        cols_needed = ['titre', 'texte', 'langue', 'date_publication', 'hash_fingerprint']
        df_pg_insert = df_postgresql[cols_needed]
        nb_postgresql = _insert_documents(conn, df_pg_insert, flux_id)
    
    logger.info(f"✅ PostgreSQL: {nb_postgresql} documents insérés")
    
    # Upload vers MinIO
    local_minio = RAW_DIR / "kaggle" / f"kaggle_split_{ts()}.csv"
    local_minio.parent.mkdir(parents=True, exist_ok=True)
    df_minio.to_csv(local_minio, index=False)
    
    try:
        minio_client = MinIOClient()
        minio_uri = minio_client.upload_file(local_minio, f"kaggle/{local_minio.name}")
        nb_minio = len(df_minio)
        logger.info(f"✅ MinIO: {nb_minio} documents uploadés - {minio_uri}")
    except Exception as e:
        logger.warning(f"⚠️ MinIO upload échoué: {e}")
        minio_uri = f"local://{local_minio}"
        nb_minio = len(df_minio)
    
    logger.info(f"✅ Collecte Kaggle terminée: {nb_postgresql} PG + {nb_minio} MinIO")
    return nb_postgresql, nb_minio, minio_uri
