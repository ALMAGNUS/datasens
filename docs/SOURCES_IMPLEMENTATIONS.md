# 📋 Implémentations des Sources (Extrait de datasens_E1_v2.ipynb)

Ce document récapitule les implémentations des 5 sources telles qu'elles ont été trouvées et intégrées dans le notebook `03_ingest_sources.ipynb`.

## 📄 Source 1 : Fichier plat CSV (Kaggle)

**Statut** : ✅ Déjà implémenté dans `03_ingest_sources.ipynb`

**Architecture** :
- 50% → PostgreSQL (table `document`)
- 50% → MinIO DataLake (fichiers bruts)

**Process** :
1. Chargement CSV depuis `data/raw/kaggle/`
2. Calcul SHA256 fingerprint pour déduplication
3. Split aléatoire 50/50
4. Upload 50% vers MinIO
5. Insertion 50% dans PostgreSQL avec traçabilité (id_flux)

---

## 🌦️ Source 2 : API OpenWeatherMap

**Code source** : `datasens_E1_v2.ipynb` (Cellule ~927-994)

**Implémentation** : ✅ Intégrée dans `03_ingest_sources.ipynb` (Cellules 5-6)

**Villes collectées** : Paris, Lyon, Marseille, Lille

**Données récupérées** :
- Température (°C), Humidité (%), Pression (hPa)
- Description météo (clair, nuageux, pluie...)
- Vitesse du vent (m/s)
- Timestamp de mesure

**Stockage** :
- **PostgreSQL** : Table `meteo` avec géolocalisation (id_territoire FK)
- **MinIO** : CSV brut (`api/owm/owm_*.csv`)

**API Key requise** : `OWM_API_KEY` dans `.env`

---

## 📰 Source 3 : Flux RSS Multi-Sources (Presse française)

**Code source** : `datasens_E1_v2.ipynb` (Cellule ~1037-1210)

**Implémentation** : ✅ Intégrée dans `03_ingest_sources.ipynb` (Cellules 7-8)

**Sources RSS** :
- **Franceinfo** : `https://www.francetvinfo.fr/titres.rss`
- **20 Minutes** : `https://www.20minutes.fr/feeds/rss-une.xml`
- **Le Monde** : `https://www.lemonde.fr/rss/une.xml`

**Extraction** : titre, description, date publication, URL source

**Stockage** :
- **PostgreSQL** : Table `document` avec métadonnées
- **MinIO** : CSV compilé (`rss/rss_multi_sources_*.csv`)

**Déduplication** : SHA256 sur (titre + description)

**Module requis** : `feedparser` (pip install feedparser)

---

## 🌐 Source 4 : Web Scraping Multi-Sources (Dry-run)

**Code source** : `datasens_E1_v2.ipynb` (Cellule ~1540-1782)

**Implémentation** : ✅ Intégrée dans `03_ingest_sources.ipynb` (Cellules 9-10)

**Version simplifiée pour E1** :
- **Vie-publique.fr** (RSS) : Consultations citoyennes nationales
- **data.gouv.fr** (API) : Open Data datasets CSV officiels

**Éthique & Légalité** :
- ✅ Open Data gouvernemental (.gouv.fr)
- ✅ Respect robots.txt
- ✅ APIs officielles uniquement
- ✅ Aucun scraping de sites privés sans autorisation

**Stockage** :
- **PostgreSQL** : Documents structurés
- **MinIO** : CSV bruts (`scraping/multi/scraping_multi_*.csv`)

**Note** : Version complète dans `datasens_E1_v2.ipynb` inclut aussi Reddit, YouTube, SignalConso, Trustpilot

---

## 🌍 Source 5 : GDELT GKG France (Big Data)

**Code source** : `datasens_E1_v2.ipynb` (Cellule ~1867+)

**Implémentation** : ✅ Intégrée dans `03_ingest_sources.ipynb` (Cellules 11-12)

**Source** : http://data.gdeltproject.org/gdeltv2/

**Format** : GKG 2.0 (Global Knowledge Graph) - Fichiers CSV.zip (~300 MB/15min)

**Contenu Big Data** :
- Événements mondiaux géolocalisés
- **Tonalité émotionnelle** (V2Tone : -100 négatif → +100 positif)
- **Thèmes extraits** (V2Themes : PROTEST, HEALTH, ECONOMY, TERROR...)
- **Entités nommées** (V2Persons, V2Organizations)
- **Géolocalisation** (V2Locations avec codes pays)

**Filtrage France** :
- Sélection événements avec localisation France (code pays FR)
- Extraction tonalité moyenne France
- Top thèmes français

**Stratégie Big Data** :
- Téléchargement fichier dernières 15min (~6-300 MB brut)
- Parsing colonnes V2* nommées (27 colonnes GKG)
- Filtrage géographique France → échantillon (100 événements pour démo)
- Storage MinIO (fichier brut complet)
- Insertion PostgreSQL (événements + documents + thèmes)

**Stockage** :
- **MinIO** : ZIP brut (`gdelt/*.gkg.csv.zip`)
- **PostgreSQL** : Tables `evenement`, `document`, `document_evenement`, `theme`

---

## 🔗 Notes d'Intégration

Toutes les sources suivent la même architecture pipeline :

1. **Logging structuré** : `logs/collecte_*.log` + `logs/errors_*.log`
2. **MinIO DataLake** : Upload automatique fichiers bruts → `s3://datasens-raw/`
3. **PostgreSQL** : Insertion structurée avec traçabilité (flux, manifests)
4. **Fonctions helpers** : `create_flux()`, `insert_documents()`, `ensure_territoire()`, `minio_upload()`
5. **Déduplication** : Hash SHA-256 pour éviter doublons
6. **RGPD** : Pas de données personnelles directes

**Référence** : Voir `notebooks/datasens_E1_v2.ipynb` pour implémentations complètes avec toutes les variantes
