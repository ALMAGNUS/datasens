# C’est le carburant de DataSens 🚀

# 🧭 Synthèse —

# Sources potentielles de données pour enrichir DataSens

# ⚙️ 1️⃣ PILIER : FICHIERS PLATS (CSV, XLSX, JSON)

Objectif : exploiter des datasets statiques, descriptifs ou historiques disponibles sur des plateformes ouvertes (Kaggle, Data.gouv, etc.)

**🔹 Sources françaises & francophones**

| **Plateforme** | **Dataset / Exemple** | **Type de données** | **Fréquence** | **Pertinence émotionnelle** |
| --- | --- | --- | --- | --- |
| Kaggle | 🇫🇷 French News Articles Dataset | Titres + textes médias FR | Hebdomadaire | Analyse de sentiment et ton médiatique |
| Data.gouv.fr | Baromètre de la confiance politique / sécurité / emploi | Enquêtes sociales publiques | Mensuelle | Mesure de tension sociale |
| INSEE | Revenus médians, chômage, population, éducation | Indicateurs socio-éco | Trimestrielle | Contexte économique et bien-être |
| Open Data Santé France | Covid19, hôpitaux, vaccination | Données sanitaires | Quotidienne | Thème santé / peur / confiance |
| Banque mondiale (WB Data) | Indicateurs économiques par pays | Données macro | Annuelle | Comparaison France/UE |
| Eurostat | Qualité de vie, opinion publique | Données UE | Trimestrielle | Thèmes d’équilibre vie sociale |

🧩 Intégration :

→ dossier `data/raw/csv/`

→ ingestion via Pandas + SQLAlchemy

→ tables cibles : `flux`, `document`, `indicateur`, `type_indicateur`

# 🌐 2️⃣ PILIER : BASES DE DONNÉES (SQL / NoSQL)

Objectif : structurer des corpus riches déjà annotés (émotions, polarités, thèmes)

| **Source** | **Format** | **Contenu** | **Usage** |
| --- | --- | --- | --- |
| Kaggle DB – Emotion Detection | SQLite | Corpus FR/EN annotés émotions | Fine-tuning futur E2 |
| DBPedia / Wikidata | SPARQL | Métadonnées sur événements / personnalités | Relier événements & contexte |
| Base OpenMedia | PostgreSQL / CSV | Articles, chaînes, sources média | Catégorisation / fiabilité |
| Le Monde Diplomatique (archives) | SQL dump | Articles historiques (licence CC) | Analyse longitudinale |
| Twitter / Mastodon dumps | JSONL | Posts FR publics (échantillons) | Analyse de langage émotionnel |

🧩 Intégration :

→ `data/silver/db/`

→ extraction `pandas.read_sql()` ou `sqlite3`

→ tables : `document`, `source`, `flux`, `annotation`

# ☁️ 3️⃣ PILIER : APIs PUBLIQUES

Objectif : capter des données dynamiques (météo, actualités, réseaux sociaux, émotions sociales)

| **API** | **Données** | **Intérêt pour DataSens** | **Exemple d’usage** |
| --- | --- | --- | --- |
| OpenWeatherMap | Température, humidité, météo-type | Lien météo ↔ humeur | Table `meteo` + `territoire` |
| NewsAPI.org | Titres récents FR | Flux d’actualités réelles | Table `document` (actualités récentes) |
| GDELT API | Événements mondiaux + tonalité | Grands thèmes / tension sociale | Table `evenement` |
| Google Trends API (PyTrends) | Tendances de recherche FR | Popularité de thèmes | Table `indicateur` (socio-numérique) |
| IFOP / IPSOS / Odoxa APIs | Baromètres d’opinion | Indicateurs perçus | Table `barometre_theme` |
| API Politiques publiques (Data.gouv) | Lois, débats, élections | Climat politique | Thème “Institutions” |
| Météo France | Conditions locales | Corrélation climat / émotions | `meteo` enrichie |
| INPI API | Marques / brevets | Activité économique | Thème innovation / emploi |

🧩 Intégration :

→ `data/raw/api/`

→ JSON → tables `flux`, `document`, `meteo`, `indicateur`

→ automatisable via Prefect task

# 🧾 4️⃣ PILIER : WEB SCRAPING (avis citoyens, forums, médias locaux)

Objectif : capter les émotions réelles exprimées par les internautes (sans données personnelles directes)

| **Site** | **Thématique** | **Format** | **Méthode** |
| --- | --- | --- | --- |
| MonAvisCitoyen.fr | Satisfaction territoriale (villes) | HTML | Scraping sélectif (avis + note, hash auteur) |
| LeFigaro / LeMonde / FranceInfo | Articles + commentaires publics | HTML / RSS | Scraping + parsing |
| Forums Doctissimo / Reddit FR | Santé, société, famille | HTML / API | Limité à titres/textes |
| Trustpilot.fr | Consommation, confiance | HTML | Catégoriser ton / émotion |
| Google Actualités RSS | Tendances journalières | XML | Scraper/Parser flux RSS |
| LesDécodeurs (Le Monde) | Vérification de faits | HTML | Catégorisation “positif/négatif” |

🧩 Précautions :

- Respect robots.txt
- Hash SHA256 pour tout pseudo
- User-Agent spécifique `DataSensBot/1.0`
- Pause 3s entre requêtes

🧩 Intégration :

→ `data/raw/scraping/`

→ Tables : `document`, `flux`, `annotation`

# 💾 5️⃣ PILIER : BIG DATA (massif / évènementiel)

Objectif : capter les tendances émotionnelles à grande échelle (événements, tonalités, signaux faibles)

| **Source** | **Type** | **Exemple** | **Intérêt** |
| --- | --- | --- | --- |
| GDELT GKG (Global Knowledge Graph) | TSV (zip) | Événements FR/UE + tonalité | Corrélation actualité ↔ émotions |
| Common Crawl (FR subset) | Parquet / JSONL | Corpus web FR | Données massives textuelles |
| Hugging Face Datasets (FR) | JSON | Corpus FR annotés (EmoLex, Tweets FR) | Enrichissement annotation IA |
| Google BigQuery Public Datasets (FR) | SQL | Mots-clés actualités | Données open |
| Twitter Academic API (limité) | JSONL | Flux émotions temps réel | Corrélation climat social |
| YouTube API | JSON | Commentaires vidéos FR | Polarité culturelle |

🧩 Intégration :

→ `data/raw/bigdata/`

→ ingestion batch (Prefect Flow)

→ tables : `evenement`, `document_evenement`, `indicateur`

# 💡 Bonus —

# Sources barométriques officielles (à intégrer absolument)

Pour enrichir les indicateurs sociétaux et émotionnels.

| **Organisme** | **Baromètre** | **Type** | **Pertinence** |
| --- | --- | --- | --- |
| IFOP | Baromètre moral des Français | Opinion | Confiance / pessimisme |
| IPSOS | Fractures françaises | Opinion | Polarisation / colère |
| CREDOC | Conditions de vie & aspirations | Étude | Bien-être / attentes |
| INSEE | Baromètre social | Statistique | Économie / emploi / société |
| Oxfam | Inégalités sociales | ONG | Thèmes justice / colère |
| ADEME | Transition écologique | Opinion | Écologie / espoir |
| Ministère de la Culture | Baromètre de la confiance média | Étude | Confiance / désinformation |

🧩 Intégration :

→ `data/silver/barometres/`

→ Table : `barometre_theme` (thème + indicateur + score moral + source + date)

# 🧩 Taxonomie thématique à croiser avec les sources

| **Catégorie principale** | **Sous-thèmes** | **Exemple de sources associées** |
| --- | --- | --- |
| 1. Société & Cohésion | Sécurité, immigration, éducation | IFOP, INSEE, FranceInfo |
| 2. Économie & Pouvoir d’achat | Inflation, emploi | INSEE, Eurostat, GDELT |
| 3. Santé & Bien-être | Hôpital, pandémie | Santé France, Doctissimo |
| 4. Environnement & Climat | Pollution, météo | OpenWeatherMap, ADEME |
| 5. Politique & Institutions | Gouvernement, élections | IFOP, Oxfam |
| 6. Médias & Confiance | Désinformation, presse | Baromètre média, RSS |
| 7. Technologie & IA | Innovation, numérique | INPI, BigQuery |
| 8. Culture & Identité | Patrimoine, art, sport | Ministère Culture |
| 9. Famille & Société | Logement, éducation | MonAvisCitoyen, CREDOC |
| 10. Justice & Égalité | Inégalités, droits | Oxfam, IFOP |
| 11. Travail & Futur | Télétravail, précarité | INSEE, IPSOS |
| 12. Espoir & Résilience | JO 2024, solidarité | FranceInfo, GDELT |

# ✅ Synthèse : Architecture d’intégration

| **Type de source** | **Fréquence** | **Table cible principale** | **Objectif** |
| --- | --- | --- | --- |
| CSV / XLSX | Hebdo / mensuel | document, flux | Données textuelles |
| SQL / DB | Unique | document, annotation | Corpus enrichi |
| API | Quotidienne | meteo, indicateur | Données dynamiques |
| Scraping | Hebdo | document, annotation | Données émotionnelles citoyennes |
| Big Data | Quotidienne | evenement, indicateur | Données massives de contexte |
| Baromètres | Mensuel / trimestriel | barometre_theme | Données d’opinion synthétiques |
