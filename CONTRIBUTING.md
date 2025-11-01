# 🤝 Guide de Contribution DataSens

Merci de votre intérêt pour contribuer à DataSens ! Ce guide vous aidera à comprendre comment contribuer efficacement.

---

## 📋 Table des Matières

1. [Code de Conduite](#code-de-conduite)
2. [Processus de Contribution](#processus-de-contribution)
3. [Standards de Code](#standards-de-code)
4. [Structure du Projet](#structure-du-projet)
5. [Tests](#tests)

---

## 📜 Code de Conduite

### Nos Valeurs

- **Respect** : Traiter tous les contributeurs avec respect et bienveillance
- **Collaboration** : Construire ensemble un projet de qualité
- **Excellence** : Viser la meilleure qualité technique possible
- **Transparence** : Code et documentation clairs et accessibles

---

## 🔄 Processus de Contribution

### 1. Fork et Clone

```bash
# Fork le projet sur GitHub
# Puis clonez votre fork
git clone https://github.com/VOTRE_USERNAME/datasens.git
cd datasens
```

### 2. Créer une Branche

```bash
# Créer une branche pour votre feature/fix
git checkout -b feature/ma-nouvelle-feature
# ou
git checkout -b fix/correction-bug
```

### 3. Développer

- **Suivre les standards de code** (voir ci-dessous)
- **Documenter** votre code (commentaires en français)
- **Tester** vos modifications

### 4. Commit

```bash
# Messages de commit clairs et descriptifs
git commit -m "feat: Ajout collecte source X"
git commit -m "fix: Correction bug déduplication"
git commit -m "docs: Amélioration README"
```

**Format des messages** : `type: description courte`

Types :
- `feat` : Nouvelle fonctionnalité
- `fix` : Correction de bug
- `docs` : Documentation
- `refactor` : Refactorisation
- `test` : Tests
- `chore` : Maintenance

### 5. Push et Pull Request

```bash
git push origin feature/ma-nouvelle-feature
```

Puis créer une Pull Request sur GitHub avec :
- **Description claire** de ce qui change
- **Screenshots** si changement visuel
- **Référence** à une issue si applicable

---

## 📐 Standards de Code

### Python

- **Style** : PEP 8
- **Linter** : Ruff (configuré dans `pyproject.toml`)
- **Commentaires** : En français, clairs et utiles
- **Docstrings** : Pour fonctions complexes

### Notebooks Jupyter

- **Structure** : Cellules markdown explicatives avant code
- **Sorties** : Garder seulement les sorties utiles
- **Nettoyage** : Pas de cellules vides en fin de notebook
- **Ordre** : Suivre la séquence 01 → 02 → 03 → 04 → 05

### SQL

- **Requêtes paramétrées** : Toujours utiliser `text("... :param")` avec dict
- **Noms de tables** : Préfixe `tXX_` pour E1_v3 (ex: `t04_document`)
- **Sécurité** : Validation whitelist pour identifiants dynamiques
  - Utiliser `assert_valid_identifier()` avant utilisation de noms dynamiques
  - Utiliser `load_whitelist_tables()` pour valider contre `information_schema`
  - **JAMAIS** de f-strings/concaténation pour valeurs utilisateur
  - Voir [SECURITY.md](SECURITY.md) pour détails complets

---

## 🏗️ Structure du Projet

```
DataSens/
├── notebooks/          # Notebooks Jupyter par version
│   └── datasens_E1_v3/
├── docs/              # Documentation technique
├── config/            # Configuration flexible (JSON)
├── data/              # Données (raw, silver, gold)
├── logs/              # Logs d'exécution
├── scripts/           # Scripts utilitaires (optionnel)
├── .github/workflows/ # CI/CD
├── README.md          # Point d'entrée
├── LICENSE            # MIT
└── requirements.txt   # Dépendances Python
```

### Où Ajouter du Code ?

- **Nouvelle source** : `notebooks/datasens_E1_v3/03_ingest_sources.ipynb`
- **Nouvelle table** : `docs/datasens_MPD.sql` + `02_schema_create.ipynb`
- **Nouvelle visualisation** : Notebooks concernés (section visualisations)
- **Documentation** : `docs/` avec nom explicite

---

## 🧪 Tests

### Tests Manuels

1. **Exécuter les notebooks** dans l'ordre 01 → 05
2. **Vérifier les visualisations** s'affichent
3. **Contrôler les logs** (`logs/`) pour erreurs
4. **Vérifier PostgreSQL** : Données insérées correctement
5. **Vérifier MinIO** : Objets stockés

### Tests Automatisés (CI/CD)

Le workflow GitHub Actions vérifie :
- Lint (Ruff) : Qualité du code
- Build Docker : Image buildable
- Structure : Fichiers essentiels présents

---

## 📝 Documentation

### Exigences

- **README.md** : Mis à jour si changement majeur
- **Guide Technique** : Mettre à jour si nouvelle fonctionnalité
- **CHANGELOG.md** : Ajouter entrée pour chaque changement notable
- **Commentaires** : Code auto-documenté

### Format

- **Markdown** : Pour documentation
- **Français** : Langue principale
- **Exemples** : Code snippets concrets
- **Liens** : Références croisées

---

## ✅ Checklist Pré-PR

Avant de soumettre une Pull Request :

- [ ] Code suit les standards (PEP 8, Ruff)
- [ ] Notebooks exécutables sans erreur
- [ ] Documentation à jour (README, Guide)
- [ ] Tests manuels passés
- [ ] Pas de secrets dans le code
- [ ] `.env.example` mis à jour si nouvelles variables
- [ ] CHANGELOG.md mis à jour
- [ ] Commit messages clairs

---

## 🎯 Types de Contributions Sought

### Priorités

1. **Nouvelles sources** : Ajout de collecteurs de données
2. **Amélioration visualisations** : Graphiques plus clairs
3. **Documentation** : Clarification, exemples supplémentaires
4. **Tests** : Tests unitaires pour fonctions utilitaires
5. **Performance** : Optimisations du pipeline ETL

### Idées Futures (E2/E3)

- Annotation IA avancée (CamemBERT, FlauBERT)
- Dashboards interactifs (Streamlit, Grafana)
- Orchestration (Prefect flows)
- Monitoring (Prometheus, logs structurés)

---

## 💬 Questions ?

- **Issues** : Pour questions, bugs, feature requests
- **Discussions** : Pour discussions générales
- **Email** : `aljaffre@icloud.com` (questions directes)

---

**Merci de contribuer à DataSens ! 🚀**

