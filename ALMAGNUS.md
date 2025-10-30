# DataSens - Démarrage rapide pour le jury

## Clone et lancement (2 minutes)

### 1. Cloner le dépôt
```bash
git clone https://github.com/ALMAGNUS/datasens.git
cd datasens
```

### 2. Lancer le stack Docker complet
```bash
docker compose up -d --build
```

### 3. Accéder à Jupyter Lab
**URL :** http://localhost:8888

**Token (si demandé) :**
```bash
docker compose logs app | grep token
```

---

## Accès aux services

- **Jupyter Lab** : http://localhost:8888 (pas de token requis)
- **PostgreSQL** : localhost:5433 (user: `postgres`, pwd: `postgres`, db: `postgres`)
- **MinIO Console** : http://localhost:9003 (user: `minioadmin`, pwd: `minioadmin`)
- **MinIO API** : http://localhost:9002

---

## Arrêter le stack
```bash
docker compose down
```

---

## Notebooks à consulter

**Recommandé pour la démo :**
- `notebooks/datasens_E1_v3/03_ingest_sources.ipynb`

**Setup initial :**
- `notebooks/datasens_E1_v3/01_setup_env.ipynb`

---

## Documentation

- Guide technique complet : `docs/GUIDE_TECHNIQUE_E1.md`
- Runbook démo : `docs/datasens_runbook_demo.md`
- Dictionnaires : `docs/datasens_*.md`

---

## Support

- Dépôt : https://github.com/ALMAGNUS/datasens
- Issues : https://github.com/ALMAGNUS/datasens/issues

