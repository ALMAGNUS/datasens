# 🔧 Améliorations v1/v2 basées sur v3

**Date** : 2025-11-01  
**Objectif** : Appliquer les meilleures pratiques de v3 aux versions v1 et v2

---

## ✅ Améliorations Prioritaires

### 1. **Sécurité SQL (Priorité 1)**

#### v2 : `notebooks/datasens_E1_v2/03_ingest_sources.ipynb`

**Ajouter dans la section "Fonctions utilitaires" (après `insert_documents`) :**

```python
# =====================================================
# FONCTIONS UTILITAIRES DE SÉCURITÉ
# =====================================================
def assert_valid_identifier(name: str) -> None:
    """
    Valide qu'un identifiant SQL (nom de table, colonne) est sûr.
    Lève une ValueError si l'identifiant contient des caractères non autorisés.
    """
    if not isinstance(name, str):
        raise ValueError("L'identifiant doit être une chaîne de caractères.")
    # Autorise lettres, chiffres, underscores, et points (pour schémas.tables)
    if not name.replace('_', '').replace('.', '').isalnum():
        raise ValueError(f"Identifiant SQL invalide : {name}. Seuls les caractères alphanumériques, underscores et points sont autorisés.")

def load_whitelist_tables(conn, schema: str = 'public') -> set[str]:
    """
    Charge une liste blanche des noms de tables valides depuis information_schema.
    Retourne un set des noms de tables pour validation.
    """
    try:
        result = conn.execute(text(f"""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = :schema_name
        """), {"schema_name": schema}).fetchall()
        return {row[0] for row in result}
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement de la whitelist des tables: {e}")
        return set()  # Retourne un set vide en cas d'erreur

print("✅ Fonctions de sécurité (assert_valid_identifier, load_whitelist_tables) chargées.")
```

**Référence** : Voir `notebooks/datasens_E1_v3/03_ingest_sources.ipynb` cellule 4 (lignes 437-464)

#### v2 : `notebooks/datasens_E1_v2/02_schema_create.ipynb`

**Ajouter après la création de `engine` :**

```python
# =====================================================
# FONCTIONS UTILITAIRES DE SÉCURITÉ
# =====================================================
def assert_valid_identifier(name: str) -> None:
    """
    Valide qu'un identifiant SQL (nom de table, colonne) est sûr.
    Lève une ValueError si l'identifiant contient des caractères non autorisés.
    """
    if not isinstance(name, str):
        raise ValueError("L'identifiant doit être une chaîne de caractères.")
    # Autorise lettres, chiffres, underscores, et points (pour schémas.tables)
    if not name.replace('_', '').replace('.', '').isalnum():
        raise ValueError(f"Identifiant SQL invalide : {name}. Seuls les caractères alphanumériques, underscores et points sont autorisés.")

print("✅ Fonctions de sécurité chargées")
```

**Si des DROP TABLE sont présents**, valider avant utilisation :
```python
for table in drop_order:
    assert_valid_identifier(table)  # Protection anti-injection SQL
    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
```

#### v1 : `notebooks/datasens_E1_v1/02_schema_create.ipynb`

**Ajouter après la connexion SQLite** :

```python
# =====================================================
# FONCTIONS UTILITAIRES DE SÉCURITÉ
# =====================================================
def assert_valid_identifier(name: str) -> None:
    """
    Valide qu'un identifiant SQL (nom de table, colonne) est sûr.
    Bien que SQLite soit moins sensible, la validation est une bonne pratique.
    """
    if not isinstance(name, str):
        raise ValueError("L'identifiant doit être une chaîne de caractères.")
    if not name.replace('_', '').replace('.', '').isalnum():
        raise ValueError(f"Identifiant SQL invalide : {name}")

print("✅ Fonctions de sécurité chargées")
```

**Valider les noms de tables avant création** :
```python
for name, sql in TABLES_SQL.items():
    assert_valid_identifier(name)  # Validation avant création
    cur.execute(sql)
    tables_created.append(name)
```

---

### 2. **Visualisations Améliorées (Priorité 2)**

#### v1 : `notebooks/datasens_E1_v1/03_ingest_sources.ipynb`

**Ajouter des tables pandas après chaque collecte** :

```python
# Après insertion de documents
with engine.connect() as conn:
    df_docs = pd.read_sql_query("""
        SELECT d.id_doc, d.titre, d.langue, d.date_publication
        FROM document d
        JOIN flux f ON d.id_flux = f.id_flux
        JOIN source s ON f.id_source = s.id_source
        WHERE s.nom = :nom_source
        ORDER BY d.id_doc DESC
        LIMIT 10
    """, conn, params={"nom_source": "Nom Source"})
    
    print("\n📋 Table 'document' - Documents insérés (aperçu 10 premiers) :")
    display(df_docs)  # Afficher le DataFrame
```

**Référence** : Voir `notebooks/datasens_E1_v3/03_ingest_sources.ipynb` pour exemples complets

#### v1/v2 : `04_crud_tests.ipynb`

**Améliorer les visualisations de qualité** :

```python
# Après vérification des doublons
if nb_doublons > 0:
    plt.figure(figsize=(10, 6))
    categories = ['Documents uniques', 'Doublons détectés']
    values = [nb_docs_uniques, nb_doublons]
    colors = ['#4ECDC4', '#FECA57']
    bars = plt.bar(categories, values, color=colors)
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.02,
                f"{int(value):,}", ha='center', va='bottom', fontweight='bold')
    plt.title("🧹 Détection des doublons (SHA256)", fontsize=12, fontweight='bold')
    plt.ylabel("Nombre de documents", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()
```

---

### 3. **Documentation et Cohérence (Priorité 3)**

#### Vérifier `README_VERSIONNING.md`

- ✅ Vérifier que les entrées sont cohérentes entre v1/v2/v3
- ✅ Format uniforme : `YYYY-MM-DD HH:MM:SS | Action | Détail`

#### Commentaires inline

- ✅ Ajouter des commentaires expliquant les choix techniques
- ✅ Référencer `docs/GUIDE_TECHNIQUE_E1.md` pour plus de détails

---

## 📋 Checklist d'Application

### v2 (PostgreSQL)
- [ ] Ajouter fonctions sécurité dans `03_ingest_sources.ipynb`
- [ ] Ajouter fonctions sécurité dans `02_schema_create.ipynb` (si DROP TABLE)
- [ ] Vérifier visualisations dans `03_ingest_sources.ipynb` (déjà bon, peut améliorer)
- [ ] Améliorer visualisations dans `04_crud_tests.ipynb`
- [ ] Vérifier cohérence `README_VERSIONNING.md`

### v1 (SQLite)
- [ ] Ajouter fonctions sécurité dans `02_schema_create.ipynb`
- [ ] Ajouter tables pandas dans `03_ingest_sources.ipynb` (après chaque collecte)
- [ ] Améliorer visualisations dans `04_crud_tests.ipynb`
- [ ] Vérifier cohérence `README_VERSIONNING.md`

---

## 🔗 Références

- **Code source v3** : `notebooks/datasens_E1_v3/03_ingest_sources.ipynb` (cellule 4)
- **Guide technique** : `docs/GUIDE_TECHNIQUE_E1.md`
- **Documentation sécurité** : `docs/SECURITY.md`
- **Audit sécurité** : `docs/AUDIT_SECURITE_DOCS.md`

---

## 💡 Notes

1. **Format JSON des notebooks** : L'édition automatique via `edit_notebook` peut échouer si le formatage diffère. En cas d'échec, ajouter manuellement les fonctions en s'inspirant de v3.

2. **Compatibilité** : Les fonctions de sécurité sont identiques entre v1 (SQLite), v2 (PostgreSQL) et v3 (PostgreSQL), seule la validation des schémas diffère.

3. **Tests** : Après ajout des fonctions, tester que les notebooks s'exécutent sans erreur.

---

**Dernière mise à jour** : 2025-11-01

