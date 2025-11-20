# 📦 GUIDE TRANSMISSION - DataSens Project

## 🎯 Méthodes de Transmission

### Option 1: GitHub Repository (Recommandé) ✅

#### Étape 1: Nettoyer le repository
```powershell
# Supprimer fichiers temporaires
git clean -fd
git reset --hard HEAD

# Commit changements
git add .
git commit -m "feat: Phase 2 refactoring + GDELT BigData + ML Annotations"
```

#### Étape 2: Pousser vers GitHub
```powershell
# Si vous avez déjà un remote origin
git push origin main

# Si remote n'existe pas, créer nouveau repo sur github.com puis:
git remote add origin https://github.com/VOTRE_USERNAME/DataSens.git
git branch -M main
git push -u origin main
```

#### Étape 3: Partager URL
```
Donner au client: https://github.com/VOTRE_USERNAME/DataSens
```

---

### Option 2: Archive Docker (Sans GitHub)

#### Étape 1: Créer archive propre
```powershell
# Nettoyer données temporaires
Remove-Item -Recurse -Force data/raw/*.csv, data/silver/*, data/gold/* -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force logs/*.log, artifacts/*.json -ErrorAction SilentlyContinue

# Créer archive ZIP
Compress-Archive -Path . -DestinationPath ../DataSens_Production.zip -Force
```

#### Étape 2: Partager via cloud
- Google Drive / OneDrive / Dropbox
- WeTransfer (jusqu'à 2GB gratuit)
- Email (si < 25MB)

---

### Option 3: Docker Image (Production-Ready)

#### Étape 1: Build image Docker complète
```powershell
# Créer Dockerfile production
docker build -t datasens:production -f Dockerfile.prod .

# Sauvegarder image
docker save datasens:production -o datasens_production.tar

# Compresser
gzip datasens_production.tar
```

#### Étape 2: Partager fichier .tar.gz
```
Fichier: datasens_production.tar.gz
Taille: ~500MB-1GB
Client peut charger avec: docker load -i datasens_production.tar.gz
```

---

## 🧹 Checklist Nettoyage Avant Transmission

### Fichiers à Supprimer
```powershell
# Supprimer fichiers dev/debug
Remove-Item check_columns.py -ErrorAction SilentlyContinue
Remove-Item -Recurse docs/logs/ -ErrorAction SilentlyContinue
Remove-Item -Recurse notebooks/datasens_E1_v3/data/ -ErrorAction SilentlyContinue
Remove-Item -Recurse notebooks/datasens_E1_v3/logs/ -ErrorAction SilentlyContinue
```

### Fichiers à Garder
```
✅ README.md (documentation principale)
✅ README_DEMO.md (guide démonstration)
✅ requirements.txt (dépendances Python)
✅ docker-compose.yml (infrastructure)
✅ pyproject.toml (configuration projet)
✅ .env.example (template configuration)
✅ datasens/ (modules refactorisés)
✅ notebooks/datasens_E1_v3/ (5 notebooks démo)
✅ docs/PHASE3_OPTIMISATIONS.md
✅ docs/GUIDE_TECHNIQUE_E1.md
✅ docs/datasens_MPD.sql (schéma DB)
```

### Dossiers Structure (vides OK)
```
✅ data/raw/.gitkeep
✅ data/silver/.gitkeep
✅ data/gold/.gitkeep
✅ data/dataset/.gitkeep
✅ logs/.gitkeep
✅ artifacts/.gitkeep
```

---

## 📋 Fichiers de Configuration Requis

### 1. `.env.example` (template)
```bash
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=datasens_user
POSTGRES_PASSWORD=CHANGE_ME
POSTGRES_DB=datasens

# MinIO Configuration
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=CHANGE_ME
MINIO_BUCKET=datasens-raw

# API Keys (optional)
OWM_API_KEY=your_openweathermap_key
NEWSAPI_KEY=your_newsapi_key
```

### 2. `INSTALLATION.md`
```markdown
# Installation DataSens

## Prérequis
- Docker Desktop 4.25+
- Python 3.11+
- Git 2.40+

## Installation Rapide
1. Clone repository: `git clone <URL>`
2. Copy `.env.example` to `.env`
3. Update credentials in `.env`
4. Launch: `docker-compose up -d`
5. Install Python deps: `pip install -e .`
6. Open notebooks: `notebooks/datasens_E1_v3/`

## Validation
Run notebook `01_setup_env.ipynb` to verify connections.
```

---

## 🚀 Commandes de Transmission

### Méthode Rapide: Git Push
```powershell
# Nettoyage + Commit + Push (3 commandes)
git add .
git commit -m "feat: Production-ready DataSens ETL Pipeline"
git push origin main

# Partager URL: https://github.com/VOTRE_USERNAME/DataSens
```

### Méthode Archive ZIP
```powershell
# Créer archive propre (exclut .git, __pycache__, etc.)
$exclude = @('*.pyc', '__pycache__', '.git', '.venv', 'data/raw/*.csv')
Compress-Archive -Path @(
    'datasens',
    'notebooks/datasens_E1_v3',
    'docs',
    'docker-compose.yml',
    'requirements.txt',
    'pyproject.toml',
    'README.md',
    'README_DEMO.md',
    '.env.example'
) -DestinationPath ../DataSens_Production.zip -Force
```

---

## 📧 Message de Transmission

### Email Template
```
Objet: DataSens ETL Pipeline - Livraison Production

Bonjour,

Voici le projet DataSens ETL Pipeline finalisé.

🔗 GitHub Repository: https://github.com/USERNAME/DataSens
📖 Documentation: README.md + README_DEMO.md
🚀 Quick Start: docker-compose up -d

Architecture:
- 5 collectors (Kaggle, RSS, OWM, WebScraping, GDELT)
- 2 annotators (SpaCy NER, YAKE Keywords)
- PostgreSQL (36 tables Medallion)
- MinIO S3-compatible storage
- Phase 3 optimizations (retry, pooling, cache)

Demo:
- Notebooks: datasens_E1_v3/ (01 → 05)
- Guide: README_DEMO.md
- Duration: 25 minutes

Credentials:
- PostgreSQL: datasens_user / voir .env
- MinIO: admin / voir .env
- Config: .env.example à copier en .env

Support:
- Documentation: docs/GUIDE_TECHNIQUE_E1.md
- Schema DB: docs/datasens_MPD.sql
- Optimisations: docs/PHASE3_OPTIMISATIONS.md

Cordialement,
```

---

## ✅ Validation Finale

### Test Avant Transmission
```powershell
# 1. Vérifier structure
tree /F datasens
tree /F notebooks/datasens_E1_v3

# 2. Vérifier dépendances
pip install -e .
python -c "import datasens; print('OK')"

# 3. Vérifier Docker
docker-compose up -d
docker ps  # Voir postgres + minio

# 4. Tester notebook
# Ouvrir 01_setup_env.ipynb → Exécuter cellules 1-3
```

### Checklist
- [ ] .env.example présent (pas de credentials hardcodés)
- [ ] README.md à jour avec instructions
- [ ] README_DEMO.md présent
- [ ] requirements.txt complet
- [ ] docker-compose.yml fonctionnel
- [ ] Notebooks exécutables (pas d'erreurs)
- [ ] Module datasens importable
- [ ] Documentation technique présente
- [ ] Pas de fichiers sensibles (.env, logs, data)
- [ ] .gitignore configuré

---

## 🎯 Recommandation Finale

**GitHub (Option 1)** = Meilleur choix:
- Version control
- Collaboration facile
- Clone en 1 commande
- Issues/PRs disponibles
- CI/CD intégrable

**Commandes finales:**
```powershell
git add .
git commit -m "feat: DataSens Production Ready - Phase 2 Complete"
git push origin main
```

**Partager:** `https://github.com/VOTRE_USERNAME/DataSens`

Le client peut cloner en 1 commande:
```bash
git clone https://github.com/VOTRE_USERNAME/DataSens.git
cd DataSens
cp .env.example .env
# Modifier .env avec credentials
docker-compose up -d
pip install -e .
```

✅ **Ready for Production!**
