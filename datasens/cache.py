"""
Cache simple pour éviter la re-collecte de données
Basé sur hash_fingerprint pour détecter les doublons avant insertion
"""

import logging
from typing import Set, Optional
from sqlalchemy import text, Engine

logger = logging.getLogger(__name__)


class DuplicateCache:
    """
    Cache en mémoire des hash_fingerprint déjà insérés.
    Permet de skip les doublons avant insertion SQL (plus rapide).
    """
    
    def __init__(self, engine: Engine = None):
        """
        Initialise le cache avec les hash existants en DB.
        
        Args:
            engine: SQLAlchemy engine pour charger hashes existants
        """
        self._cache: Set[str] = set()
        self._engine = engine
        self._loaded = False
        
    def load_existing_hashes(self, limit: int = 10000) -> int:
        """
        Charge les N derniers hash_fingerprint depuis t04_document.
        
        Args:
            limit: Nombre de hash à charger (défaut 10k plus récents)
            
        Returns:
            int: Nombre de hash chargés
        """
        if self._loaded:
            logger.debug("⚡ Cache déjà chargé, skip")
            return len(self._cache)
            
        if self._engine is None:
            from .db import get_engine
            self._engine = get_engine()
        
        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(f"""
                    SELECT hash_fingerprint 
                    FROM datasens.t04_document 
                    WHERE hash_fingerprint IS NOT NULL
                    ORDER BY id_doc DESC
                    LIMIT {limit}
                """))
                
                for row in result:
                    if row[0]:
                        self._cache.add(row[0])
                
                self._loaded = True
                logger.info(f"⚡ Cache chargé: {len(self._cache)} hash")
                return len(self._cache)
                
        except Exception as e:
            logger.warning(f"⚠️ Erreur chargement cache: {e}")
            return 0
    
    def is_duplicate(self, hash_fingerprint: str) -> bool:
        """
        Vérifie si un hash est déjà dans le cache.
        
        Args:
            hash_fingerprint: Hash à vérifier
            
        Returns:
            bool: True si doublon détecté
        """
        if not self._loaded:
            self.load_existing_hashes()
        
        return hash_fingerprint in self._cache
    
    def add(self, hash_fingerprint: str):
        """Ajoute un hash au cache après insertion réussie"""
        self._cache.add(hash_fingerprint)
    
    def size(self) -> int:
        """Retourne la taille actuelle du cache"""
        return len(self._cache)
    
    def clear(self):
        """Vide le cache"""
        self._cache.clear()
        self._loaded = False


# Instance globale pour partager entre collectors
_global_cache: Optional[DuplicateCache] = None


def get_duplicate_cache(engine: Engine = None) -> DuplicateCache:
    """
    Retourne l'instance globale du cache de doublons.
    Lazy initialization lors du premier appel.
    
    Args:
        engine: SQLAlchemy engine (optionnel)
        
    Returns:
        DuplicateCache: Instance du cache
    """
    global _global_cache
    
    if _global_cache is None:
        _global_cache = DuplicateCache(engine)
        _global_cache.load_existing_hashes()
    
    return _global_cache
