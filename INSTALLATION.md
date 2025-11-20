# 🚀 Installation DataSens ETL Pipeline

## 📋 Prérequis

### Logiciels Requis
- **Docker Desktop**: 4.25+ ([Download](https://www.docker.com/products/docker-desktop))
- **Python**: 3.11+ ([Download](https://www.python.org/downloads/))
- **Git**: 2.40+ ([Download](https://git-scm.com/downloads))

### Système
- **OS**: Windows 10/11, macOS 12+, Ubuntu 20.04+
- **RAM**: 8GB minimum, 16GB recommandé
- **Disk**: 10GB espace libre

---

## ⚡ Installation Rapide (5 minutes)

### 1. Cloner le Repository
```bash
git clone https://github.com/ALMAGNUS/DataSens.git
cd DataSens
```

### 2. Configuration Environnement
```bash
# Copier template configuration
cp .env.example .env

# Éditer .env avec vos credentials
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Modifiez au minimum:**
```bash
POSTGRES_PASSWORD=VotreMotDePasse123!
MINIO_SECRET_KEY=VotreCléSecrète456!
```

### 3. Lancer Infrastructure Docker
```bash
# Démarrer PostgreSQL + MinIO
docker-compose up -d

# Vérifier services actifs
docker ps
```

**Services attendus:**
- `datasens-postgres` (port 5432)
- `datasens-minio` (port 9000)
- `datasens-pgadmin` (port 5050, optionnel)

### 4. Installer Dépendances Python
```bash
# Créer environnement virtuel
python -m venv .venv

# Activer
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Installer package en mode éditable
pip install -e .

# Installer modèle SpaCy
python -m spacy download fr_core_news_md
```

### 5. Validation Installation
```bash
# Test import modules
python -c "from datasens.db import get_engine; print('✅ Modules OK')"

# Test connexion PostgreSQL
python -c "from datasens.db import get_engine; e=get_engine(); e.connect(); print('✅ PostgreSQL OK')"

# Test connexion MinIO
python -c "from datasens.storage import MinIOClient; c=MinIOClient(); c.test_connection(); print('✅ MinIO OK')"
```

---

## 📖 Utilisation

### Démarrer Démo
```bash
# Ouvrir VS Code
code .

# Ouvrir notebooks dans l'ordre:
# 1. notebooks/datasens_E1_v3/01_setup_env.ipynb
# 2. notebooks/datasens_E1_v3/02_schema_create.ipynb
# 3. notebooks/datasens_E1_v3/03_ingest_sources.ipynb
# 4. notebooks/datasens_E1_v3/04_crud_tests.ipynb
# 5. notebooks/datasens_E1_v3/05_snapshot_and_readme.ipynb
```

**Lire guide démo:** `README_DEMO.md`

---

## 🔧 Configuration Détaillée

### PostgreSQL
```yaml
# docker-compose.yml déjà configuré
Service: datasens-postgres
Port: 5432
Database: datasens
User: datasens_user (configurable via .env)
```

**Accès PgAdmin:**
```
URL: http://localhost:5050
Email: admin@datasens.local
Password: admin
```

### MinIO S3
```yaml
Service: datasens-minio
API Port: 9000
Console Port: 9001
Bucket: datasens-raw (créé automatiquement)
```

**Accès Console:**
```
URL: http://localhost:9001
Access Key: admin (via .env)
Secret Key: (via .env)
```

---

## 📊 Architecture

```
DataSens/
├── datasens/                      # Modules Python refactorisés
│   ├── collectors/                # 5 collecteurs data
│   │   ├── kaggle.py
│   │   ├── rss.py
│   │   ├── owm.py
│   │   ├── webscraping.py
│   │   └── gdelt.py              # BigData
│   ├── annotation/               # ML annotations
│   │   ├── spacy_annotator.py   # NER
│   │   └── yake_annotator.py    # Keywords
│   ├── config.py                 # Configuration centralisée
│   ├── db.py                     # PostgreSQL + pooling
│   ├── storage.py                # MinIO S3 + logging
│   ├── retry.py                  # Exponential backoff
│   └── cache.py                  # Deduplication
├── notebooks/datasens_E1_v3/     # 5 notebooks démo
├── docs/                         # Documentation technique
├── docker-compose.yml            # Infrastructure
├── requirements.txt              # Dépendances Python
└── README_DEMO.md               # Guide démonstration
```

---

## 🐛 Dépannage

### Docker ne démarre pas
```bash
# Vérifier Docker Desktop actif
docker version

# Redémarrer services
docker-compose down
docker-compose up -d

# Logs si erreur
docker-compose logs postgres
docker-compose logs minio
```

### Python import error
```bash
# Réinstaller en mode éditable
pip install -e .

# Vérifier virtual env actif
which python  # Linux/macOS
gcm python    # Windows PowerShell
```

### SpaCy modèle manquant
```bash
# Télécharger modèle français
python -m spacy download fr_core_news_md

# Vérifier installation
python -c "import spacy; spacy.load('fr_core_news_md'); print('OK')"
```

### MinIO connexion refusée
```bash
# Vérifier service actif
docker ps | grep minio

# Tester manuellement
curl http://localhost:9000/minio/health/live
```

### PostgreSQL connexion refusée
```bash
# Vérifier service actif
docker ps | grep postgres

# Vérifier credentials .env
cat .env | grep POSTGRES
```

---

## 🔐 Sécurité

### Avant Production
1. **Changer passwords** dans `.env`:
   - `POSTGRES_PASSWORD`
   - `MINIO_SECRET_KEY`

2. **Ne jamais commit `.env`**:
   - Déjà dans `.gitignore`
   - Utiliser `.env.example` comme template

3. **Firewall Docker**:
   ```bash
   # Restreindre accès externe (production)
   # Modifier docker-compose.yml:
   # ports: "127.0.0.1:5432:5432"
   ```

---

## 📚 Documentation Complémentaire

- **Guide Technique**: `docs/GUIDE_TECHNIQUE_E1.md`
- **Schéma DB**: `docs/datasens_MPD.sql`
- **Optimisations Phase 3**: `docs/PHASE3_OPTIMISATIONS.md`
- **Guide Démo**: `README_DEMO.md`

---

## 🆘 Support

### Vérification Santé Système
```bash
# Script validation complète
python -c "
from datasens.config import get_db_url, get_minio_config
from datasens.db import get_engine
from datasens.storage import MinIOClient

print('🔍 Test Configuration...')
print(f'   DB URL: {get_db_url()}')
print(f'   MinIO: {get_minio_config()[\"endpoint\"]}')

print('\\n🔍 Test PostgreSQL...')
engine = get_engine()
with engine.connect() as conn:
    result = conn.execute('SELECT version()').scalar()
    print(f'   ✅ PostgreSQL: {result[:50]}...')

print('\\n🔍 Test MinIO...')
minio = MinIOClient()
if minio.test_connection():
    print('   ✅ MinIO: Connected')
else:
    print('   ❌ MinIO: Failed')

print('\\n✅ Système Ready!')
"
```

### Logs Debugging
```bash
# Logs Docker
docker-compose logs -f postgres
docker-compose logs -f minio

# Logs Python (dans notebooks)
# Vérifier: logs/datasens.log
```

---

## ✅ Checklist Post-Installation

- [ ] Docker services actifs (postgres + minio)
- [ ] `.env` configuré avec credentials
- [ ] Virtual env Python actif
- [ ] Package `datasens` installé (`pip install -e .`)
- [ ] SpaCy modèle téléchargé (`fr_core_news_md`)
- [ ] Notebook 01 exécuté avec succès
- [ ] PostgreSQL accessible
- [ ] MinIO accessible
- [ ] Modules `datasens` importables

**Si tous ✅ → Prêt pour démo!** 🚀

Consultez `README_DEMO.md` pour guide présentation.
