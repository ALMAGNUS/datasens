# 🎯 GUIDE DÉMO TECHNIQUE - DataSens ETL Pipeline

## ⚡ Démarrage Infrastructure (2 min)

### 1. Lancer l'infrastructure
```powershell
cd "C:\Users\Utilisateur\Desktop\DEV IA 2025\DataSens"
docker-compose up -d
```

### 2. Ouvrir le notebook principal
```
📂 Ouvrir: notebooks/datasens_E1_v3/03_ingest_sources.ipynb
```

## 🎬 Scénario de Démo Complet (25 minutes)

### Introduction (2 min)
Présenter l'architecture refactorisée:
```
DataSens/
├── datasens/              ← Modules refactorisés Phase 2
│   ├── collectors/        ← 5 collecteurs (Kaggle, RSS, OWM, WebScraping, GDELT)
│   ├── annotation/        ← SpaCy NER + YAKE Keywords
│   ├── db.py              ← PostgreSQL + Connection Pooling
│   ├── storage.py         ← MinIO S3-compatible + Logging
│   ├── retry.py           ← Exponential backoff
│   └── cache.py           ← Déduplication in-memory
└── notebooks/datasens_E1_v3/  ← 5 Notebooks progression
    ├── 01_setup_env.ipynb         ← Infrastructure setup
    ├── 02_schema_create.ipynb     ← Schema DDL (36 tables)
    ├── 03_ingest_sources.ipynb    ← ETL Pipeline ⭐
    ├── 04_crud_tests.ipynb        ← Unit tests
    └── 05_snapshot_and_readme.ipynb ← Documentation
```

### Notebook 1: `01_setup_env.ipynb` (2 min)

**Objectif**: Validation environnement technique

**Exécuter cellules 1-3:**
```
✅ Python 3.11+
✅ Dependencies (pandas, sqlalchemy, minio, spacy, yake)
✅ Environment variables (.env)
✅ PostgreSQL connection
✅ MinIO S3 connection
```

**Points techniques:**
- Configuration centralisée `.env`
- Health checks automatisés
- Dependency validation

### Notebook 2: `02_schema_create.ipynb` (3 min)

**Objectif**: DDL PostgreSQL avec architecture Medallion

**Exécuter cellules principales:**
```
✅ Schema datasens created
✅ 36 tables (t01-t37) with foreign keys
✅ Indexes on hash_fingerprint, date_publication
✅ Medallion architecture (RAW → SILVER → GOLD)
```

**Points techniques:**
- Normalized schema (3NF)
- Referential integrity constraints
- Optimized indexes for queries

### Notebook 3: `03_ingest_sources.ipynb` ⭐ PRINCIPAL (12 min)

**Objectif**: Pipeline ETL complet avec collecte multi-sources

#### Partie A: Sources Classiques (7 min)

**Exécuter cellules 1-25:**
- ✅ Configuration chargée (PostgreSQL + MinIO)
- ✅ Collecte RSS (Franceinfo, 20 Minutes, Le Monde)
- ✅ Collecte météo OpenWeatherMap
- ✅ Upload MinIO + Insertion PostgreSQL

**Points techniques:**
- Modules réutilisables avec retry mechanism
- Structured logging (taille, durée, status)
- Exponential backoff (1s → 2s → 4s)

#### Partie B: BigData + ML (5 min)

**Exécuter nouvelles cellules fin de notebook:**

1. **Collecte GDELT:**
   - Download ZIP from GDELT GKG API
   - Parse 28 colonnes métadonnées
   - Insert PostgreSQL + Upload MinIO

2. **SpaCy NER:**
   - Modèle fr_core_news_md
   - Extract PER, LOC, ORG entities
   - 3 colonnes ajoutées au DataFrame

3. **YAKE Keywords:**
   - Unsupervised extraction (n-grams 1-3)
   - Top 5 keywords per document
   - Deduplication threshold 0.9

4. **Visualisations:** ⭐
   - Bar/Pie chart: Distribution entités NER
   - Horizontal bar: Top 15 keywords YAKE
   - Stacked bar + Table: Matrice annotations complète

5. **Upload MinIO:**
   - Dataset annoté (CSV format)
   - URI s3://datasens-raw/demo/

**Points techniques:**
- GDELT = Global Event Database (15min frequency)
- SpaCy = Production-ready NER (French model)
- YAKE = Statistical keyword extraction
- Dataset AI-ready pour ML/DL downstream tasks

### Notebook 4: `04_crud_tests.ipynb` (3 min)

**Objectif**: Unit tests opérations CRUD

**Exécuter cellules clés:**
- ✅ CREATE: Insert test data
- ✅ READ: SELECT queries validation
- ✅ UPDATE: Modify records
- ✅ DELETE: Remove records

**Points techniques:**
- Data integrity validation
- Schema constraints verification
- Referential integrity tests

### Notebook 5: `05_snapshot_and_readme.ipynb` (3 min)

**Objectif**: Auto-documentation et versioning

**Exécuter cellules:**
- ✅ README.md auto-generated
- ✅ Database snapshot (tables + row counts)
- ✅ Global statistics export
- ✅ Metadata manifest (JSON)

**Points techniques:**
- Automated documentation pipeline
- State versioning (git-compatible)
- Metadata traceability

## 🎓 Messages Clés pour le Professeur

### 1. Architecture Refactorisée ✅
"Nous avons refactorisé le code monolithique en modules réutilisables. Les notebooks appellent maintenant `datasens.collectors`, `datasens.annotation`, etc."

### 2. Optimisations Phase 3 ⚡
"Nous avons implémenté 3 optimisations majeures:
- **Retry** avec exponential backoff (résilience réseau)
- **Connection Pooling** PostgreSQL (5+10 connexions)
- **Cache** déduplication in-memory (10k hash)"

### 3. BigData GDELT 🌍
"GDELT publie des fichiers toutes les 15 minutes avec des millions d'événements mondiaux. Notre collecteur télécharge, parse et stocke ces données massives."

### 4. Annotations ML 🔍
"Nous préparons des datasets AI-ready avec:
- **SpaCy**: Extraction d'entités (NER français)
- **YAKE**: Extraction de mots-clés
Le dataset annoté est prêt pour du ML/DL (sentiment, classification, etc.)"

### 5. Production Ready 🚀
"Notre pipeline est production-ready:
- Logging structuré (taille, durée, erreurs)
- Test de connexion MinIO
- Gestion d'erreurs avec retry
- Storage hybride (PostgreSQL + MinIO S3)"

## 📋 Si Questions Techniques

**Q: "Pourquoi refactoriser en modules?"**
→ "Code reusability, testability, maintainability. Single Responsibility Principle: 1 collector = 1 module. Easier debugging and horizontal scaling."

**Q: "Différence avec code monolithique?"**
→ "Avant: 5000 lignes notebook monolithique. Maintenant: notebooks courts + Python packages. DRY principle, proper imports, version control friendly."

**Q: "Pourquoi GDELT?"**
→ "Production-scale BigData validation: millions de records, 15min frequency, 28 metadata columns. Demonstrates pipeline capacity for real-world volumes."

**Q: "Purpose des annotations?"**
→ "Generate AI-ready datasets for downstream ML tasks: sentiment analysis, topic classification, entity linking. SpaCy NER + YAKE keywords = feature engineering automation."

**Q: "Scalability approach?"**
→ "Retry mechanism = network resilience. Connection pooling = concurrency. MinIO S3 = horizontal storage scaling. In-memory cache = performance optimization. Architecture supports distributed processing (future: Spark/Dask)."

## ✅ Checklist Avant Démo

- [ ] Docker Compose lancé: `docker ps` (voir postgres + minio)
- [ ] Virtual env activé: `(.venv)` visible dans terminal
- [ ] SpaCy installé: `python -m spacy download fr_core_news_md`
- [ ] Tous les notebooks dans `datasens_E1_v3/` ouverts en onglets
- [ ] Ordre des onglets: 01 → 02 → 03 → 04 → 05
- [ ] Notebook 01 cellules 1-3 pré-exécutées (gain de temps)
- [ ] Notebook 02 cellules schema pré-exécutées (gain de temps)

## 🎬 Script de Démo Détaillé

### Minute 0-2: Notebook 01 (Setup)
```
"Je vais vous montrer notre pipeline DataSens en 5 étapes.
D'abord, on vérifie que l'infrastructure Docker est opérationnelle."

[Exécuter cellules 1-3]

"✅ PostgreSQL connecté, MinIO connecté, toutes les dépendances sont OK.
Notre configuration est centralisée dans .env."
```

### Minute 2-5: Notebook 02 (Schema)
```
"Maintenant, créons le schéma PostgreSQL complet."

[Exécuter cellules création tables]

"✅ 36 tables créées selon notre MCD/MPD documenté.
Architecture Medallion: RAW → SILVER → GOLD."
```

### Minute 5-17: Notebook 03 (Ingest) ⭐ STAR
```
"C'est le cœur du pipeline: la collecte multi-sources."

[Exécuter cellules configuration]
"Configuration chargée depuis nos modules refactorisés."

[Exécuter cellules RSS]
"✅ Collecte RSS: Franceinfo, 20 Minutes, Le Monde.
Données uploadées vers MinIO, insérées dans PostgreSQL.
Remarquez le retry automatique et le logging structuré."

[Exécuter cellules GDELT]
"🌍 GDELT BigData: fichiers mondiaux toutes les 15 minutes.
50 événements téléchargés, parsés, stockés."

[Exécuter cellules SpaCy]
"🔍 Annotations SpaCy NER: extraction automatique des entités.
Personnes, lieux, organisations identifiés."

[Exécuter cellules YAKE]
"🔑 YAKE: extraction mots-clés unsupervised.
Dataset maintenant AI-ready pour ML/DL."

[Exécuter cellules statistiques]
"📊 Résultats: X événements, Y entités, Z mots-clés.
Tout est dans PostgreSQL + MinIO."
```

### Minute 17-20: Notebook 04 (CRUD)
```
"Tests unitaires pour valider l'intégrité."

[Exécuter 2-3 cellules CRUD]

"✅ CREATE, READ, UPDATE, DELETE fonctionnent.
Contraintes respectées."
```

### Minute 20-23: Notebook 05 (Snapshot)
```
"Documentation automatique et snapshot final."

[Exécuter cellules génération]

"✅ README généré, métadonnées exportées.
Traçabilité complète pour versioning."
```

### Minute 23-25: Questions
```
"Voilà le pipeline complet de bout en bout.
Questions?"
```

## 🎯 Timing Idéal (25 min)

| Notebook | Durée | Contenu |
|----------|-------|---------|
| **01_setup_env** | 2 min | Vérification environnement |
| **02_schema_create** | 3 min | Création 36 tables PostgreSQL |
| **03_ingest_sources** | 12 min | Pipeline ETL + GDELT + Annotations ⭐ |
| **04_crud_tests** | 3 min | Tests CRUD + validations |
| **05_snapshot_readme** | 3 min | Documentation auto + snapshot |
| **Questions** | 2 min | Réponses + discussion |
| **TOTAL** | **25 min** | |

## 📋 Ordre d'Exécution Démo

### Séquence Recommandée

1. **01_setup_env.ipynb** → Montrer que tout est prêt
2. **02_schema_create.ipynb** → Montrer l'architecture DB
3. **03_ingest_sources.ipynb** → ⭐ DÉMO PRINCIPALE
   - Partie A: Collecte RSS + OWM (sources classiques)
   - Partie B: GDELT + SpaCy + YAKE (BigData + ML)
4. **04_crud_tests.ipynb** → Tests rapides (optionnel si temps limité)
5. **05_snapshot_readme.ipynb** → Documentation finale

### Si Temps Limité (15 min)

Concentrez-vous sur **03_ingest_sources.ipynb**:
- Cellules 1-3: Configuration
- Cellules RSS: Collecte multi-sources
- Cellules GDELT: BigData
- Cellules Annotations: SpaCy + YAKE
- Cellules Statistiques: Résultats finaux

## 🎓 Technical Highlights par Notebook

### 01 - Setup
"Dockerized infrastructure: PostgreSQL 14, MinIO S3-compatible, PgAdmin. Environment variables managed via .env."

### 02 - Schema
"Medallion architecture with 36 normalized tables (3NF). Entity relationships documented in MCD/MPD. Indexes optimized for hash_fingerprint lookups."

### 03 - Ingest ⭐
"Multi-source ETL pipeline with exponential backoff retry, PostgreSQL connection pooling (5+10), in-memory deduplication cache. GDELT BigData + SpaCy/YAKE annotations generate AI-ready datasets."

### 04 - CRUD
"Unit tests validate schema integrity: CREATE, READ, UPDATE, DELETE operations. Foreign key constraints and referential integrity verified."

### 05 - Snapshot
"Automated documentation generation. Database state versioning with JSON manifests. Git-compatible traceability."

## 💡 Presentation Best Practices

### Pre-Demo Setup
1. **Pre-execute notebooks 01-02** (saves 5 minutes)
2. **Keep 5 notebooks as browser tabs** (ordered 01→05)
3. **Dry-run once** to validate timings

### During Demo
1. **Navigate between tabs** to show pipeline progression
2. **Comment while executing** (explain what's happening)
3. **Highlight logs** (structured output: size, duration, status)
4. **Display DataFrames** (visual proof with .head())
5. **Show visualizations** (graphs = concrete evidence)

### High-Impact Moments
- 🌍 **GDELT BigData** → Demonstrates volume capacity
- 🔍 **SpaCy NER** → Shows intelligent processing
- 📊 **Visualizations** → Concrete proof of annotations
- ☁️ **MinIO** → Proves scalable architecture
- � **Statistics** → Quantifiable results

### Technical Issue Handling
- **MinIO disconnected**: "Local fallback active, pipeline continues gracefully"
- **GDELT timeout**: "Worldwide BigData source, adjustable limits for demo"
- **SpaCy slow**: "NER model analyzes every token, expected latency"
- **Visualization error**: "Matplotlib backend issue, data remains valid"

---

🎬 **Demo Ready!** 5 notebooks tell complete story: Infrastructure → Schema → ETL → Tests → Documentation
