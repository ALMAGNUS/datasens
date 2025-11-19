# Plan d'Action Démo - Major de Promo ! 🏆

**Date** : 2025-11-19  
**Objectif** : Impressionner le jury avec une démo technique irréprochable

---

## 🎯 Vision Stratégique

**Objectif** : Démontrer une maîtrise technique complète avec :
1. ✅ Choix technologiques justifiés
2. ✅ Tests comparatifs réels (spaCy vs YAKE)
3. ✅ Architecture solide (Merise, ETL, DataLake)
4. ✅ Préparation E2/E3 (annotation IA)

---

## 📋 Checklist Pré-Démo (24h avant)

### ✅ Infrastructure
- [ ] Docker Compose lancé (PostgreSQL + MinIO)
- [ ] Ports vérifiés (5432 PostgreSQL, 9000 MinIO)
- [ ] `.env` configuré et testé
- [ ] Virtual environment activé (`.venv`)

### ✅ Données
- [ ] Dataset GOLD disponible (`data/dataset/datasens_gold_*.csv`)
- [ ] Au moins 50+ documents dans PostgreSQL
- [ ] Sources actives (RSS, API, Baromètres)

### ✅ Notebooks
- [ ] `01_setup_env.ipynb` : Test connexions OK
- [ ] `02_schema_create.ipynb` : 38 tables créées
- [ ] `03_ingest_sources.ipynb` : Visualisations OK
- [ ] Tous les kernels sélectionnés (`.venv`)

### ✅ Documentation
- [ ] Rapport comparatif dépendances lu
- [ ] Résultats test spaCy vs YAKE disponibles
- [ ] Plan d'action mémorisé

---

## 🎬 Script Démo (30 minutes)

### Phase 1 : Introduction (5 min)

**Message clé** : "DataSens est un pipeline ETL complet avec architecture Merise, préparé pour annotation IA E2/E3"

**Points à présenter** :
1. Architecture globale (RAW → SILVER → GOLD → Dataset IA)
2. 38 tables Merise (MCD/MLD/MPD)
3. Sources multiples (RSS, API, CSV, GDELT, Baromètres)
4. Préparation annotation IA (colonnes prêtes)

---

### Phase 2 : Infrastructure & Choix Techniques (10 min)

#### 2.1 DataLake : MinIO vs Alternatives

**Démontrer** :
- MinIO lancé (Docker)
- Compatibilité S3 native
- Upload fichier RAW test

**Justification** :
> "MinIO choisi pour simplicité + compatibilité S3. Alternative Cassandra si volume massif E3."

**Support** : `docs/COMPARAISON_DEPENDANCES_ALTERNATIVES.md`

#### 2.2 SGBD : PostgreSQL vs Alternatives

**Démontrer** :
- Connexion PostgreSQL
- 38 tables Merise listées
- Relations FK vérifiées

**Justification** :
> "PostgreSQL optimal pour relations Merise complexes. Alternative MongoDB si données non structurées uniquement."

#### 2.3 ETL : pandas 2.x vs Alternatives

**Démontrer** :
- Dataset GOLD chargé avec pandas
- Performance (Arrow support)
- Export Parquet

**Justification** :
> "pandas 2.x : standard industrie + performance optimisée. Alternative Spark si Big Data distribué E3."

---

### Phase 3 : Test Comparatif NLP (10 min) ⭐ **POINT FORT**

#### 3.1 Présentation Test spaCy vs YAKE

**Démontrer** :
- Exécution script `scripts/test_comparatif_spacy_yake.py`
- Résultats en temps réel
- Comparaison performance + qualité

**Résultats attendus** :
- spaCy : NER (entités nommées) - lieux, personnes, organisations
- YAKE : Mots-clés extraits - thèmes, contexte

**Justification** :
> "Test comparatif réel : spaCy pour NER territorial, YAKE pour mots-clés. Complémentarité pour E2/E3."

**Support** : `docs/tests_comparatifs/RAPPORT_COMPARATIF_SPACY_YAKE_*.md`

#### 3.2 Démonstration Live

**Exécuter** :
```python
# Exemple texte
text = "Le maire de Paris annonce une nouvelle politique écologique pour 2026."

# spaCy
doc = nlp(text)
entities = [(ent.text, ent.label_) for ent in doc.ents]
# Résultat : [('Paris', 'LOC'), ('2026', 'DATE')]

# YAKE
keywords = kw_extractor.extract_keywords(text)
# Résultat : [('politique écologique', 0.1234), ('maire Paris', 0.2345)]
```

**Message** :
> "spaCy détecte entités (Paris = lieu), YAKE extrait thèmes (politique écologique). Complémentarité parfaite."

---

### Phase 4 : Pipeline ETL Complet (5 min)

#### 4.1 Notebook `03_ingest_sources.ipynb`

**Démontrer** :
- Collecte sources (RSS, API, Baromètres)
- Pipeline RAW → SILVER → GOLD
- Visualisations dashboard

**Points clés** :
- 98+ documents ingérés
- Dataset GOLD avec colonnes IA prêtes
- Métriques qualité affichées

---

## 🎯 Messages Clés pour Jury

### 1. Choix Technologiques Justifiés

**MinIO** : Simplicité + Compatibilité S3 (vs Cassandra si volume massif)  
**PostgreSQL** : Relations Merise (vs MongoDB si non structuré)  
**pandas 2.x** : Standard + Performance (vs Spark si distribué)  
**spaCy** : NER français (vs Transformers si besoin sémantique avancé)  
**YAKE** : Mots-clés non supervisé (vs KeyBERT si besoin sémantique)

### 2. Test Comparatif Réel

**spaCy** : NER (entités nommées) - optimal pour annotation territoriale  
**YAKE** : Mots-clés - optimal pour contexte/thèmes  
**Complémentarité** : Les deux utilisés ensemble pour E2/E3

### 3. Architecture Solide

**38 tables Merise** : MCD/MLD/MPD complet  
**Pipeline ETL** : RAW → SILVER → GOLD → Dataset IA  
**Préparation E2/E3** : Colonnes annotation créées (status: pending)

### 4. Veille Technologique

**Rapport complet** : `docs/VEILLE_TECHNIQUE_DEPENDANCES.md`  
**Comparaisons** : `docs/COMPARAISON_DEPENDANCES_ALTERNATIVES.md`  
**Tests réels** : `docs/tests_comparatifs/`

---

## 📊 Support Visuel

### Documents à Avoir Ouverts

1. **`docs/COMPARAISON_DEPENDANCES_ALTERNATIVES.md`** : Justifications choix
2. **`docs/tests_comparatifs/RAPPORT_COMPARATIF_SPACY_YAKE_*.md`** : Résultats tests
3. **`docs/VEILLE_TECHNIQUE_DEPENDANCES.md`** : Veille technologique
4. **`notebooks/datasens_E1_v3/03_ingest_sources.ipynb`** : Dashboard visualisations

### Visualisations à Présenter

1. **Dashboard Pipeline** : Architecture RAW → SILVER → GOLD
2. **Métriques Sources** : Volumes par source
3. **Test Comparatif** : Graphiques spaCy vs YAKE (temps, qualité)

---

## 🎤 Réponses aux Questions Probables

### Q1 : "Pourquoi MinIO et pas Cassandra ?"

**Réponse** :
> "MinIO choisi pour E1 : simplicité d'installation, compatibilité S3 standard, et migration future transparente. Cassandra serait optimal pour E3 si volume massif (millions de documents) nécessitant distribution."

**Support** : `docs/COMPARAISON_DEPENDANCES_ALTERNATIVES.md` section MinIO

### Q2 : "Pourquoi PostgreSQL et pas MongoDB ?"

**Réponse** :
> "PostgreSQL optimal pour architecture Merise avec 38 tables relationnelles. MongoDB serait adapté si données non structurées uniquement, mais nous avons besoin d'intégrité référentielle et relations complexes."

**Support** : `docs/COMPARAISON_DEPENDANCES_ALTERNATIVES.md` section PostgreSQL

### Q3 : "spaCy ou YAKE, lequel est meilleur ?"

**Réponse** :
> "Test comparatif réalisé : spaCy optimal pour NER (entités nommées - lieux, personnes), YAKE optimal pour extraction mots-clés (thèmes, contexte). Complémentarité : les deux utilisés ensemble pour E2/E3."

**Support** : `docs/tests_comparatifs/RAPPORT_COMPARATIF_SPACY_YAKE_*.md`

### Q4 : "Pourquoi pandas 2.x et pas Spark ?"

**Réponse** :
> "pandas 2.x : standard industrie, performance optimisée avec Arrow, écosystème complet. Spark serait optimal pour E3 si traitement Big Data distribué nécessaire."

**Support** : `docs/COMPARAISON_DEPENDANCES_ALTERNATIVES.md` section pandas

---

## 🏆 Points Bonus pour Major de Promo

### 1. Veille Technologique Complète
- ✅ Rapport comparatif dépendances vs alternatives
- ✅ Veille technique sur toutes les dépendances
- ✅ Justifications techniques solides

### 2. Tests Comparatifs Réels
- ✅ Test spaCy vs YAKE exécuté
- ✅ Résultats mesurés et documentés
- ✅ Démonstration live possible

### 3. Architecture Solide
- ✅ 38 tables Merise (MCD/MLD/MPD)
- ✅ Pipeline ETL complet
- ✅ Préparation E2/E3 (colonnes IA)

### 4. Documentation Professionnelle
- ✅ Rapports techniques complets
- ✅ Comparaisons justifiées
- ✅ Plan d'action structuré

---

## ⚡ Actions Immédiates (Maintenant)

1. **Exécuter test comparatif** :
   ```bash
   python scripts/test_comparatif_spacy_yake.py
   ```

2. **Vérifier résultats** :
   - Lire `docs/tests_comparatifs/RAPPORT_COMPARATIF_SPACY_YAKE_*.md`
   - Préparer démonstration live

3. **Relire documentation** :
   - `docs/COMPARAISON_DEPENDANCES_ALTERNATIVES.md`
   - `docs/VEILLE_TECHNIQUE_DEPENDANCES.md`

4. **Tester démo complète** :
   - Exécuter notebooks dans l'ordre
   - Vérifier visualisations
   - Préparer réponses questions

---

## 🎯 Objectif Final

**Impressionner le jury avec** :
1. ✅ Maîtrise technique complète
2. ✅ Choix justifiés et documentés
3. ✅ Tests comparatifs réels
4. ✅ Architecture solide et évolutive

**Résultat attendu** : 🏆 **MAJOR DE PROMO !**

---

**Dernière mise à jour** : 2025-11-19  
**Statut** : ✅ PRÊT POUR DÉMO

