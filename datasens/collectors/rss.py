"""
Collecteur Flux RSS
Ingestion multi-sources de flux RSS
"""

import pandas as pd
import feedparser
import time
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging
from sqlalchemy import text

from ..config import RAW_DIR
from ..storage import MinIOClient
from ..utils import sha256_hash, ts
from ..retry import retry_on_network_error

logger = logging.getLogger(__name__)


def _get_source_id(conn, nom: str) -> Optional[int]:
    """Récupère l'ID d'une source depuis t02_source"""
    result = conn.execute(
        text("SELECT id_source FROM datasens.t02_source WHERE nom = :nom"), 
        {"nom": nom}
    ).scalar()
    return result


def _create_flux(conn, source_nom: str, format_type: str = "rss", manifest_uri: str = None) -> int:
    """Crée un flux dans t03_flux"""
    sid = _get_source_id(conn, source_nom)
    if not sid:
        # Créer la source si elle n'existe pas
        tid = conn.execute(text("SELECT id_type_donnee FROM datasens.t01_type_donnee WHERE libelle = 'rss_feed' LIMIT 1")).scalar()
        if not tid:
            tid = 1  # Fallback
        sid = conn.execute(text("""
            INSERT INTO datasens.t02_source(id_type_donnee, nom, url, fiabilite) 
            VALUES (:tid, :nom, '', 0.7) RETURNING id_source
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


def collect_rss_feeds(
    rss_sources: Dict[str, str],
    source_name: str = "Flux RSS Multi-Sources",
    max_items_per_source: int = 30,
    sleep_between_sources: float = 1.0,
    engine = None
) -> Tuple[int, int, str, pd.DataFrame]:
    """
    Collecte des articles depuis plusieurs flux RSS.
    
    Args:
        rss_sources: Dict avec {nom_source: url_rss}
        source_name: Nom de la source dans t02_source
        max_items_per_source: Nombre max d'articles par source
        sleep_between_sources: Pause entre sources (en secondes)
        engine: SQLAlchemy engine (optionnel)
        
    Returns:
        Tuple[int, int, str, DataFrame]: (nb_brut, nb_insérés, minio_uri, dataframe)
    """
    logger.info(f"📰 Collecte RSS: {len(rss_sources)} sources")
    
    all_items = []
    
    @retry_on_network_error(max_retries=3)
    def parse_feed(url: str) -> feedparser.FeedParserDict:
        """Parse RSS feed avec retry automatique"""
        return feedparser.parse(url)
    
    for src_name, rss_url in rss_sources.items():
        logger.info(f"📡 Source: {src_name}")
        try:
            feed = parse_feed(rss_url)
            if len(feed.entries) == 0:
                logger.warning(f"⚠️ Aucun article pour {src_name}")
                continue
            
            source_items = []
            for entry in feed.entries[:max_items_per_source]:
                titre = entry.get("title", "").strip()
                texte = (entry.get("summary", "") or entry.get("description", "") or "").strip()
                if titre and texte:
                    source_items.append({
                        "titre": titre,
                        "texte": texte,
                        "date_publication": pd.to_datetime(entry.get("published", ""), errors="coerce"),
                        "langue": "fr",
                        "source_media": src_name,
                        "url": entry.get("link", "")
                    })
            
            all_items.extend(source_items)
            logger.info(f"✅ {len(source_items)} articles collectés")
            
        except Exception as e:
            logger.error(f"❌ Erreur {src_name}: {str(e)[:80]}")
        
        time.sleep(sleep_between_sources)
    
    if len(all_items) == 0:
        logger.warning("⚠️ Aucun article RSS collecté")
        return 0, 0, "", pd.DataFrame()
    
    # Créer DataFrame et dédupliquer
    df = pd.DataFrame(all_items)
    logger.info(f"📊 Total brut: {len(df)} articles")
    
    # Hash et déduplication
    df["hash_fingerprint"] = df.apply(
        lambda row: sha256_hash(row["titre"] + " " + row["texte"]), 
        axis=1
    )
    nb_avant = len(df)
    df = df.drop_duplicates(subset=["hash_fingerprint"])
    nb_apres = len(df)
    logger.info(f"🧹 Déduplication: {nb_avant} → {nb_apres} articles uniques")
    
    # Sauvegarde locale
    local_path = RAW_DIR / "rss" / f"rss_multi_{ts()}.csv"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(local_path, index=False)
    
    # Upload MinIO
    try:
        minio_client = MinIOClient()
        minio_uri = minio_client.upload_file(local_path, f"rss/{local_path.name}")
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
        
        # Créer flux
        flux_id = _create_flux(conn, source_name, "rss", minio_uri)
        
        # Insérer documents
        cols_needed = ['titre', 'texte', 'langue', 'date_publication', 'hash_fingerprint']
        df_insert = df[cols_needed]
        nb_inserted = _insert_documents(conn, df_insert, flux_id)
    
    logger.info(f"✅ RSS: {nb_inserted} articles insérés + MinIO")
    return nb_avant, nb_inserted, minio_uri, df
