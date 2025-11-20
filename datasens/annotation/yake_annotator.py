"""
Annotation YAKE - Extraction de mots-clés
"""

import pandas as pd
import yake
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

# Paramètres YAKE par défaut
DEFAULT_LANGUAGE = "fr"
DEFAULT_MAX_NGRAM_SIZE = 3
DEFAULT_DEDUPLICATION_THRESHOLD = 0.9
DEFAULT_NUM_KEYWORDS = 10


def extract_keywords_yake(text: str, 
                          max_ngrams: int = DEFAULT_MAX_NGRAM_SIZE,
                          num_keywords: int = DEFAULT_NUM_KEYWORDS) -> List[Tuple[str, float]]:
    """
    Extrait mots-clés avec YAKE.
    
    Args:
        text: Texte à analyser
        max_ngrams: Taille max des n-grams (1-3)
        num_keywords: Nombre de mots-clés à retourner
        
    Returns:
        Liste de tuples (mot-clé, score)
    """
    if not text or len(text) < 50:
        return []
    
    try:
        kw_extractor = yake.KeywordExtractor(
            lan=DEFAULT_LANGUAGE,
            n=max_ngrams,
            dedupLim=DEFAULT_DEDUPLICATION_THRESHOLD,
            top=num_keywords,
            features=None
        )
        
        keywords = kw_extractor.extract_keywords(text[:1000000])  # Limite 1M caractères
        return keywords
    
    except Exception as e:
        logger.error(f"❌ YAKE extraction erreur: {e}")
        return []


def annotate_dataframe_yake(df: pd.DataFrame, 
                            text_column: str = "texte",
                            num_keywords: int = 10) -> pd.DataFrame:
    """
    Annote un DataFrame avec YAKE keywords.
    
    Args:
        df: DataFrame avec colonne texte
        text_column: Nom de la colonne texte
        num_keywords: Nombre de mots-clés par document
        
    Returns:
        DataFrame avec colonne yake_keywords ajoutée
    """
    logger.info(f"🔑 Annotation YAKE: {len(df)} documents")
    
    keywords_list = []
    for idx, row in df.iterrows():
        text = row.get(text_column, "")
        keywords = extract_keywords_yake(text, num_keywords=num_keywords)
        
        # Garder seulement les mots-clés (pas les scores)
        kw_strings = [kw[0] for kw in keywords]
        keywords_list.append(",".join(kw_strings))
    
    df["yake_keywords"] = keywords_list
    
    logger.info(f"✅ YAKE annotation terminée")
    return df
