# 📊 Configuration Flexible des Sources DataSens

Ce dossier contient la configuration flexible de **toutes les sources** DataSens (E1 + Baromètres).

## 🎯 Principe

**Pour ajouter/modifier une source, vous n'avez besoin que d'éditer le fichier JSON. Aucune modification de code n'est nécessaire !**

## 📁 Fichiers

- `sources_config.json` : Configuration complète de toutes les sources (E1 + Baromètres)

## 🔧 Comment ajouter une nouvelle source

1. Ouvrez `sources_config.json`
2. Ajoutez une nouvelle entrée dans le tableau `sources[]`
3. Remplissez les champs (voir exemple ci-dessous)
4. Relancez le notebook `03_ingest_sources.ipynb`

### Exemple complet

```json
{
  "id": "source_XXX",
  "nom": "Nom de votre source",
  "type_source": "Données Maîtres",
  "categorie": "Catégorie de source",
  "format": "csv",
  "url": "https://example.com/",
  "url_data": "https://example.com/data.csv",
  "description": "Description de la source",
  "themes": ["Thème1", "Thème2"],
  "tables_target": ["t22_indicateur", "t04_document"],
  "frequence_collecte": "mensuelle",
  "actif": true,
  "priorite": "moyenne",
  "api_key_required": false,
  "api_key_env": "",
  "collector": "csv_file",
  "params": {
    "separator": ",",
    "encoding": "utf-8"
  }
}
```

## 📋 Types de collecteurs

### `csv_file`
Collecte depuis fichier CSV local ou distant.

**Paramètres** : `separator`, `encoding`

### `api_rest`
Collecte depuis API REST.

**Paramètres** : `endpoint`, `method`, `cities` (pour météo), etc.

### `rss_feed`
Collecte depuis flux RSS.

**Paramètres** : `feeds` (liste de feeds), `max_items_per_feed`

### `web_scraping`
Collecte via web scraping.

**Paramètres** : `selectors` (sélecteurs CSS), `sources` (liste de sources)

### `gdelt_big_data`
Collecte GDELT Big Data.

**Paramètres** : `filter_country`, `max_rows`

### `pdf_parser`
Extraction depuis PDF.

**Paramètres** : `extract_text`, `extract_tables`

## 🔄 Utilisation

Le notebook `03_ingest_sources.ipynb` charge automatiquement cette configuration et collecte toutes les sources actives.

## 📝 Pour désactiver une source

Mettez `"actif": false` dans sa configuration.
