# Séparation E1 / E2 / E3 - DataSens

**Date** : 2025-11-19  
**Objectif** : Clarifier la séparation entre E1 (ETL pur) et E2/E3 (Annotation IA)

---

## 🎯 E1_v3 : ETL PUR (SANS IA)

### Ce que fait E1

**Pipeline ETL classique** :
- **Extract** : Collecte depuis sources (RSS, API, CSV, GDELT, Baromètres)
- **Transform** : Nettoyage, normalisation, déduplication (règles métier, pas d'IA)
- **Load** : PostgreSQL (SILVER) + MinIO (RAW) + Dataset GOLD

**Actions E1** :
- ✅ Structuration données (38 tables Merise)
- ✅ Nettoyage et déduplication (hash_fingerprint SHA-256)
- ✅ Enrichissement territorial (T13-T17) - données brutes INSEE (pas de géocodage IA)
- ✅ Enrichissement contextuel (météo, événements, baromètres) - données brutes
- ✅ Dataset GOLD avec colonnes CRÉÉES mais VIDENTES

**Ce que E1 NE fait PAS** :
- ❌ Pas d'annotation IA (FlauBERT, CamemBERT)
- ❌ Pas de géocodage automatique (API IGN)
- ❌ Pas de détection émotions
- ❌ Pas de classification sentimentale

**Statut E1_v3** : ✅ 98 documents préparés, colonnes `territoire_*` et `humeur_*` créées mais VIDENTES (status: pending)

---

## 🎯 E2/E3 : Annotation IA

### Ce que fait E2/E3

**Annotation avec modèles IA** :
- **Annotation Territoriale** : Géocodage (API IGN), enrichissement INSEE
- **Annotation Émotionnelle** : FlauBERT-sentiment, CamemBERT-sentiment, NER émotions
- **Validation** : Validation croisée, contrôle qualité

**Modèles IA utilisés (E2/E3 UNIQUEMENT)** :
- FlauBERT-sentiment : Classification sentimentale
- CamemBERT-sentiment : Alternative FlauBERT
- NER Émotions : Détection émotions fines
- Sentence-Transformers : Embeddings sémantiques

**Actions E2/E3** :
- ✅ Géocodage automatique (API IGN)
- ✅ Classification sentimentale (FlauBERT/CamemBERT)
- ✅ Détection émotions (NER)
- ✅ Calcul valence
- ✅ Validation croisée

---

## 📊 Séparation Claire

| Phase | Rôle | IA ? | Modèles |
|-------|------|------|---------|
| **E1_v3** | ETL pur | ❌ NON | Aucun |
| **E2/E3** | Annotation | ✅ OUI | FlauBERT, CamemBERT, NER |

---

## 🎯 Pipeline Complet

```
E1_v3 : ETL PUR (SANS IA)
    ↓
RAW (MinIO) → SILVER (PostgreSQL) → GOLD (Dataset avec colonnes vides)
    ↓
E2/E3 : Annotation IA
    ↓
Dataset GOLD Annoté (colonnes remplies avec modèles IA)
```

---

**IMPORTANT** : E1 ne fait QUE la préparation structurelle, PAS d'annotation IA

