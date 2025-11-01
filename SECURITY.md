# 🔒 Politique de Sécurité DataSens

## 🎯 Engagement Sécurité

DataSens prend la sécurité au sérieux. Ce document décrit les bonnes pratiques de sécurité implémentées dans le projet.

---

## ✅ Mesures de Sécurité Implémentées

### 1. Protection contre les Injections SQL

**Principe** : Toujours utiliser des requêtes paramétrées, jamais de concaténation.

#### ✅ Code Sécurisé (utilisé dans le projet)

```python
from sqlalchemy import text

# ✅ CORRECT : Requête paramétrée
conn.execute(text("SELECT * FROM t04_document WHERE id_doc = :id"), {"id": 123})

# ✅ CORRECT : Validation whitelist pour identifiants
def assert_valid_identifier(name: str):
    if not name.replace('_', '').isalnum():
        raise ValueError(f"Invalid identifier: {name}")

whitelist_tables = load_whitelist_from_information_schema(conn)
table_name = "t04_document"
assert_valid_identifier(table_name)
if table_name not in whitelist_tables:
    raise ValueError(f"Table {table_name} not in whitelist")
```

#### ❌ À Éviter (NE PAS faire)

```python
# ❌ DANGEREUX : Injection SQL possible
conn.execute(f"SELECT * FROM {table_name} WHERE id = {user_id}")

# ❌ DANGEREUX : Concaténation
conn.execute("SELECT * FROM " + table_name + " WHERE id = " + str(user_id))
```

**Référence** : Tous les notebooks utilisent `text("... :param")` avec dictionnaires de paramètres.

---

### 2. Gestion des Secrets

#### ✅ Bonnes Pratiques

- **`.env`** : Fichier ignoré par Git (dans `.gitignore`)
- **`.env.example`** : Template versionné (sans secrets réels)
- **API Keys** : Stockées dans `.env`, jamais hardcodées dans le code
- **Passwords** : Variables d'environnement uniquement

#### Structure Recommandée

```
.env              # ❌ NE JAMAIS COMMITER (ignoré)
.env.example      # ✅ Template versionné (sans secrets)
```

**Vérification** :
```bash
# S'assurer que .env n'est pas tracké
git check-ignore .env  # Doit retourner: .env
```

---

### 3. Validation des Entrées

#### Whitelist pour Identifiants

Tous les noms de tables/colonnes dynamiques sont validés :

```python
def assert_valid_identifier(name: str):
    """Valide qu'un identifiant est sûr (alphanum + underscore uniquement)"""
    if not isinstance(name, str):
        raise ValueError("Identifier must be a string")
    if not name.replace('_', '').isalnum():
        raise ValueError(f"Invalid identifier: {name}")
```

#### Validation des Types

```python
# Validation des types PostgreSQL
if not isinstance(pg_port, int) or pg_port < 1 or pg_port > 65535:
    raise ValueError("Invalid port number")
```

---

### 4. Logging et Audit

#### ✅ Logs Structurés

- **Logs d'opérations** : `logs/collecte_*.log` (traçabilité complète)
- **Logs d'erreurs** : `logs/errors_*.log` (sans informations sensibles)
- **Manifests JSON** : Métadonnées de collecte (hash fingerprints, pas de secrets)

#### ⚠️ Précautions

- **Ne pas logger** : Mots de passe, clés API, tokens
- **Logger** : Timestamps, opérations, erreurs (sans stacktrace avec secrets)

---

### 5. Conteneurisation Docker

#### ✅ Sécurité Docker

- **Image officielle** : `python:3.10-slim` (minimal, régulièrement mise à jour)
- **Pas de root** : Utilisateur non-privilégié (option `--allow-root` pour Jupyter uniquement)
- **Volumes** : Isolation des données sensibles
- **Réseau** : Services isolés dans `docker-compose`

---

## 🔍 Audit de Sécurité

### Checklist Pré-Commit

- [ ] Aucun mot de passe en dur dans le code
- [ ] `.env` dans `.gitignore`
- [ ] `.env.example` versionné (sans secrets)
- [ ] Requêtes SQL paramétrées uniquement
- [ ] Validation des entrées utilisateur
- [ ] Pas de tokens/clés dans les logs

### Vérification Automatique

Le workflow CI/CD vérifie :
- Lint (Ruff) : Détection de patterns dangereux
- Build Docker : Test de l'image
- `.env.example` : Présence du template

---

## 🐛 Signaler une Vulnérabilité

Si vous découvrez une vulnérabilité de sécurité :

1. **Ne pas ouvrir d'issue publique** immédiatement
2. Contacter directement : `aljaffre@icloud.com`
3. Décrire la vulnérabilité de manière détaillée
4. Proposer une solution si possible

**Réponse** : Engagement de réponse sous 48h.

---

## 📚 Ressources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection Prevention](https://owasp.org/www-community/attacks/SQL_Injection)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security-warnings.html)

---

**Dernière mise à jour** : 2025-01-30  
**Version** : 1.0

