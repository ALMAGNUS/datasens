# Analyse du MCD DataSens - 36 Tables

## 📊 Dénombrement des tables

**Tables identifiées dans le MCD** :

### Domaine Collecte (4 tables)
1. T01_TYPE_DONNEE
2. T02_SOURCE
3. T03_FLUX
4. T37_ARCHIVE_FLUX

### Annotation & Emotions (9 tables)
5. T04_DOCUMENT
6. T05_ANNOTATION
7. T06_ANNOTATION_EMOTION
8. T07_META_ANNOTATION
9. T08_EMOTION
10. T09_TYPE_EMOTION
11. T10_VALENCE
12. T11_MODELE_IA
13. T12_UTILISATEUR

### Géographie (5 tables)
14. T13_PAYS
15. T14_REGION
16. T15_DEPARTEMENT
17. T16_COMMUNE
18. T17_TERRITOIRE

### Contexte : Météo & Indicateurs (5 tables)
19. T18_TYPE_METEO
20. T19_METEO
21. T20_TYPE_INDICATEUR
22. T21_SOURCE_INDICATEUR
23. T22_INDICATEUR

### Thèmes / Événements (5 tables)
24. T23_THEME_CATEGORY
25. T24_THEME
26. T25_EVENEMENT
27. T26_DOCUMENT_THEME
28. T27_DOCUMENT_EVENEMENT

### Baromètres (2 tables)
29. T28_SOURCE_BAROMETRE
30. T29_DOCUMENT_BARO

### Pipeline / Qualité (5 tables)
31. T30_PIPELINE
32. T31_ETAPE_ETL
33. T32_EXEC_ETAPE
34. T33_QC_RULE
35. T34_QC_RESULT

### Gouvernance / Versionning (2 tables)
36. T35_TABLE_AUDIT
37. T36_TABLE_VERSION

**⚠️ TOTAL : 37 tables identifiées** (au lieu de 36 annoncées)

**Hypothèse** : T37_ARCHIVE_FLUX pourrait être comptée comme extension de T03_FLUX, ou erreur de comptage.

---

## ✅ Vérifications de cohérence

### 1. Relations vérifiées

#### Domaine Collecte ✅
- T01_TYPE_DONNEE ||--o{ T02_SOURCE : "catégorise" ✅
- T02_SOURCE ||--o{ T03_FLUX : "alimente" ✅
- T03_FLUX ||--o{ T04_DOCUMENT : "génère" ✅
- T02_SOURCE ||--o{ T37_ARCHIVE_FLUX : "historise" ✅

#### Annotation & Emotions ✅
- T04_DOCUMENT ||--o{ T05_ANNOTATION : "contient" ✅
- T05_ANNOTATION ||--o{ T06_ANNOTATION_EMOTION : "associe" ✅
- T08_EMOTION ||--o{ T06_ANNOTATION_EMOTION : "rattachée" ✅ (relation N-N via table de liaison)
- T08_EMOTION }o--|| T09_TYPE_EMOTION : "appartient à" ✅
- T09_TYPE_EMOTION }o--|| T10_VALENCE : "porte" ✅
- T08_EMOTION }o--|| T11_MODELE_IA : "produite par" ✅
- T05_ANNOTATION ||--o{ T07_META_ANNOTATION : "évaluée par" ✅
- T11_MODELE_IA ||--o{ T07_META_ANNOTATION : "produit" ✅
- T12_UTILISATEUR ||--o{ T05_ANNOTATION : "valide" ✅

#### Géographie ✅
- T04_DOCUMENT }o--|| T17_TERRITOIRE : "localisé dans" ✅
- T17_TERRITOIRE }o--|| T16_COMMUNE : "référence" ✅
- T16_COMMUNE }o--|| T15_DEPARTEMENT : "appartient à" ✅
- T15_DEPARTEMENT }o--|| T14_REGION : "rattaché à" ✅
- T14_REGION }o--|| T13_PAYS : "situé dans" ✅

#### Contexte ✅
- T18_TYPE_METEO ||--o{ T19_METEO : "qualifie" ✅
- T17_TERRITOIRE ||--o{ T19_METEO : "possède" ✅
- T20_TYPE_INDICATEUR ||--o{ T22_INDICATEUR : "définit" ✅
- T21_SOURCE_INDICATEUR ||--o{ T22_INDICATEUR : "publie" ✅
- T17_TERRITOIRE ||--o{ T22_INDICATEUR : "constate" ✅

#### Thèmes / Événements ✅
- T23_THEME_CATEGORY ||--o{ T24_THEME : "classe" ✅
- T24_THEME ||--o{ T25_EVENEMENT : "influence" ✅
- T04_DOCUMENT }o--o{ T26_DOCUMENT_THEME : "traite" ✅ (relation N-N)
- T04_DOCUMENT }o--o{ T27_DOCUMENT_EVENEMENT : "lié à" ✅ (relation N-N)

#### Baromètres ✅
- T28_SOURCE_BAROMETRE ||--o{ T29_DOCUMENT_BARO : "documente" ✅
- T29_DOCUMENT_BARO ||--|| T04_DOCUMENT : "décrit" ✅ (relation 1-1)

#### Pipeline / Qualité ✅
- T30_PIPELINE ||--o{ T31_ETAPE_ETL : "compose" ✅
- T31_ETAPE_ETL ||--o{ T32_EXEC_ETAPE : "exécutée par" ✅
- T03_FLUX }o--o{ T32_EXEC_ETAPE : "alimente" ✅
- T04_DOCUMENT }o--o{ T32_EXEC_ETAPE : "produit" ✅
- T31_ETAPE_ETL }o--o{ T33_QC_RULE : "applique" ✅
- T32_EXEC_ETAPE ||--o{ T34_QC_RESULT : "génère" ✅
- T33_QC_RULE ||--o{ T34_QC_RESULT : "vérifie" ✅

#### Gouvernance / Versionning ✅
- T12_UTILISATEUR ||--o{ T35_TABLE_AUDIT : "opère" ✅
- T35_TABLE_AUDIT }o--|| T36_TABLE_VERSION : "trace" ✅
- T36_TABLE_VERSION }o--|| T30_PIPELINE : "versionne" ✅

---

## 🔍 Points de vérification à demander

### 1. Cardinalités
- **T04_DOCUMENT }o--|| T17_TERRITOIRE** : Un document peut-il être sans territoire ? (NULL autorisé ?)
- **T29_DOCUMENT_BARO ||--|| T04_DOCUMENT** : Relation 1-1 stricte ? Un document baro = exactement 1 document ?
- **T17_TERRITOIRE }o--|| T16_COMMUNE** : Un territoire peut-il être sans commune ? (cas territoire plus large ?)

### 2. Clés primaires composées
- **T06_ANNOTATION_EMOTION** : `id_annotation FK + id_emotion FK` → Clé primaire composée ?
- **T26_DOCUMENT_THEME** : `id_doc FK + id_theme FK` → Clé primaire composée ?
- **T27_DOCUMENT_EVENEMENT** : `id_doc FK + id_event FK` → Clé primaire composée ?

### 3. Indexation suggérée
- **T04_DOCUMENT.hash_fingerprint** : UNIQUE ? (déduplication)
- **T16_COMMUNE.code_insee** : UNIQUE ?
- **T04_DOCUMENT.date_publication** : Index pour requêtes temporelles ?
- **T19_METEO.date_obs** : Index temporel ?
- **T25_EVENEMENT.date_event** : Index temporel ?

### 4. Contraintes à confirmer
- **T05_ANNOTATION.polarity** : ENUM('positive', 'negative', 'neutral') ?
- **T08_EMOTION.score_confiance** : CHECK(score_confiance BETWEEN 0 AND 1) ?
- **T22_INDICATEUR.valeur** : CHECK(valeur >= 0) si indicateur positif ?
- **T32_EXEC_ETAPE.statut** : ENUM('pending', 'running', 'success', 'error') ?

---

## 📋 Comparaison E1 (18 tables) → E2 (36 tables)

### Tables conservées (renommées)
- `type_donnee` → **T01_TYPE_DONNEE**
- `source` → **T02_SOURCE**
- `flux` → **T03_FLUX**
- `document` → **T04_DOCUMENT**
- `territoire` → **T17_TERRITOIRE** (enrichie)
- `type_meteo` → **T18_TYPE_METEO**
- `meteo` → **T19_METEO**
- `type_indicateur` → **T20_TYPE_INDICATEUR**
- `source_indicateur` → **T21_SOURCE_INDICATEUR**
- `indicateur` → **T22_INDICATEUR**
- `theme` → **T24_THEME** (enrichie avec catégories)
- `evenement` → **T25_EVENEMENT**
- `document_evenement` → **T27_DOCUMENT_EVENEMENT**
- `pipeline` → **T30_PIPELINE**
- `etape_etl` → **T31_ETAPE_ETL**
- `utilisateur` → **T12_UTILISATEUR**
- `qc_rule` → **T33_QC_RULE**
- `qc_result` → **T34_QC_RESULT**

### Nouvelles tables (18 tables)

#### Annotation & Emotions (7 nouvelles)
- T05_ANNOTATION
- T06_ANNOTATION_EMOTION
- T07_META_ANNOTATION
- T08_EMOTION
- T09_TYPE_EMOTION
- T10_VALENCE
- T11_MODELE_IA

#### Géographie (4 nouvelles)
- T13_PAYS
- T14_REGION
- T15_DEPARTEMENT
- T16_COMMUNE

#### Thèmes (1 nouvelle)
- T23_THEME_CATEGORY
- T26_DOCUMENT_THEME (nouvelle relation N-N)

#### Baromètres (2 nouvelles)
- T28_SOURCE_BAROMETRE
- T29_DOCUMENT_BARO

#### Pipeline (1 nouvelle)
- T32_EXEC_ETAPE

#### Gouvernance (2 nouvelles)
- T35_TABLE_AUDIT
- T36_TABLE_VERSION

#### Collecte (1 nouvelle)
- T37_ARCHIVE_FLUX

---

## ✅ Statut de vérification

**EN ATTENTE** des documents suivants pour validation complète :
- [ ] MLD (Modèle Logique de Données) avec types de données précis
- [ ] MPD (Modèle Physique de Données) avec DDL PostgreSQL complet
- [ ] Relations détaillées (cardinalités précises, contraintes)
- [ ] Indexations complètes

---

## ✅ Validation MLD (Modèle Logique de Données)

### Cardinalités explicites (MLD)

#### Relations 1-N (Obligatoires)
- ✅ T01_TYPE_DONNEE ||--o{ T02_SOURCE : "(1–N)" — Un type de donnée → plusieurs sources
- ✅ T02_SOURCE ||--o{ T03_FLUX : "(1–N)" — Une source → plusieurs flux
- ✅ T03_FLUX ||--o{ T04_DOCUMENT : "(1–N)" — Un flux → plusieurs documents
- ✅ T02_SOURCE ||--o{ T37_ARCHIVE_FLUX : "(1–N)" — Une source → plusieurs archives
- ✅ T04_DOCUMENT ||--o{ T05_ANNOTATION : "(1–N)" — Un document → plusieurs annotations
- ✅ T05_ANNOTATION ||--o{ T06_ANNOTATION_EMOTION : "(1–N)" — Une annotation → plusieurs émotions associées
- ✅ T08_EMOTION ||--o{ T06_ANNOTATION_EMOTION : "(1–N)" — Une émotion → plusieurs annotations
- ✅ T05_ANNOTATION ||--o{ T07_META_ANNOTATION : "(1–N)" — Une annotation → plusieurs méta-annotations
- ✅ T11_MODELE_IA ||--o{ T07_META_ANNOTATION : "(1–N)" — Un modèle → plusieurs méta-annotations
- ✅ T12_UTILISATEUR ||--o{ T05_ANNOTATION : "(1–N)" — Un utilisateur → plusieurs annotations
- ✅ T18_TYPE_METEO ||--o{ T19_METEO : "(1–N)" — Un type météo → plusieurs relevés
- ✅ T17_TERRITOIRE ||--o{ T19_METEO : "(1–N)" — Un territoire → plusieurs relevés météo
- ✅ T20_TYPE_INDICATEUR ||--o{ T22_INDICATEUR : "(1–N)" — Un type → plusieurs indicateurs
- ✅ T21_SOURCE_INDICATEUR ||--o{ T22_INDICATEUR : "(1–N)" — Une source → plusieurs indicateurs
- ✅ T17_TERRITOIRE ||--o{ T22_INDICATEUR : "(1–N)" — Un territoire → plusieurs indicateurs
- ✅ T23_THEME_CATEGORY ||--o{ T24_THEME : "(1–N)" — Une catégorie → plusieurs thèmes
- ✅ T24_THEME ||--o{ T25_EVENEMENT : "(1–N)" — Un thème → plusieurs événements
- ✅ T28_SOURCE_BAROMETRE ||--o{ T29_DOCUMENT_BARO : "(1–N)" — Une source → plusieurs documents baro
- ✅ T30_PIPELINE ||--o{ T31_ETAPE_ETL : "(1–N)" — Un pipeline → plusieurs étapes
- ✅ T31_ETAPE_ETL ||--o{ T32_EXEC_ETAPE : "(1–N)" — Une étape → plusieurs exécutions
- ✅ T32_EXEC_ETAPE ||--o{ T34_QC_RESULT : "(1–N)" — Une exécution → plusieurs résultats QC
- ✅ T33_QC_RULE ||--o{ T34_QC_RESULT : "(1–N)" — Une règle → plusieurs résultats
- ✅ T12_UTILISATEUR ||--o{ T35_TABLE_AUDIT : "(1–N)" — Un utilisateur → plusieurs audits

#### Relations N-1 (Optionnelles si }o--||)
- ✅ T04_DOCUMENT }o--|| T17_TERRITOIRE : "(N–1)" — Un document peut être sans territoire (NULL autorisé)
- ✅ T17_TERRITOIRE }o--|| T16_COMMUNE : "(N–1)" — Un territoire peut être sans commune (à confirmer)
- ✅ T16_COMMUNE }o--|| T15_DEPARTEMENT : "(N–1)" — **⚠️ Anomalie** : Une commune DOIT avoir un département (NOT NULL requis)
- ✅ T15_DEPARTEMENT }o--|| T14_REGION : "(N–1)" — **⚠️ Anomalie** : Un département DOIT avoir une région (NOT NULL requis)
- ✅ T14_REGION }o--|| T13_PAYS : "(N–1)" — **⚠️ Anomalie** : Une région DOIT avoir un pays (NOT NULL requis)
- ✅ T08_EMOTION }o--|| T09_TYPE_EMOTION : "(N–1)" — Une émotion DOIT avoir un type (NOT NULL requis)
- ✅ T09_TYPE_EMOTION }o--|| T10_VALENCE : "(N–1)" — Un type émotion DOIT avoir une valence (NOT NULL requis)
- ✅ T08_EMOTION }o--|| T11_MODELE_IA : "(N–1)" — Une émotion peut être sans modèle (NULL autorisé ?)
- ✅ T35_TABLE_AUDIT }o--|| T36_TABLE_VERSION : "(N–1)" — Un audit peut être sans version (NULL autorisé ?)
- ✅ T36_TABLE_VERSION }o--|| T30_PIPELINE : "(N–1)" — Une version peut être sans pipeline (NULL autorisé ?)

#### Relations N-N (Tables de liaison)
- ✅ T04_DOCUMENT }o--o{ T26_DOCUMENT_THEME : "(N–N)" — Document ↔ Thème (table de liaison)
- ✅ T04_DOCUMENT }o--o{ T27_DOCUMENT_EVENEMENT : "(N–N)" — Document ↔ Événement (table de liaison)
- ✅ T06_ANNOTATION_EMOTION : Table de liaison pour Annotation ↔ Émotion (N–N)
- ✅ T03_FLUX }o--o{ T32_EXEC_ETAPE : "(N–N)" — **⚠️ Complexe** : Un flux peut alimenter plusieurs exécutions, une exécution peut traiter plusieurs flux (table de liaison nécessaire ?)
- ✅ T04_DOCUMENT }o--o{ T32_EXEC_ETAPE : "(N–N)" — **⚠️ Complexe** : Un document peut être produit par plusieurs exécutions, une exécution peut produire plusieurs documents (table de liaison nécessaire ?)
- ✅ T31_ETAPE_ETL }o--o{ T33_QC_RULE : "(N–N)" — **⚠️ Complexe** : Une étape peut appliquer plusieurs règles, une règle peut être appliquée à plusieurs étapes (table de liaison nécessaire ?)

#### Relations 1-1
- ✅ T29_DOCUMENT_BARO ||--|| T04_DOCUMENT : "(1–1)" — **⚠️ Contrainte stricte** : Un document baro = exactement 1 document, et réciproquement (UNIQUE contraint nécessaire)

### ⚠️ Anomalies détectées dans le MLD

1. **T16_COMMUNE }o--|| T15_DEPARTEMENT** : Relation optionnelle (NULL autorisé) alors qu'une commune DOIT appartenir à un département. **Suggestion** : `||--||` (obligatoire).

2. **T15_DEPARTEMENT }o--|| T14_REGION** : Relation optionnelle alors qu'un département DOIT appartenir à une région. **Suggestion** : `||--||` (obligatoire).

3. **T14_REGION }o--|| T13_PAYS** : Relation optionnelle alors qu'une région DOIT appartenir à un pays. **Suggestion** : `||--||` (obligatoire).

4. **Relations N-N complexes** : T03_FLUX ↔ T32_EXEC_ETAPE, T04_DOCUMENT ↔ T32_EXEC_ETAPE, T31_ETAPE_ETL ↔ T33_QC_RULE nécessitent des tables de liaison explicites dans le MPD.

5. **T29_DOCUMENT_BARO ||--|| T04_DOCUMENT** : Relation 1-1 stricte nécessite contrainte UNIQUE sur la FK dans T29_DOCUMENT_BARO.

---

**Note** : Analyse MLD effectuée. ⏳ **EN ATTENTE du MPD** pour validation DDL PostgreSQL complète.
