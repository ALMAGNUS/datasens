# 📊 Baromètres DataSens - Sources Métier

Ce document liste les 10 types de baromètres à implémenter pour enrichir le dataset DataSens.

## 🎯 Vue d'ensemble

Ces baromètres couvrent différents aspects de la société française et permettent d'enrichir les données de sentiment, d'émotions et de perception citoyenne.

---

## 📋 Tableau des Baromètres

| Type de source | Exemple concret | Thématique couverte | Format prévu | Catégorie E1 |
|---|---|---|---|---|
| 🔹 Baromètre de confiance politique & sociale | CEVIPOF – La confiance des Français dans la politique | Société, gouvernance, démocratie, institutions | CSV / PDF / API | API / Fichier plat |
| 🔹 Baromètre des émotions et du moral | Kantar Public / Ipsos Mood of France | Joie, anxiété, colère, espoir (→ table EMOTION) | CSV / scraping | CSV / Web Scraping |
| 🔹 Baromètre environnemental | ADEME / IFOP pour la transition écologique | Écologie, énergie, climat, sobriété | Dataset plat + API | API / CSV |
| 🔹 Baromètre économique et social | INSEE Conjoncture + BVA Observatoire social | Pouvoir d'achat, chômage, inflation, emploi | Base SQL / CSV | Base de données / CSV |
| 🔹 Baromètre des médias et de la confiance | La Croix – Baromètre Kantar sur les médias | Information, confiance médiatique, fake news | Web scraping | Web Scraping |
| 🔹 Baromètre sport & cohésion sociale | Ministère des Sports / CNOSF / Paris 2024 | Sport, bien-être, fierté nationale, cohésion | CSV / API | CSV / API |
| 🔹 Baromètre des discriminations et égalité | Défenseur des Droits / IFOP | Inclusion, diversité, égalité femmes-hommes | CSV / API | CSV / API |
| 🔹 Baromètre santé mentale et bien-être | Santé Publique France – CoviPrev | Stress, anxiété, santé mentale post-COVID | CSV | CSV |
| 🔹 Baromètre climat social et tensions | Elabe / BFMTV Opinion 2024 | Colère, frustration, confiance, peur | Web Scraping | Web Scraping |
| 🔹 Baromètre innovation et IA | CNIL / France IA / Capgemini Research Institute | Adoption de l'IA, confiance numérique | PDF / API | API / PDF scraping |

---

## 🔍 Détails par Baromètre

### 1. Baromètre de confiance politique & sociale

**Source principale** : CEVIPOF (Centre de recherches politiques de Sciences Po)

**URL** : https://www.cevipof.com/fr/le-barometre-de-la-confiance-politique

**Données disponibles** :
- Enquêtes annuelles sur la confiance dans les institutions
- Datasets historiques (PDF + CSV)
- API si disponible

**Thématiques** :
- Confiance dans les institutions (gouvernement, parlement, justice, médias)
- Satisfaction démocratique
- Engagement citoyen

**Format d'ingestion** :
- CSV annuel (résultats agrégés)
- PDF (rapports complets)
- API (si mise à disposition)

**Tables PostgreSQL cibles** :
- `indicateur` (indices de confiance)
- `document` (rapports et analyses)
- `theme` (gouvernance, démocratie)

---

### 2. Baromètre des émotions et du moral

**Sources principales** :
- Kantar Public : "Mood of France"
- Ipsos : Baromètres d'opinion

**URL** :
- https://www.kantar.com/fr/public-sector/social-data-analysis
- https://www.ipsos.com/fr-fr

**Données disponibles** :
- Enquêtes mensuelles/trimestrielles
- Sentiments mesurés : joie, anxiété, colère, espoir, peur
- CSV téléchargeables

**Thématiques** :
- État émotionnel des Français
- Évolution du moral (timeline)
- Corrélation avec événements politiques/sociaux

**Format d'ingestion** :
- CSV (données quantitatives)
- Web scraping (rapports publics)

**Tables PostgreSQL cibles** :
- `emotion` (si table existe dans E2+)
- `indicateur` (scores émotionnels)
- `document` (analyses)

---

### 3. Baromètre environnemental

**Sources principales** :
- ADEME (Agence de la Transition Écologique)
- IFOP pour la transition écologique

**URL** :
- https://www.ademe.fr/expertises/changements-climatiques-energie/consommation/impacts-consommation
- https://www.ifop.com/

**Données disponibles** :
- Enquêtes sur les pratiques écologiques
- Indicateurs de sensibilisation environnementale
- Datasets open data

**Thématiques** :
- Transition écologique
- Sobriété énergétique
- Sensibilisation climat

**Format d'ingestion** :
- CSV (datasets ADEME)
- API (si disponible)
- PDF (rapports)

**Tables PostgreSQL cibles** :
- `indicateur` (scores environnementaux)
- `theme` (écologie, climat)

---

### 4. Baromètre économique et social

**Sources principales** :
- INSEE Conjoncture
- BVA Observatoire social

**URL** :
- https://www.insee.fr/fr/statistiques
- https://www.bva-group.com/

**Données disponibles** :
- Bases de données SQL INSEE
- CSV de conjoncture
- Indicateurs économiques temps réel

**Thématiques** :
- Pouvoir d'achat
- Chômage, emploi
- Inflation
- Conditions de vie

**Format d'ingestion** :
- Base SQL (export INSEE)
- CSV (conjoncture INSEE)
- API INSEE (si disponible)

**Tables PostgreSQL cibles** :
- `indicateur` (indices économiques)
- `territoire` (données par région/département)

---

### 5. Baromètre des médias et de la confiance

**Source principale** : La Croix – Baromètre Kantar sur les médias

**URL** : https://www.la-croix.com/

**Données disponibles** :
- Rapports annuels sur la confiance dans les médias
- Données de perception des fake news
- Web scraping des articles

**Thématiques** :
- Confiance médiatique
- Perception de l'information
- Lutte contre les fake news

**Format d'ingestion** :
- Web scraping (articles La Croix)
- CSV (données complémentaires)

**Tables PostgreSQL cibles** :
- `document` (articles)
- `indicateur` (indices de confiance médiatique)

---

### 6. Baromètre sport & cohésion sociale

**Sources principales** :
- Ministère des Sports
- CNOSF (Comité National Olympique et Sportif Français)
- Paris 2024 (données post-JO)

**URL** :
- https://www.sports.gouv.fr/
- https://cnosf.franceolympique.com/

**Données disponibles** :
- Statistiques de pratique sportive
- Impact des JO sur la cohésion nationale
- CSV / API ministère

**Thématiques** :
- Sport et bien-être
- Fierté nationale post-JO
- Cohésion sociale

**Format d'ingestion** :
- CSV (statistiques ministère)
- API (si disponible)

**Tables PostgreSQL cibles** :
- `indicateur` (scores sportifs)
- `evenement` (événements sportifs)

---

### 7. Baromètre des discriminations et égalité

**Sources principales** :
- Défenseur des Droits
- IFOP

**URL** :
- https://www.defenseurdesdroits.fr/
- https://www.ifop.com/

**Données disponibles** :
- Rapports annuels discriminations
- Données d'enquêtes IFOP
- CSV / API

**Thématiques** :
- Inclusion, diversité
- Égalité femmes-hommes
- Lutte contre les discriminations

**Format d'ingestion** :
- CSV (rapports Défenseur des Droits)
- API (si disponible)

**Tables PostgreSQL cibles** :
- `indicateur` (indices d'égalité)
- `document` (rapports)

---

### 8. Baromètre santé mentale et bien-être

**Source principale** : Santé Publique France – CoviPrev

**URL** : https://www.santepubliquefrance.fr/etudes-et-enquetes/coviprev-une-enquete-pour-suivre-l-evolution-des-comportements-et-de-la-sante-mentale-pendant-l-epidemie-de-covid-19

**Données disponibles** :
- Enquêtes CoviPrev (post-COVID)
- Indicateurs de santé mentale
- CSV datasets

**Thématiques** :
- Stress, anxiété
- Santé mentale post-COVID
- Bien-être général

**Format d'ingestion** :
- CSV (datasets Santé Publique France)

**Tables PostgreSQL cibles** :
- `indicateur` (scores santé mentale)
- `theme` (santé, bien-être)

---

### 9. Baromètre climat social et tensions

**Sources principales** :
- Elabe
- BFMTV Opinion 2024

**URL** :
- https://www.elabe.fr/
- https://www.bfmtv.com/politique/

**Données disponibles** :
- Sondages d'opinion Elabe
- Analyses BFMTV Opinion
- Web scraping articles

**Thématiques** :
- Colère, frustration sociale
- Confiance dans l'avenir
- Tensions sociales

**Format d'ingestion** :
- Web scraping (articles BFMTV)
- CSV (données Elabe si disponibles)

**Tables PostgreSQL cibles** :
- `document` (articles)
- `indicateur` (indices de tension sociale)

---

### 10. Baromètre innovation et IA

**Sources principales** :
- CNIL (Commission Nationale de l'Informatique et des Libertés)
- France IA
- Capgemini Research Institute

**URL** :
- https://www.cnil.fr/
- https://france-ia.fr/
- https://www.capgemini.com/research-institute/

**Données disponibles** :
- Rapports sur l'adoption de l'IA
- Baromètres de confiance numérique
- PDF / API

**Thématiques** :
- Adoption de l'IA en France
- Confiance numérique
- Éthique IA

**Format d'ingestion** :
- PDF (rapports CNIL)
- API (si disponible)
- Web scraping (datasets publics)

**Tables PostgreSQL cibles** :
- `document` (rapports)
- `indicateur` (indices d'adoption IA)

---

## 🎯 Plan d'Implémentation

### Phase E1 (Actuel)
Les 5 sources de base sont implémentées :
1. ✅ Fichier plat CSV (Kaggle)
2. ✅ API (OpenWeatherMap)
3. ✅ Web Scraping (RSS Multi-Sources)
4. ✅ Web Scraping (Multi-Sources éthique)
5. ✅ Big Data (GDELT GKG)

### Phase E2 (Enrichissement)
Implémenter les baromètres en priorité :
1. **Baromètre économique et social** (INSEE) → Base SQL + CSV
2. **Baromètre des émotions** (Kantar/Ipsos) → CSV + scraping
3. **Baromètre santé mentale** (Santé Publique France) → CSV

### Phase E3 (Complément)
Implémenter les baromètres secondaires :
4. **Baromètre environnemental** (ADEME) → API + CSV
5. **Baromètre confiance politique** (CEVIPOF) → CSV/PDF
6. **Baromètre médias** (La Croix/Kantar) → Web Scraping
7. **Baromètre sport** (Ministère Sports) → CSV/API
8. **Baromètre discriminations** (Défenseur des Droits) → CSV/API
9. **Baromètre climat social** (Elabe/BFMTV) → Web Scraping
10. **Baromètre innovation IA** (CNIL/France IA) → PDF/API

---

## 📝 Notes Techniques

### Mapping Format → Type Source E1

- **CSV / Dataset plat** → Source 1 (Fichier plat CSV)
- **Base SQL** → Source 2 (Base de données)
- **API** → Source 3 (API REST)
- **Web Scraping** → Source 4 (Web Scraping)
- **PDF** → Source 4 (Web Scraping avec parsing PDF) ou Source 1 (si converti en CSV)
- **Big Data** → Source 5 (Big Data)

### Tables PostgreSQL Impactées

Pour chaque baromètre, enrichir :
- `indicateur` : Scores/indices mesurés
- `document` : Rapports, articles, analyses
- `theme` : Thématiques couvertes
- `source_indicateur` : Lien source → indicateur
- `evenement` : Événements liés (si applicable)

### RGPD & Éthique

- ✅ Utiliser uniquement données publiques/agrégées
- ✅ Respecter robots.txt pour scraping
- ✅ Anonymiser données individuelles si présentes
- ✅ Documenter sources et droits d'usage

---

## 🔗 Références

- Architecture pipeline : `docs/ARCHITECTURE_PIPELINE_E1.md`
- Implémentations sources : `docs/SOURCES_IMPLEMENTATIONS.md`
- Notebook ingestion : `notebooks/03_ingest_sources.ipynb`
