"""
Gestion de la base de données PostgreSQL
SQLAlchemy wrapper et fonctions utilitaires
"""

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.pool import QueuePool
from typing import Optional, Any, Dict, List
import pandas as pd
import logging

from .config import get_db_url

logger = logging.getLogger(__name__)


def get_engine(poolclass=QueuePool, pool_size: int = 5, max_overflow: int = 10) -> Engine:
    """
    Crée un moteur SQLAlchemy connecté à PostgreSQL avec connection pooling optimisé.
    
    Args:
        poolclass: Classe de pooling SQLAlchemy (défaut: QueuePool pour performance)
        pool_size: Nombre de connexions permanentes dans le pool
        max_overflow: Nombre max de connexions supplémentaires temporaires
        
    Returns:
        Engine: Moteur SQLAlchemy avec connection pool
        
    Note:
        QueuePool maintient des connexions ouvertes pour réduire la latence.
        pool_size=5 + max_overflow=10 = 15 connexions max simultanées.
    """
    db_url = get_db_url()
    engine = create_engine(
        db_url, 
        poolclass=poolclass,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,  # Vérifie connexion avant utilisation
        pool_recycle=3600,   # Recycle connexions après 1h
        echo=False
    )
    logger.debug(f"🔌 Moteur DB créé avec pool: {pool_size}+{max_overflow} connexions")
    return engine


def execute_query(query: str, params: Optional[Dict[str, Any]] = None, engine: Optional[Engine] = None) -> Any:
    """
    Exécute une requête SQL et retourne le résultat.
    
    Args:
        query: Requête SQL à exécuter
        params: Paramètres de la requête (optionnel)
        engine: Moteur SQLAlchemy (crée un nouveau si None)
        
    Returns:
        Any: Résultat de la requête (fetchall, lastrowid, etc.)
    """
    if engine is None:
        engine = get_engine()
    
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        conn.commit()
        
        # Retourne selon le type de requête
        if query.strip().upper().startswith('SELECT'):
            return result.fetchall()
        elif query.strip().upper().startswith('INSERT') and 'RETURNING' in query.upper():
            return result.fetchone()
        else:
            return result.rowcount


def insert_documents(
    df: pd.DataFrame,
    source_id: int,
    flux_id: int,
    territoire_complet: str = "FR:NAT:FRANCE",
    engine: Optional[Engine] = None
) -> int:
    """
    Insère des documents dans t04_document depuis un DataFrame.
    
    Args:
        df: DataFrame avec colonnes: titre, contenu, date_publication, url, hash_contenu
        source_id: ID de la source (t01_source.id_source)
        flux_id: ID du flux (t02_flux.id_flux)
        territoire_complet: Code territoire (défaut: France nationale)
        engine: Moteur SQLAlchemy (optionnel)
        
    Returns:
        int: Nombre de documents insérés
    """
    if engine is None:
        engine = get_engine()
    
    inserted_count = 0
    
    with engine.connect() as conn:
        for _, row in df.iterrows():
            try:
                query = text("""
                    INSERT INTO datasens.t04_document (
                        id_source, id_flux, titre, contenu, date_publication, url_source, 
                        hash_contenu, territoire_complet, created_at
                    ) VALUES (
                        :source_id, :flux_id, :titre, :contenu, :date_publication, :url, 
                        :hash_contenu, :territoire_complet, NOW()
                    )
                    ON CONFLICT (hash_contenu) DO NOTHING
                    RETURNING id_document
                """)
                
                result = conn.execute(query, {
                    'source_id': source_id,
                    'flux_id': flux_id,
                    'titre': row['titre'],
                    'contenu': row['contenu'],
                    'date_publication': row['date_publication'],
                    'url': row['url'],
                    'hash_contenu': row['hash_contenu'],
                    'territoire_complet': territoire_complet
                })
                
                if result.fetchone():
                    inserted_count += 1
                    
            except Exception as e:
                logger.warning(f"⚠️ Erreur insertion document '{row.get('titre', 'N/A')}': {e}")
                continue
        
        conn.commit()
    
    logger.info(f"✅ {inserted_count}/{len(df)} documents insérés")
    return inserted_count


def get_source_id(nom_source: str, engine: Optional[Engine] = None) -> Optional[int]:
    """
    Récupère l'ID d'une source par son nom.
    
    Args:
        nom_source: Nom de la source (ex: "Kaggle CSV", "OpenWeatherMap")
        engine: Moteur SQLAlchemy (optionnel)
        
    Returns:
        Optional[int]: ID de la source ou None si non trouvée
    """
    if engine is None:
        engine = get_engine()
    
    query = text("SELECT id_source FROM datasens.t01_source WHERE nom_source = :nom_source")
    
    with engine.connect() as conn:
        result = conn.execute(query, {'nom_source': nom_source})
        row = result.fetchone()
        return row[0] if row else None


def create_flux(
    nom_flux: str,
    url_flux: str,
    source_id: int,
    actif: bool = True,
    engine: Optional[Engine] = None
) -> int:
    """
    Crée un nouveau flux dans t02_flux.
    
    Args:
        nom_flux: Nom du flux
        url_flux: URL du flux
        source_id: ID de la source parente
        actif: Flux actif ou non
        engine: Moteur SQLAlchemy (optionnel)
        
    Returns:
        int: ID du flux créé
    """
    if engine is None:
        engine = get_engine()
    
    query = text("""
        INSERT INTO datasens.t02_flux (nom_flux, url_flux, id_source, actif, created_at)
        VALUES (:nom_flux, :url_flux, :source_id, :actif, NOW())
        ON CONFLICT (url_flux) DO UPDATE SET actif = :actif
        RETURNING id_flux
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {
            'nom_flux': nom_flux,
            'url_flux': url_flux,
            'source_id': source_id,
            'actif': actif
        })
        conn.commit()
        flux_id = result.fetchone()[0]
    
    logger.info(f"✅ Flux créé/mis à jour: {nom_flux} (id={flux_id})")
    return flux_id


def get_table_count(table_name: str, schema: str = "datasens", engine: Optional[Engine] = None) -> int:
    """
    Compte le nombre de lignes dans une table.
    
    Args:
        table_name: Nom de la table
        schema: Schéma de la table (défaut: datasens)
        engine: Moteur SQLAlchemy (optionnel)
        
    Returns:
        int: Nombre de lignes
    """
    if engine is None:
        engine = get_engine()
    
    query = text(f"SELECT COUNT(*) FROM {schema}.{table_name}")
    
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]
