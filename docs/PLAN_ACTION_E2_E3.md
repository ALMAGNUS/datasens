# 🎯 Plan d'Action DataSens - E2/E3

**Objectif** : Plan stratégique pour passage E1 → E2/E3 avec corrections MPD et intégration nouvelles sources.

**Version** : v1.0 - 2025
**Scope** : Corrections techniques + Roadmap sources

---

## 📋 PHASE 1 : CORRECTIONS MPD (Critique - Avant E2)

### 1.1 Tables de liaison N-N manquantes

**Priorité** : 🔴 **CRITIQUE**

**Actions** :
1. Créer script SQL `fix_mpd_tables_liaison.sql` avec :
   - T38_FLUX_EXEC_ETAPE
   - T39_DOCUMENT_EXEC_ETAPE
   - T40_ETAPE_QC_RULE
2. Exécuter dans `02_schema_create.ipynb` (nouvelle cellule)
3. Documenter dans guide technique V2

**Livrable** : Script SQL + mise à jour notebook 02

---

### 1.2 Corrections ON DELETE

**Priorité** : 🟠 **HAUTE**

**Actions** :
1. Créer script SQL `fix_mpd_on_delete.sql` avec ALTER TABLE pour 10 FK
2. Exécuter après création tables (ordre important)
3. Valider intégrité référentielle

**Livrable** : Script SQL + tests intégrité

---

### 1.3 Ajout colonnes manquantes

**Priorité** : 🟠 **HAUTE**

**Actions** :
1. Ajouter dans DDL MPD final :
   - `t32_exec_etape.nb_entrees`, `nb_sorties`, `erreurs_json`
   - `t31_etape_etl.parametres_modele`
   - `t36_table_version.id_pipeline`
2. Créer migration SQL si tables déjà créées
3. Documenter dans dictionnaire

**Livrable** : ALTER TABLE scripts + DDL final corrigé

---

### 1.4 Contraintes CHECK supplémentaires

**Priorité** : 🟡 **MOYENNE**

**Actions** :
1. Ajouter contraintes géographiques (lat/lon)
2. Ajouter contraintes météo (humidité 0-100%, pression > 0)
3. Ajouter contrainte année indicateurs
4. Créer types ENUM pour `statut`, `action`, `severite`

**Livrable** : Script contraintes + types ENUM

---

## 📊 PHASE 2 : INTÉGRATION SOURCES BAROMÉTRIQUES (E2)

**Objectif** : Enrichir indicateurs sociétaux avec baromètres d'opinion officiels

### 2.1 IFOP Baromètre moral

| Élément | Détails |
|---------|---------|
| **Source** | IFOP (API ou CSV selon disponibilité) |
| **Tables** | `source_barometre`, `document_baro`, `indicateur` |
| **Thèmes** | 1 (Société), 2 (Économie), 5 (Politique) |
| **Fréquence** | Mensuelle |
| **Notebook** | Ajouter section dans `03_ingest_sources.ipynb` |

**Actions** :
1. Créer fonction `ingest_ifop_barometre()`
2. Parser CSV/API selon format disponible
3. Insérer dans `document_baro` + `indicateur` (score moral)
4. Classifier thèmes automatiquement (E2 IA)

**Livrable** : Code fonctionnel dans notebook 03

---

### 2.2 IPSOS Fractures françaises

| Élément | Détails |
|---------|---------|
| **Source** | IPSOS (API ou CSV) |
| **Tables** | `document_baro`, `indicateur` |
| **Thèmes** | 1 (Société), 2 (Économie), 10 (Justice) |
| **Fréquence** | Trimestrielle |

**Actions** : Similaire IFOP, focus polarisation sociale

**Livrable** : Code fonctionnel + documentation

---

### 2.3 INSEE Baromètre social

| Élément | Détails |
|---------|---------|
| **Source** | INSEE (CSV Open Data) |
| **Tables** | `indicateur`, `territoire`, `source_indicateur` |
| **Thèmes** | 1, 2, 11 (Travail) |
| **Fréquence** | Trimestrielle |

**Actions** :
1. Télécharger CSV INSEE régulièrement
2. Parser et insérer indicateurs par territoire
3. Géolocaliser via `code_insee` → `territoire`

**Livrable** : Pipeline automatique CSV → PostgreSQL

---

## 🤖 PHASE 3 : ENRICHISSEMENT IA (E2)

**Objectif** : Classification automatique thèmes/émotions avec modèles IA

### 3.1 Corpus annotés (Hugging Face / Kaggle)

**Sources prioritaires** :
- Hugging Face Datasets : `emotion`, `french_sentiment`
- Kaggle DB : Emotion Detection (SQLite)

**Actions** :
1. Télécharger corpus annotés
2. Insérer dans `document` + `annotation` + `emotion`
3. Utiliser pour fine-tuning modèles E2

**Livrable** : Pipeline ingestion corpus + référentiel modèles IA (`t11_modele_ia`)

---

### 3.2 Classification automatique

**Actions** :
1. Intégrer spaCy/transformers pour NER
2. Classifier thèmes automatiquement → `document_theme`
3. Extraire émotions → `annotation` + `emotion`
4. Évaluer cohérence → `meta_annotation`

**Livrable** : Notebook `06_enrichissement_ia.ipynb` (nouveau)

---

## 📈 PHASE 4 : EXPANSION SOURCES (E3)

### 4.1 APIs supplémentaires

| API | Priorité | Complexité | Livrable |
|-----|----------|------------|----------|
| NewsAPI.org | 🔴 Haute | Faible | Fonction dans notebook 03 |
| Google Trends (PyTrends) | 🟠 Moyenne | Moyenne | Nouveau notebook |
| Météo France | 🟠 Moyenne | Faible | Remplace/complète OWM |

### 4.2 Scraping avancé

| Source | Priorité | Précautions RGPD | Livrable |
|--------|----------|------------------|----------|
| Forums Doctissimo/Reddit FR | 🔴 Haute | Hash auteur strict | Pipeline scraping |
| Trustpilot.fr | 🟠 Moyenne | Respect robots.txt | Pipeline scraping |
| Google Actualités RSS | 🟠 Moyenne | Pas de précautions spéciales | Extension RSS existant |

### 4.3 Big Data massif

| Source | Priorité | Complexité | Livrable |
|--------|----------|------------|----------|
| Common Crawl FR | 🟠 Moyenne | Élevée | Pipeline batch Prefect |
| Twitter Academic API | 🔴 Haute | Moyenne | Pipeline temps réel |
| YouTube API | 🟠 Moyenne | Faible | Pipeline scraping |

---

## 🛠️ PHASE 5 : AUTOMATISATION & PRODUCTION (E3)

### 5.1 Orchestration (Prefect/Airflow)

**Actions** :
1. Créer DAG/Flow pour collecte quotidienne
2. Gérer dépendances sources
3. Alertes erreurs via Slack/Email
4. Monitoring performances

**Livrable** : DAG Prefect ou Airflow

---

### 5.2 Dashboard Grafana

**Actions** :
1. Connecter Grafana → PostgreSQL
2. Créer dashboards :
   - Volume données par source
   - Évolution émotions/tendances
   - KPIs qualité données
   - Mapping géographique indicateurs

**Livrable** : Dashboard Grafana configuré

---

### 5.3 API REST (FastAPI)

**Actions** :
1. Créer API REST pour consultation données
2. Endpoints :
   - `/api/documents` (recherche documents)
   - `/api/indicateurs` (requêtes indicateurs)
   - `/api/emotions` (statistiques émotions)
   - `/api/themes` (classement par thème)
3. Documentation OpenAPI/Swagger

**Livrable** : API FastAPI + documentation

---

## 📚 PHASE 6 : DOCUMENTATION & GUIDE TECHNIQUE

### 6.1 Mise à jour Guide Technique V2

**Actions** :
1. Ajouter section "Schéma 36 tables → 40 tables"
2. Documenter corrections MPD
3. Ajouter section "Référentiel sources E2/E3"
4. Mettre à jour roadmap E2/E3 avec sources prioritaires

**Livrable** : `docs/GUIDE_TECHNIQUE_JURY_V2.md` mis à jour

---

### 6.2 Documentation sources

**Actions** :
1. Créer `docs/SOURCES_IMPLEMENTATIONS.md` (déjà existant, enrichir)
2. Documenter chaque source :
   - Format données
   - Tables PostgreSQL cibles
   - Exemple code ingestion
   - Précautions RGPD

**Livrable** : Documentation complète par source

---

## ✅ CHECKLIST VALIDATION E2

### Corrections MPD
- [ ] Tables de liaison T38-T40 créées
- [ ] ON DELETE corrigés (10 FK)
- [ ] Colonnes manquantes ajoutées (3)
- [ ] Contraintes CHECK ajoutées
- [ ] Types ENUM créés

### Sources barométriques (3)
- [ ] IFOP baromètre moral intégré
- [ ] IPSOS fractures intégrées
- [ ] INSEE baromètre social intégré

### Enrichissement IA
- [ ] Corpus annotés intégrés (Hugging Face/Kaggle)
- [ ] Classification automatique thèmes fonctionnelle
- [ ] Extraction émotions automatique fonctionnelle
- [ ] Évaluation cohérence IA/Humain opérationnelle

### Expansion sources (5)
- [ ] NewsAPI.org intégré
- [ ] Forums Doctissimo/Reddit FR intégrés
- [ ] Twitter Academic API intégré
- [ ] Google Trends intégré
- [ ] Météo France intégré

### Production E3
- [ ] Orchestration automatique (Prefect/Airflow)
- [ ] Dashboard Grafana opérationnel
- [ ] API REST FastAPI déployée
- [ ] Monitoring et alertes configurés

### Documentation
- [ ] Guide technique V2 mis à jour
- [ ] Documentation sources complète
- [ ] README E2/E3 créé

---

## 🎯 PRIORISATION RÉCAPITULATIVE

| Phase | Priorité | Durée estimée | Dépendances |
|-------|----------|---------------|-------------|
| **PHASE 1 : Corrections MPD** | 🔴 **CRITIQUE** | 2-3 jours | Aucune |
| **PHASE 2 : Baromètres (3 sources)** | 🔴 **HAUTE** | 1 semaine | Phase 1 |
| **PHASE 3 : Enrichissement IA** | 🟠 **HAUTE** | 2 semaines | Phase 1, Phase 2 |
| **PHASE 4 : Expansion sources (5)** | 🟠 **MOYENNE** | 2-3 semaines | Phase 3 |
| **PHASE 5 : Production E3** | 🟡 **MOYENNE** | 3-4 semaines | Phase 4 |
| **PHASE 6 : Documentation** | 🟢 **FAIBLE** | 1 semaine | Parallèle toutes phases |

---

**Note** : Plan d'action stratégique prêt. Commencer par Phase 1 (corrections MPD) avant toute intégration E2. 🚀
