# Rapport Comparatif spaCy vs YAKE

**Date** : 2025-11-19T01:12:09.950145  
**Dataset** : datasens_gold_20251118T222736Z_ai_ready_20251118T235819Z.parquet  
**Échantillons testés** : 10

---

## 📊 Métriques Globales

### spaCy

- **Temps moyen** : 22.0 ms
- **Entités totales détectées** : 17
- **Moyenne entités/échantillon** : 1.7

### YAKE

- **Temps moyen** : 28.79 ms
- **Mots-clés totaux extraits** : 74
- **Moyenne mots-clés/échantillon** : 7.4

---

## 🎯 Comparaison

| Critère | spaCy | YAKE | Gagnant |
|---------|-------|------|---------|
| **Performance** | 22.0 ms | 28.79 ms | spaCy |
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


### Échantillon 1

**Texte** : Température: 5.18°C, légère pluie  
**Longueur** : 33 caractères

#### spaCy
- **Temps** : 12.66 ms
- **Entités détectées** : 1
- **Top entités** :
  - `Température` (PER)

#### YAKE
- **Temps** : 2.0 ms
- **Mots-clés extraits** : 4
- **Top mots-clés** :
  - `0.02570861714399338` (score: 0.0000)
  - `0.04491197687864554` (score: 0.0000)
  - `0.15831692877998726` (score: 0.0000)
  - `0.15831692877998726` (score: 0.0000)

### Échantillon 2

**Texte** : Température: 6.86°C, ciel dégagé  
**Longueur** : 32 caractères

#### spaCy
- **Temps** : 6.0 ms
- **Entités détectées** : 1
- **Top entités** :
  - `Température` (PER)

#### YAKE
- **Temps** : 2.0 ms
- **Mots-clés extraits** : 4
- **Top mots-clés** :
  - `0.02570861714399338` (score: 0.0000)
  - `0.04491197687864554` (score: 0.0000)
  - `0.15831692877998726` (score: 0.0000)
  - `0.15831692877998726` (score: 0.0000)

### Échantillon 3

**Texte** : Température: -2.65°C, ciel dégagé  
**Longueur** : 33 caractères

#### spaCy
- **Temps** : 8.52 ms
- **Entités détectées** : 1
- **Top entités** :
  - `Température` (PER)

#### YAKE
- **Temps** : 1.0 ms
- **Mots-clés extraits** : 4
- **Top mots-clés** :
  - `0.02570861714399338` (score: 0.0000)
  - `0.04491197687864554` (score: 0.0000)
  - `0.15831692877998726` (score: 0.0000)
  - `0.15831692877998726` (score: 0.0000)

### Échantillon 4

**Texte** : Température: 6.27°C, couvert  
**Longueur** : 28 caractères

#### spaCy
- **Temps** : 68.47 ms
- **Entités détectées** : 1
- **Top entités** :
  - `Température` (PER)

#### YAKE
- **Temps** : 1.0 ms
- **Mots-clés extraits** : 2
- **Top mots-clés** :
  - `0.04491197687864554` (score: 0.0000)
  - `0.04491197687864554` (score: 0.0000)

### Échantillon 5

**Texte** : De son côté, l'armée israélienne a affirmé avoir frappé un camp d'entraînement du Hamas.  
**Longueur** : 88 caractères

#### spaCy
- **Temps** : 12.0 ms
- **Entités détectées** : 1
- **Top entités** :
  - `Hamas` (ORG)

#### YAKE
- **Temps** : 14.62 ms
- **Mots-clés extraits** : 10
- **Top mots-clés** :
  - `0.026233073037508336` (score: 0.0000)
  - `0.04940384002065631` (score: 0.0000)
  - `0.08596317751626563` (score: 0.0000)
  - `0.09700399286574239` (score: 0.0000)
  - `0.09700399286574239` (score: 0.0000)
