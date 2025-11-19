# Comparaison Dépendances Choisies vs Alternatives - DataSens

**Date** : 2025-11-19  
**Objectif** : Justifier les choix technologiques face aux alternatives pour la démo jury

---

## 🎯 Stratégie de Comparaison

Pour chaque dépendance critique, analyser :
1. **Pourquoi ce choix ?**
2. **Alternatives considérées**
3. **Avantages/inconvénients**
4. **Justification technique pour jury**

---

## 🗄️ DataLake : MinIO vs Alternatives

### Choix : MinIO

**Version** : 7.2.16

#### Pourquoi MinIO ?

1. **Compatibilité S3 native** :
   - API S3 standard (AWS S3 compatible)
   - Migration future vers AWS S3 transparente
   - Support outils S3 existants (boto3, etc.)

2. **Léger et performant** :
   - Installation simple (Docker)
   - Faible consommation ressources
   - Parfait pour environnement local/développement

3. **Open Source** :
   - Pas de coût de licence
   - Communauté active
   - Documentation complète

#### Alternatives considérées

| Alternative | Pourquoi non choisi ? | Cas d'usage alternatif |
|-------------|------------------------|------------------------|
| **Apache Cassandra** | Trop complexe pour E1, orienté Big Data distribué | E3 si volume massif (millions de documents) |
| **MongoDB** | Base documentaire, pas optimisé pour objets bruts | Si besoin requêtes complexes sur métadonnées |
| **Hadoop HDFS** | Surdimensionné pour E1, complexité opérationnelle | E3 si traitement Big Data distribué |
| **AWS S3** | Coût, dépendance cloud externe | Production cloud |
| **Azure Blob Storage** | Coût, dépendance cloud externe | Production cloud Azure |

#### Justification pour Jury

> **"MinIO offre le meilleur compromis pour E1 : simplicité d'installation, compatibilité S3 standard, et migration future transparente vers cloud si nécessaire."**

---

## 🗄️ Base de Données : PostgreSQL vs Alternatives

### Choix : PostgreSQL

**Version** : Via psycopg2-binary 2.9.10 + SQLAlchemy 2.0.34

#### Pourquoi PostgreSQL ?

1. **Architecture Merise** :
   - Support relations complexes (FK, contraintes)
   - Schéma structuré (38 tables)
   - Transactions ACID

2. **Maturité et stabilité** :
   - Standard industrie
   - Support JSON natif (flexibilité)
   - Extensions (PostGIS pour géolocalisation)

3. **Performance** :
   - Indexation avancée
   - Optimiseur de requêtes performant
   - Support volumes importants

#### Alternatives considérées

| Alternative | Pourquoi non choisi ? | Cas d'usage alternatif |
|-------------|------------------------|------------------------|
| **MySQL** | Moins de fonctionnalités avancées | Si contraintes de licence |
| **MongoDB** | Pas adapté pour relations Merise complexes | Si données non structurées uniquement |
| **SQLite** | Limité pour production, pas de concurrence | Prototypage rapide |
| **Cassandra** | NoSQL, pas adapté pour relations Merise | Big Data distribué sans relations |
| **Elasticsearch** | Orienté recherche, pas SGBD relationnel | Si besoin recherche full-text uniquement |

#### Justification pour Jury

> **"PostgreSQL est le choix optimal pour implémenter l'architecture Merise (MCD/MLD/MPD) avec 38 tables relationnelles, garantissant intégrité référentielle et performance."**

---

## 📊 Data Processing : pandas vs Alternatives

### Choix : pandas

**Version** : 2.2.2

#### Pourquoi pandas ?

1. **Standard industrie** :
   - Bibliothèque la plus utilisée en Data Science
   - Documentation exhaustive
   - Communauté massive

2. **Performance pandas 2.x** :
   - Support Arrow natif (pyarrow)
   - Copy-on-write (mémoire optimisée)
   - Performance améliorée vs pandas 1.x

3. **Écosystème** :
   - Intégration avec tous les outils (matplotlib, plotly, etc.)
   - Support formats multiples (CSV, Parquet, Excel, etc.)

#### Alternatives considérées

| Alternative | Pourquoi non choisi ? | Cas d'usage alternatif |
|-------------|------------------------|------------------------|
| **Polars** | Plus récent, écosystème moins mature | Si besoin performance extrême |
| **Dask** | Surdimensionné pour E1, complexité | E3 si traitement distribué |
| **Vaex** | Moins de fonctionnalités, communauté réduite | Si datasets très volumineux |
| **Apache Spark** | Surdimensionné pour E1, complexité | E3 si Big Data distribué |

#### Justification pour Jury

> **"pandas 2.x offre le meilleur équilibre : standard industrie, performance optimisée avec Arrow, et écosystème complet pour ETL."**

---

## 🤖 NLP : spaCy vs Alternatives

### Choix : spaCy

**Version** : 3.8.11 + modèle français `fr_core_news_sm 3.8.0`

#### Pourquoi spaCy ?

1. **Performance** :
   - Ultra-rapide (Cython)
   - Optimisé pour production
   - Modèles pré-entraînés français

2. **Fonctionnalités** :
   - NER (Named Entity Recognition) français
   - Tokenisation, lemmatisation
   - Support transformers (intégration FlauBERT/CamemBERT possible)

3. **Maturité** :
   - Standard NLP Python
   - Documentation excellente
   - Communauté active

#### Alternatives considérées

| Alternative | Pourquoi non choisi ? | Cas d'usage alternatif |
|-------------|------------------------|------------------------|
| **NLTK** | Plus lent, moins de fonctionnalités | Recherche académique |
| **Transformers (HuggingFace)** | Plus lourd, nécessite GPU pour performance | E2/E3 si besoin modèles avancés |
| **Stanford NLP** | Java, moins intégré écosystème Python | Recherche académique |
| **spaCy + Transformers** | Combiné pour E2/E3 (FlauBERT/CamemBERT) | Annotation avancée E2/E3 |

#### Justification pour Jury

> **"spaCy est optimal pour E1 : performance, modèle français pré-entraîné, et intégration future avec transformers (FlauBERT/CamemBERT) pour E2/E3."**

---

## 🔑 Extraction Mots-clés : YAKE vs Alternatives

### Choix : YAKE

**Version** : 0.6.0

#### Pourquoi YAKE ?

1. **Non supervisé** :
   - Pas besoin de corpus d'entraînement
   - Fonctionne sur n'importe quel texte
   - Multilingue (français supporté)

2. **Léger et rapide** :
   - Algorithme simple et efficace
   - Pas de dépendances lourdes
   - Performance correcte

3. **Open Source** :
   - Bibliothèque Python pure
   - Facile à intégrer

#### Alternatives considérées

| Alternative | Pourquoi non choisi ? | Cas d'usage alternatif |
|-------------|------------------------|------------------------|
| **RAKE** | Moins performant, moins maintenu | Si besoin simplicité maximale |
| **KeyBERT** | Nécessite modèles transformers (lourd) | E2/E3 si besoin sémantique avancée |
| **TextRank** | Moins performant que YAKE | Recherche académique |
| **TF-IDF** | Basique, moins de fonctionnalités | Si besoin contrôle total |
| **Keyphrase Extraction (Transformers)** | Nécessite GPU, plus lourd | E2/E3 si performance maximale |

#### Justification pour Jury

> **"YAKE offre le meilleur compromis pour E1 : extraction non supervisée, léger, performant, et multilingue (français). Alternative KeyBERT pour E2/E3 si besoin sémantique avancée."**

---

## 🔄 Orchestration : Prefect vs Alternatives

### Choix : Prefect

**Version** : 3.4.19

#### Pourquoi Prefect ?

1. **Moderne et Python-native** :
   - API Python pure
   - Décorateurs simples
   - Intégration facile

2. **Cloud-native** :
   - Prefect Cloud (optionnel)
   - Dashboard intégré
   - Monitoring avancé

3. **Flexible** :
   - Local ou cloud
   - Support async
   - Gestion erreurs robuste

#### Alternatives considérées

| Alternative | Pourquoi non choisi ? | Cas d'usage alternatif |
|-------------|------------------------|------------------------|
| **Airflow** | Plus complexe, surdimensionné pour E1 | Production entreprise |
| **Luigi** | Moins moderne, communauté réduite | Legacy |
| **Dagster** | Plus récent, écosystème moins mature | Si besoin data lineage avancé |
| **Apache NiFi** | Java, complexité opérationnelle | Big Data entreprise |
| **Temporal** | Plus orienté workflows distribués | Microservices complexes |

#### Justification pour Jury

> **"Prefect 3.x offre la meilleure expérience développeur pour E1 : API Python moderne, dashboard intégré, et migration cloud future transparente."**

---

## 📈 Visualisation : matplotlib + plotly vs Alternatives

### Choix : matplotlib + plotly

**Versions** : matplotlib 3.9.2, plotly 5.24.1

#### Pourquoi ce duo ?

1. **matplotlib** :
   - Standard industrie
   - Visualisations statiques (PNG pour docs)
   - Intégration pandas native

2. **plotly** :
   - Visualisations interactives
   - Support Jupyter
   - Export HTML/Dash possible

#### Alternatives considérées

| Alternative | Pourquoi non choisi ? | Cas d'usage alternatif |
|-------------|------------------------|------------------------|
| **Seaborn** | Basé sur matplotlib, redondant | Si besoin statistiques avancées |
| **Bokeh** | Moins intégré écosystème | Dashboards web complexes |
| **Altair** | Moins de fonctionnalités | Visualisations déclaratives |
| **D3.js** | JavaScript, moins intégré Python | Dashboards web custom |

#### Justification pour Jury

> **"matplotlib + plotly : complémentarité parfaite - matplotlib pour docs statiques, plotly pour interactivité et démo live."**

---

## 🎯 Synthèse Comparative

### Critères de Choix Globaux

1. **Simplicité** : Facile à installer et utiliser (E1)
2. **Performance** : Optimisé pour volumes E1
3. **Standard** : Bibliothèques reconnues industrie
4. **Évolutivité** : Migration future possible (E2/E3)
5. **Documentation** : Documentation complète pour jury

### Matrice de Décision

| Dépendance | Critère Principal | Alternative si... |
|------------|-------------------|-------------------|
| **MinIO** | Simplicité + Compatibilité S3 | Volume massif → Cassandra |
| **PostgreSQL** | Relations Merise | Données non structurées → MongoDB |
| **pandas** | Standard + Performance | Big Data distribué → Spark |
| **spaCy** | Performance + Modèle FR | Besoin sémantique → Transformers |
| **YAKE** | Non supervisé + Léger | Besoin sémantique → KeyBERT |
| **Prefect** | Simplicité + Python | Production entreprise → Airflow |

---

## 📊 Tableau Récapitulatif Jury

| Composant | Choix | Alternative Principale | Justification |
|-----------|-------|------------------------|---------------|
| **DataLake** | MinIO | Cassandra | Simplicité + Compatibilité S3 |
| **SGBD** | PostgreSQL | MongoDB | Relations Merise (38 tables) |
| **ETL** | pandas 2.x | Spark | Standard + Performance |
| **NLP** | spaCy | Transformers | Performance + Modèle FR |
| **Mots-clés** | YAKE | KeyBERT | Non supervisé + Léger |
| **Orchestration** | Prefect 3.x | Airflow | Simplicité + Python |

---

## 🎯 Messages Clés pour Jury

1. **Choix justifiés** : Chaque dépendance répond à un besoin spécifique E1
2. **Évolutivité** : Architecture permet migration vers alternatives si besoin E2/E3
3. **Standards** : Bibliothèques reconnues industrie (meilleure pratique)
4. **Performance** : Optimisé pour volumes E1, scalable pour E2/E3

---

**Dernière mise à jour** : 2025-11-19

