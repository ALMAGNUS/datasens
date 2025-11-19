"""
Test Comparatif spaCy vs YAKE - Annotation Dataset Français
Date : 2025-11-19
Objectif : Comparer performance et qualité d'annotation entre spaCy et YAKE
"""

import pandas as pd
import spacy
import yake
from pathlib import Path
import json
from datetime import datetime
from typing import List, Dict, Tuple
import time

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "dataset"
RESULTS_DIR = PROJECT_ROOT / "docs" / "tests_comparatifs"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Charger modèle spaCy français
print("[INFO] Chargement modele spaCy francais...")
try:
    nlp = spacy.load("fr_core_news_sm")
    print("[OK] Modele spaCy charge : fr_core_news_sm")
except OSError:
    print("[ERROR] Modele spaCy non trouve. Installez avec : python -m spacy download fr_core_news_sm")
    nlp = None

# Initialiser YAKE
print("[INFO] Initialisation YAKE...")
kw_extractor = yake.KeywordExtractor(
    lan="fr",
    n=3,  # N-grammes max
    dedupLim=0.7,  # Seuil déduplication
    top=10,  # Top 10 mots-clés
    features=None
)
print("[OK] YAKE initialise")

def annotate_spacy(text: str) -> Dict:
    """Annotation avec spaCy : NER, tokens, lemmes"""
    if nlp is None:
        return {"error": "spaCy non disponible"}
    
    doc = nlp(text)
    
    # Entités nommées (NER)
    entities = [
        {
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        }
        for ent in doc.ents
    ]
    
    # Tokens et lemmes
    tokens = [token.text for token in doc]
    lemmes = [token.lemma_ for token in doc]
    
    # Statistiques
    stats = {
        "nb_tokens": len(tokens),
        "nb_entities": len(entities),
        "nb_sentences": len(list(doc.sents))
    }
    
    return {
        "entities": entities,
        "tokens": tokens,
        "lemmes": lemmes,
        "stats": stats
    }

def annotate_yake(text: str) -> Dict:
    """Annotation avec YAKE : Extraction mots-clés"""
    try:
        keywords = kw_extractor.extract_keywords(text)
        
        # Formater résultats
        keywords_formatted = []
        for kw in keywords:
            if len(kw) >= 2:
                try:
                    score = float(kw[0]) if isinstance(kw[0], (int, float)) else 0.0
                    keyword_text = str(kw[1]) if len(kw) > 1 else ""
                    keywords_formatted.append({
                        "keyword": keyword_text,
                        "score": score  # Score YAKE (plus bas = meilleur)
                    })
                except (ValueError, IndexError):
                    continue
        
        return {
            "keywords": keywords_formatted,
            "nb_keywords": len(keywords_formatted)
        }
    except Exception as e:
        return {"error": str(e)}

def test_comparatif(dataset_path: Path, nb_samples: int = 10) -> Dict:
    """Test comparatif sur échantillon du dataset"""
    print(f"\n[INFO] Chargement dataset : {dataset_path}")
    
    # Charger dataset
    if dataset_path.suffix == '.csv':
        df = pd.read_csv(dataset_path, nrows=nb_samples)
    elif dataset_path.suffix == '.parquet':
        df = pd.read_parquet(dataset_path)
        df = df.head(nb_samples)
    else:
        raise ValueError(f"Format non supporte : {dataset_path.suffix}")
    
    print(f"[OK] {len(df)} echantillons charges")
    
    # Colonne texte (adapter selon dataset)
    text_column = None
    for col in ['texte_nettoye', 'texte', 'contenu', 'text']:
        if col in df.columns:
            text_column = col
            break
    
    if text_column is None:
        raise ValueError("Colonne texte non trouvee dans le dataset")
    
    print(f"[INFO] Colonne texte utilisee : {text_column}")
    
    # Résultats
    results = {
        "dataset": str(dataset_path.name),
        "nb_samples": len(df),
        "timestamp": datetime.now().isoformat(),
        "samples": []
    }
    
    # Métriques globales
    spacy_times = []
    yake_times = []
    spacy_entities_total = 0
    yake_keywords_total = 0
    
    # Traiter chaque échantillon
    for idx, row in df.iterrows():
        text = str(row[text_column])
        if pd.isna(text) or len(text) < 10:
            continue
        
        sample_result = {
            "id": idx,
            "text_length": len(text),
            "text_preview": text[:100] + "..." if len(text) > 100 else text
        }
        
        # Test spaCy
        start = time.time()
        spacy_result = annotate_spacy(text)
        spacy_time = time.time() - start
        spacy_times.append(spacy_time)
        
        if "error" not in spacy_result:
            spacy_entities_total += spacy_result["stats"]["nb_entities"]
            sample_result["spacy"] = {
                "time_ms": round(spacy_time * 1000, 2),
                "entities": spacy_result["entities"][:5],  # Top 5
                "nb_entities": spacy_result["stats"]["nb_entities"],
                "nb_tokens": spacy_result["stats"]["nb_tokens"]
            }
        else:
            sample_result["spacy"] = {"error": spacy_result["error"]}
        
        # Test YAKE
        start = time.time()
        yake_result = annotate_yake(text)
        yake_time = time.time() - start
        yake_times.append(yake_time)
        
        if "error" not in yake_result:
            yake_keywords_total += yake_result["nb_keywords"]
            sample_result["yake"] = {
                "time_ms": round(yake_time * 1000, 2),
                "keywords": yake_result["keywords"],
                "nb_keywords": yake_result["nb_keywords"]
            }
        else:
            sample_result["yake"] = {"error": yake_result["error"]}
        
        results["samples"].append(sample_result)
        
        if (idx + 1) % 5 == 0:
            print(f"  [OK] Traite {idx + 1}/{len(df)} echantillons")
    
    # Métriques globales
    results["metrics"] = {
        "spacy": {
            "avg_time_ms": round(sum(spacy_times) / len(spacy_times) * 1000, 2) if spacy_times else 0,
            "total_entities": spacy_entities_total,
            "avg_entities_per_sample": round(spacy_entities_total / len(results["samples"]), 2) if results["samples"] else 0
        },
        "yake": {
            "avg_time_ms": round(sum(yake_times) / len(yake_times) * 1000, 2) if yake_times else 0,
            "total_keywords": yake_keywords_total,
            "avg_keywords_per_sample": round(yake_keywords_total / len(results["samples"]), 2) if results["samples"] else 0
        }
    }
    
    return results

def generate_report(results: Dict) -> str:
    """Générer rapport markdown"""
    report = f"""# Rapport Comparatif spaCy vs YAKE

**Date** : {results['timestamp']}  
**Dataset** : {results['dataset']}  
**Échantillons testés** : {results['nb_samples']}

---

## 📊 Métriques Globales

### spaCy

- **Temps moyen** : {results['metrics']['spacy']['avg_time_ms']} ms
- **Entités totales détectées** : {results['metrics']['spacy']['total_entities']}
- **Moyenne entités/échantillon** : {results['metrics']['spacy']['avg_entities_per_sample']}

### YAKE

- **Temps moyen** : {results['metrics']['yake']['avg_time_ms']} ms
- **Mots-clés totaux extraits** : {results['metrics']['yake']['total_keywords']}
- **Moyenne mots-clés/échantillon** : {results['metrics']['yake']['avg_keywords_per_sample']}

---

## 🎯 Comparaison

| Critère | spaCy | YAKE | Gagnant |
|---------|-------|------|---------|
| **Performance** | {results['metrics']['spacy']['avg_time_ms']} ms | {results['metrics']['yake']['avg_time_ms']} ms | {'spaCy' if results['metrics']['spacy']['avg_time_ms'] < results['metrics']['yake']['avg_time_ms'] else 'YAKE'} |
| **Détection entités** | ✅ Oui (NER) | ❌ Non | **spaCy** |
| **Extraction mots-clés** | ❌ Non | ✅ Oui | **YAKE** |
| **Modèle pré-entraîné** | ✅ Oui (fr_core_news_sm) | ❌ Non (non supervisé) | **spaCy** |
| **Multilingue** | ✅ Oui | ✅ Oui | **Égalité** |

---

## 💡 Conclusion

### spaCy : Optimal pour NER (Entités Nommées)

- ✅ Détection entités (personnes, lieux, organisations)
- ✅ Tokenisation et lemmatisation
- ✅ Modèle français pré-entraîné
- ❌ Pas d'extraction mots-clés native

### YAKE : Optimal pour Extraction Mots-clés

- ✅ Extraction mots-clés non supervisée
- ✅ Léger et rapide
- ✅ Multilingue (français)
- ❌ Pas de NER

### Recommandation pour E2/E3

**Utiliser les deux en complémentarité** :
- **spaCy** : Annotation territoriale (NER pour lieux, communes)
- **YAKE** : Extraction mots-clés pour contexte/thèmes

---

## 📋 Détails par Échantillon

"""
    
    for i, sample in enumerate(results['samples'][:5], 1):  # Top 5
        report += f"""
### Échantillon {i}

**Texte** : {sample['text_preview']}  
**Longueur** : {sample['text_length']} caractères

#### spaCy
- **Temps** : {sample.get('spacy', {}).get('time_ms', 'N/A')} ms
- **Entités détectées** : {sample.get('spacy', {}).get('nb_entities', 0)}
- **Top entités** :
"""
        if 'spacy' in sample and 'entities' in sample['spacy']:
            for ent in sample['spacy']['entities'][:3]:
                report += f"  - `{ent['text']}` ({ent['label']})\n"
        
        report += f"""
#### YAKE
- **Temps** : {sample.get('yake', {}).get('time_ms', 'N/A')} ms
- **Mots-clés extraits** : {sample.get('yake', {}).get('nb_keywords', 0)}
- **Top mots-clés** :
"""
        if 'yake' in sample and 'keywords' in sample['yake']:
            for kw in sample['yake']['keywords'][:5]:
                try:
                    score = float(kw.get('score', 0)) if isinstance(kw.get('score'), (int, float)) else 0.0
                    keyword = kw.get('keyword', 'N/A')
                    report += f"  - `{keyword}` (score: {score:.4f})\n"
                except (ValueError, TypeError):
                    report += f"  - `{kw.get('keyword', 'N/A')}` (score: N/A)\n"
    
    return report

def main():
    """Exécuter tests comparatifs"""
    print("=" * 80)
    print("TEST COMPARATIF spaCy vs YAKE")
    print("=" * 80)
    
    # Chercher dataset GOLD
    dataset_files = list(DATA_DIR.glob("datasens_gold_*.csv")) + list(DATA_DIR.glob("datasens_gold_*.parquet"))
    
    if not dataset_files:
        print(f"[ERROR] Aucun dataset GOLD trouve dans {DATA_DIR}")
        return
    
    # Prendre le plus récent
    dataset_path = max(dataset_files, key=lambda p: p.stat().st_mtime)
    print(f"[INFO] Dataset selectionne : {dataset_path.name}")
    
    # Exécuter tests
    results = test_comparatif(dataset_path, nb_samples=10)
    
    # Sauvegarder résultats JSON
    results_json_path = RESULTS_DIR / f"comparatif_spacy_yake_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Resultats JSON sauvegardes : {results_json_path}")
    
    # Générer rapport markdown
    report = generate_report(results)
    report_path = RESULTS_DIR / f"RAPPORT_COMPARATIF_SPACY_YAKE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"[OK] Rapport markdown genere : {report_path}")
    
    # Afficher résumé
    print("\n" + "=" * 80)
    print("RESUME COMPARATIF")
    print("=" * 80)
    print(f"\nspaCy :")
    print(f"  - Temps moyen : {results['metrics']['spacy']['avg_time_ms']} ms")
    print(f"  - Entites detectees : {results['metrics']['spacy']['total_entities']}")
    print(f"\nYAKE :")
    print(f"  - Temps moyen : {results['metrics']['yake']['avg_time_ms']} ms")
    print(f"  - Mots-cles extraits : {results['metrics']['yake']['total_keywords']}")
    print("\n[OK] Tests termines !")

if __name__ == "__main__":
    main()

