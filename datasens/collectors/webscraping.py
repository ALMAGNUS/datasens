"""
Collecteur Web Scraping Multi-Sources
Reddit, YouTube, data.gouv.fr, SignalConso, vie-publique.fr
"""

import pandas as pd
import requests
import os
from typing import List, Tuple, Optional, Dict
import logging
from sqlalchemy import text

from ..config import RAW_DIR
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


def _create_flux(conn, source_nom: str, format_type: str = "html", manifest_uri: str = None) -> int:
    """Crée un flux dans t03_flux"""
    sid = _get_source_id(conn, source_nom)
    if not sid:
        tid_result = conn.execute(text("SELECT id_type_donnee FROM datasens.t01_type_donnee WHERE libelle = 'web_scraping' LIMIT 1"))
        tid_row = tid_result.fetchone()
        tid = tid_row[0] if tid_row else 1
        
        sid_result = conn.execute(text("""
            INSERT INTO datasens.t02_source(id_type_donnee, nom, url, fiabilite) 
            VALUES (:tid, :nom, '', 0.6) RETURNING id_source
        """), {"tid": tid, "nom": source_nom})
        sid = sid_result.fetchone()[0]
    
    flux_result = conn.execute(text("""
        INSERT INTO datasens.t03_flux(id_source, format, manifest_uri, date_collecte)
        VALUES (:sid, :format, :manifest, NOW()) RETURNING id_flux
    """), {"sid": sid, "format": format_type, "manifest": manifest_uri})
    return flux_result.fetchone()[0]


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


def collect_reddit_data(client_id: str, client_secret: str, subreddits: List[str] = None, limit: int = 25) -> List[Dict]:
    """Collecte Reddit via API PRAW"""
    if subreddits is None:
        subreddits = ["france", "Paris"]
    
    data = []
    try:
        import praw
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="DataSensBot/1.0"
        )
        for subreddit_name in subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.hot(limit=limit):
                data.append({
                    "titre": post.title,
                    "texte": post.selftext or post.title,
                    "source_site": "reddit.com",
                    "url": f"https://reddit.com{post.permalink}",
                    "date_publication": pd.to_datetime(post.created_utc, unit='s'),
                    "langue": "fr"
                })
        logger.info(f"✅ Reddit: {len(data)} posts")
    except Exception as e:
        logger.error(f"❌ Reddit: {str(e)[:80]}")
    return data


def collect_youtube_data(api_key: str, video_ids: List[str] = None, max_comments: int = 30) -> List[Dict]:
    """Collecte YouTube commentaires via API"""
    if video_ids is None:
        return []
    
    data = []
    try:
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        for video_id in video_ids:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_comments
            )
            response = request.execute()
            
            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                data.append({
                    "titre": f"Commentaire YouTube - {video_id}",
                    "texte": snippet.get("textDisplay", ""),
                    "source_site": "youtube.com",
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "date_publication": pd.to_datetime(snippet.get("publishedAt", "")),
                    "langue": "fr"
                })
        logger.info(f"✅ YouTube: {len(data)} commentaires")
    except Exception as e:
        logger.error(f"❌ YouTube: {str(e)[:80]}")
    return data


def collect_datagouv() -> List[Dict]:
    """Collecte data.gouv.fr datasets via API"""
    data = []
    try:
        url = "https://www.data.gouv.fr/api/1/datasets/"
        params = {"q": "france", "page_size": 30}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        
        for dataset in json_data.get("data", []):
            data.append({
                "titre": dataset.get("title", ""),
                "texte": dataset.get("description", dataset.get("title", "")),
                "source_site": "data.gouv.fr",
                "url": f"https://www.data.gouv.fr/fr/datasets/{dataset.get('slug', '')}",
                "date_publication": pd.to_datetime(dataset.get("created_at", ""), errors="coerce"),
                "langue": "fr"
            })
        logger.info(f"✅ data.gouv.fr: {len(data)} datasets")
    except Exception as e:
        logger.error(f"❌ data.gouv.fr: {str(e)[:80]}")
    return data


def collect_viepublique() -> List[Dict]:
    """Collecte vie-publique.fr via RSS"""
    data = []
    try:
        import feedparser
        feed = feedparser.parse("https://www.vie-publique.fr/rss.xml")
        for entry in feed.entries[:30]:
            data.append({
                "titre": entry.get("title", ""),
                "texte": entry.get("summary", entry.get("title", "")),
                "source_site": "vie-publique.fr",
                "url": entry.get("link", ""),
                "date_publication": pd.to_datetime(entry.get("published", ""), errors="coerce"),
                "langue": "fr"
            })
        logger.info(f"✅ vie-publique.fr: {len(data)} articles")
    except Exception as e:
        logger.error(f"❌ vie-publique.fr: {str(e)[:80]}")
    return data


def collect_webscraping_multisources(
    reddit_creds: Dict[str, str] = None,
    youtube_creds: Dict[str, str] = None,
    source_name: str = "Web Scraping Multi-Sources",
    engine = None
) -> Tuple[int, str, pd.DataFrame]:
    """
    Collecte depuis 6 sources web.
    
    Args:
        reddit_creds: {"client_id": ..., "client_secret": ...}
        youtube_creds: {"api_key": ..., "video_ids": [...]}
        source_name: Nom de la source dans t02_source
        engine: SQLAlchemy engine (optionnel)
        
    Returns:
        Tuple[int, str, DataFrame]: (nb_insérés, minio_uri, dataframe)
    """
    logger.info("🌐 Collecte Web Scraping Multi-Sources")
    
    all_data = []
    
    # 1. Reddit
    if reddit_creds:
        all_data.extend(collect_reddit_data(
            reddit_creds.get("client_id"), 
            reddit_creds.get("client_secret")
        ))
    
    # 2. YouTube
    if youtube_creds:
        all_data.extend(collect_youtube_data(
            youtube_creds.get("api_key"),
            youtube_creds.get("video_ids", [])
        ))
    
    # 3. data.gouv.fr
    all_data.extend(collect_datagouv())
    
    # 4. vie-publique.fr
    all_data.extend(collect_viepublique())
    
    if len(all_data) == 0:
        logger.warning("⚠️ Aucune donnée Web Scraping collectée")
        return 0, "", pd.DataFrame()
    
    # Créer DataFrame et nettoyer
    df = pd.DataFrame(all_data)
    df = df[df["texte"].str.len() > 20].copy()
    
    # Hash et déduplication
    df["hash_fingerprint"] = df.apply(
        lambda row: sha256_hash(row["titre"] + " " + row["texte"]), 
        axis=1
    )
    df = df.drop_duplicates(subset=["hash_fingerprint"])
    
    logger.info(f"📊 Total: {len(df)} documents collectés")
    
    # Sauvegarde locale
    local_path = RAW_DIR / "scraping" / "multi" / f"scraping_multi_{ts()}.csv"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(local_path, index=False)
    
    # Upload MinIO
    try:
        minio_client = MinIOClient()
        minio_uri = minio_client.upload_file(local_path, f"scraping/multi/{local_path.name}")
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
        
        flux_id = _create_flux(conn, source_name, "html", minio_uri)
        
        cols_needed = ['titre', 'texte', 'langue', 'date_publication', 'hash_fingerprint']
        df_insert = df[cols_needed]
        nb_inserted = _insert_documents(conn, df_insert, flux_id)
    
    logger.info(f"✅ Web Scraping: {nb_inserted} documents insérés")
    return nb_inserted, minio_uri, df
