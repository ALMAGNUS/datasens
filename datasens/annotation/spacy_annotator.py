"""
Annotation SpaCy - NER et POS tagging
"""

import pandas as pd
import spacy
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

# Modèle français SpaCy
NLP_MODEL = "fr_core_news_md"


def load_spacy_model():
    """Charge le modèle SpaCy français"""
    try:
        nlp = spacy.load(NLP_MODEL)
        logger.info(f"✅ SpaCy modèle chargé: {NLP_MODEL}")
        return nlp
    except OSError:
        logger.error(f"❌ Modèle {NLP_MODEL} non trouvé. Installez avec: python -m spacy download {NLP_MODEL}")
        return None


def extract_entities(text: str, nlp) -> Dict[str, List[str]]:
    """
    Extrait entités nommées (NER).
    
    Args:
        text: Texte à analyser
        nlp: Modèle SpaCy
        
    Returns:
        Dict avec entités par type (PER, LOC, ORG, MISC)
    """
    if not nlp or not text:
        return {}
    
    doc = nlp(text[:1000000])  # Limite 1M caractères
    
    entities = {
        "PER": [],  # Personnes
        "LOC": [],  # Lieux
        "ORG": [],  # Organisations
        "MISC": []  # Divers
    }
    
    for ent in doc.ents:
        if ent.label_ == "PER":
            entities["PER"].append(ent.text)
        elif ent.label_ in ["LOC", "GPE"]:
            entities["LOC"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["ORG"].append(ent.text)
        else:
            entities["MISC"].append(ent.text)
    
    # Dédupliquer
    for key in entities:
        entities[key] = list(set(entities[key]))
    
    return entities


def annotate_dataframe_spacy(df: pd.DataFrame, text_column: str = "texte") -> pd.DataFrame:
    """
    Annote un DataFrame avec SpaCy NER.
    
    Args:
        df: DataFrame avec colonne texte
        text_column: Nom de la colonne texte
        
    Returns:
        DataFrame avec colonnes NER ajoutées
    """
    logger.info(f"🔍 Annotation SpaCy: {len(df)} documents")
    
    nlp = load_spacy_model()
    if not nlp:
        return df
    
    # Extraire entités
    entities_list = []
    for idx, row in df.iterrows():
        text = row.get(text_column, "")
        entities = extract_entities(text, nlp)
        entities_list.append(entities)
    
    # Ajouter colonnes
    df["spacy_persons"] = [",".join(e["PER"][:5]) for e in entities_list]  # Top 5
    df["spacy_locations"] = [",".join(e["LOC"][:5]) for e in entities_list]
    df["spacy_organizations"] = [",".join(e["ORG"][:5]) for e in entities_list]
    
    logger.info(f"✅ SpaCy annotation terminée")
    return df
