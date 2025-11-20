"""
Collecteur GDELT (Global Database of Events, Language and Tone)
BigData : Téléchargement et parsing des fichiers GKG (Global Knowledge Graph)
"""

import pandas as pd
import requests
import zipfile
import io
from pathlib import Path
from typing import List, Tuple, Optional
import logging
from sqlalchemy import text
from datetime import datetime, timedelta

from ..config import RAW_DIR
from ..storage import MinIOClient
from ..utils import sha256_hash, ts
from ..retry import retry_on_network_error

logger = logging.getLogger(__name__)

# Colonnes GDELT GKG v2.1 (Global Knowledge Graph)
GDELT_GKG_COLUMNS = [
    'GKGRECORDID', 'DATE', 'SourceCollectionIdentifier', 'SourceCommonName',
    'DocumentIdentifier', 'V1Counts', 'V2Counts', 'V1Themes', 'V2Themes',
    'V1Locations', 'V2Locations', 'V1Persons', 'V2Persons', 'V1Organizations',
    'V2Organizations', 'V1Tone', 'V2Tone', 'Dates', 'GCAM', 'SharingImage',
    'RelatedImages', 'SocialImageEmbeds', 'SocialVideoEmbeds', 'Quotations',
    'AllNames', 'Amounts', 'TranslationInfo', 'Extras'
]


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
        tid = conn.execute(text(
            "SELECT id_type_donnee FROM datasens.t01_type_donnee WHERE libelle = 'gdelt_events' LIMIT 1"
        )).scalar()
        if not tid:
            tid = 1
        
        sid_result = conn.execute(text("""
            INSERT INTO datasens.t02_source(id_type_donnee, nom, url, fiabilite) 
            VALUES (:tid, :nom, 'http://data.gdeltproject.org', 0.8) 
            RETURNING id_source
        """), {"tid": tid, "nom": source_nom})
        sid = sid_result.fetchone()[0]
    
    flux_result = conn.execute(text("""
        INSERT INTO datasens.t03_flux(id_source, format, manifest_uri, date_collecte)
        VALUES (:sid, :format, :manifest, NOW()) RETURNING id_flux
    """), {"sid": sid, "format": format_type, "manifest": manifest_uri})
    return flux_result.fetchone()[0]


@retry_on_network_error(max_retries=3)
def _download_gdelt_file(url: str) -> bytes:
    """Télécharge fichier GDELT avec retry"""
    logger.info(f"📥 Téléchargement: {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def collect_gdelt_gkg(
    date_str: str = None,
    source_name: str = "GDELT Global Knowledge Graph",
    max_rows: int = 1000,
    engine = None
) -> Tuple[int, str, pd.DataFrame]:
    """
    Collecte fichiers GDELT GKG (BigData).
    
    GDELT publie des fichiers toutes les 15 minutes au format :
    http://data.gdeltproject.org/gkg/YYYYMMDDHHMMSS.gkg.csv.zip
    
    Args:
        date_str: Date au format 'YYYYMMDD' (défaut: hier)
        source_name: Nom de la source dans t02_source
        max_rows: Nombre max de lignes à traiter (limite BigData)
        engine: SQLAlchemy engine (optionnel)
        
    Returns:
        Tuple[int, str, DataFrame]: (nb_events, minio_uri, dataframe)
        
    Example:
        >>> collect_gdelt_gkg(date_str='20251120', max_rows=500)
        (500, 's3://datasens-raw/gdelt/gdelt_20251120.csv', df)
    """
    logger.info(f"🌍 Collecte GDELT GKG - BigData")
    
    # Date par défaut : hier (GDELT a 1 jour de retard)
    if date_str is None:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime('%Y%m%d')
    
    # GDELT publie toutes les 15min, on prend le fichier de midi
    gdelt_url = f"http://data.gdeltproject.org/gdeltv2/{date_str}120000.gkg.csv.zip"
    
    try:
        # Télécharger ZIP
        zip_content = _download_gdelt_file(gdelt_url)
        logger.info(f"✅ Téléchargé: {len(zip_content)} bytes")
        
        # Extraire CSV du ZIP
        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            csv_filename = z.namelist()[0]
            with z.open(csv_filename) as f:
                # Parser CSV (attention: très gros fichier, limite à max_rows)
                df = pd.read_csv(
                    f,
                    sep='\t',
                    names=GDELT_GKG_COLUMNS,
                    nrows=max_rows,
                    low_memory=False,
                    on_bad_lines='skip'
                )
        
        logger.info(f"📊 Lignes chargées: {len(df)}")
        
        # Nettoyer et préparer pour insertion
        df_clean = df[['DATE', 'SourceCommonName', 'DocumentIdentifier', 'V2Themes', 'V2Locations', 'V2Tone']].copy()
        df_clean = df_clean.dropna(subset=['DocumentIdentifier'])
        
        # Créer colonnes pour t04_document
        df_clean['titre'] = df_clean['SourceCommonName'].fillna('GDELT Event')
        df_clean['texte'] = df_clean['V2Themes'].fillna('') + ' ' + df_clean['V2Locations'].fillna('')
        df_clean['texte'] = df_clean['texte'].str[:500]  # Limite taille
        df_clean['url'] = df_clean['DocumentIdentifier']
        df_clean['date_publication'] = pd.to_datetime(df_clean['DATE'], format='%Y%m%d%H%M%S', errors='coerce')
        df_clean['langue'] = 'en'
        
        # Hash fingerprint
        df_clean['hash_fingerprint'] = df_clean.apply(
            lambda row: sha256_hash(str(row['DocumentIdentifier'])), 
            axis=1
        )
        
        # Sauvegarder localement
        local_path = RAW_DIR / "gdelt" / f"gdelt_{date_str}_{ts()}.csv"
        local_path.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(local_path, index=False)
        logger.info(f"💾 Sauvegardé: {local_path}")
        
        # Upload MinIO
        try:
            minio_client = MinIOClient()
            minio_uri = minio_client.upload_file(local_path, f"gdelt/{local_path.name}")
            logger.info(f"☁️ MinIO: {minio_uri}")
        except Exception as e:
            logger.warning(f"⚠️ MinIO upload échoué: {e}")
            minio_uri = f"local://{local_path}"
        
        # Insertion PostgreSQL
        if engine is None:
            from ..db import get_engine
            engine = get_engine()
        
        with engine.begin() as conn:
            conn.execute(text("SET search_path TO datasens, public"))
            
            flux_id = _create_flux(conn, source_name, "csv", minio_uri)
            
            # Insertion dans t04_document
            inserted = 0
            cols = ['titre', 'texte', 'langue', 'date_publication', 'hash_fingerprint', 'url']
            
            for _, row in df_clean[cols].iterrows():
                try:
                    result = conn.execute(text("""
                        INSERT INTO datasens.t04_document(
                            id_flux, titre, texte, langue, date_publication, hash_fingerprint
                        )
                        VALUES(:fid, :titre, :texte, :langue, :date, :hash)
                        ON CONFLICT (hash_fingerprint) DO NOTHING
                        RETURNING id_document
                    """), {
                        "fid": flux_id,
                        "titre": row['titre'][:200],
                        "texte": row['texte'],
                        "langue": row['langue'],
                        "date": row['date_publication'],
                        "hash": row['hash_fingerprint']
                    })
                    if result.fetchone():
                        inserted += 1
                except Exception as e:
                    logger.debug(f"⚠️ Skip: {e}")
                    continue
        
        logger.info(f"✅ GDELT: {inserted} événements insérés")
        return inserted, minio_uri, df_clean
        
    except Exception as e:
        logger.error(f"❌ Erreur GDELT: {str(e)}")
        return 0, "", pd.DataFrame()


def collect_gdelt_last_updates(
    num_files: int = 4,
    max_rows_per_file: int = 250,
    engine = None
) -> Tuple[int, str, pd.DataFrame]:
    """
    Collecte les N derniers fichiers GDELT (toutes les 15min).
    Permet de récupérer l'actualité récente.
    
    Args:
        num_files: Nombre de fichiers à télécharger
        max_rows_per_file: Lignes max par fichier
        engine: SQLAlchemy engine
        
    Returns:
        Tuple[int, str, DataFrame]: (total_inserted, minio_uri, dataframe)
    """
    logger.info(f"🌍 Collecte GDELT: {num_files} derniers fichiers")
    
    # Générer URLs des dernières heures
    now = datetime.now()
    urls = []
    
    for i in range(num_files):
        time_offset = timedelta(minutes=15 * i)
        target_time = now - time_offset
        
        # GDELT format: YYYYMMDDHHMMSS (arrondi 15min)
        minute = (target_time.minute // 15) * 15
        timestamp = target_time.replace(minute=minute, second=0, microsecond=0)
        date_str = timestamp.strftime('%Y%m%d%H%M%S')
        
        urls.append(f"http://data.gdeltproject.org/gdeltv2/{date_str}.gkg.csv.zip")
    
    all_data = []
    total_inserted = 0
    
    for url in urls:
        try:
            # Télécharger et parser
            zip_content = _download_gdelt_file(url)
            
            with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
                csv_filename = z.namelist()[0]
                with z.open(csv_filename) as f:
                    df = pd.read_csv(
                        f, sep='\t', names=GDELT_GKG_COLUMNS,
                        nrows=max_rows_per_file, low_memory=False,
                        on_bad_lines='skip'
                    )
            
            all_data.append(df)
            logger.info(f"✅ {url.split('/')[-1]}: {len(df)} lignes")
            
        except Exception as e:
            logger.warning(f"⚠️ Skip {url}: {str(e)[:100]}")
            continue
    
    if not all_data:
        logger.warning("⚠️ Aucune donnée GDELT collectée")
        return 0, "", pd.DataFrame()
    
    # Consolider tous les DataFrames
    df_full = pd.concat(all_data, ignore_index=True)
    logger.info(f"📊 Total consolidé: {len(df_full)} événements")
    
    # Appliquer même traitement que collect_gdelt_gkg
    df_clean = df_full[['DATE', 'SourceCommonName', 'DocumentIdentifier', 'V2Themes', 'V2Locations']].copy()
    df_clean = df_clean.dropna(subset=['DocumentIdentifier'])
    
    df_clean['titre'] = df_clean['SourceCommonName'].fillna('GDELT Event')
    df_clean['texte'] = df_clean['V2Themes'].fillna('') + ' ' + df_clean['V2Locations'].fillna('')
    df_clean['texte'] = df_clean['texte'].str[:500]
    df_clean['date_publication'] = pd.to_datetime(df_clean['DATE'], format='%Y%m%d%H%M%S', errors='coerce')
    df_clean['langue'] = 'en'
    df_clean['hash_fingerprint'] = df_clean.apply(
        lambda row: sha256_hash(str(row['DocumentIdentifier'])), axis=1
    )
    
    # Sauvegarde + MinIO + PostgreSQL (même logique)
    local_path = RAW_DIR / "gdelt" / f"gdelt_updates_{ts()}.csv"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(local_path, index=False)
    
    try:
        minio_client = MinIOClient()
        minio_uri = minio_client.upload_file(local_path, f"gdelt/{local_path.name}")
    except:
        minio_uri = f"local://{local_path}"
    
    if engine is None:
        from ..db import get_engine
        engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("SET search_path TO datasens, public"))
        flux_id = _create_flux(conn, "GDELT Updates", "csv", minio_uri)
        
        inserted = 0
        for _, row in df_clean[['titre', 'texte', 'langue', 'date_publication', 'hash_fingerprint']].iterrows():
            try:
                result = conn.execute(text("""
                    INSERT INTO datasens.t04_document(id_flux, titre, texte, langue, date_publication, hash_fingerprint)
                    VALUES(:fid, :titre, :texte, :langue, :date, :hash)
                    ON CONFLICT (hash_fingerprint) DO NOTHING
                    RETURNING id_document
                """), {
                    "fid": flux_id, "titre": row['titre'][:200], "texte": row['texte'],
                    "langue": row['langue'], "date": row['date_publication'], "hash": row['hash_fingerprint']
                })
                if result.fetchone():
                    inserted += 1
            except:
                continue
    
    logger.info(f"✅ GDELT Updates: {inserted} événements insérés")
    return inserted, minio_uri, df_clean
