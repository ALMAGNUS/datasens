# Dictionnaire des Tables — DataSens

# 🧱 DOMAINE 1 — COLLECTE

**🟦**

**T01 – TYPE_DONNEE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_type_donnee | PK | int | Identifiant unique |
| libelle |  | varchar(100) | Nom du type (Fichier, API, Web, BigData) |
| description |  | text | Détail fonctionnel |
| frequence_maj |  | varchar(50) | Quotidienne / Hebdo / Temps réel |
| categorie_metier |  | varchar(50) | Descriptive / Usage / Évaluation / Qualité |
| Rôle : Classifie les sources selon leur nature et usage. |  |  |  |
| Relation : TYPE_DONNEE 1—N SOURCE. |  |  |  |

**🟦**

**T02 – SOURCE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_source | PK | int | Identifiant |
| id_type_donnee | FK | int | Lien vers TYPE_DONNEE |
| nom |  | varchar(100) | Nom de la source |
| url |  | text | Lien complet |
| fiabilite |  | float | Score 0–1 |
| Rôle : Référentiel des fournisseurs de données. |  |  |  |
| Relation : SOURCE 1—N FLUX. |  |  |  |

**🟦**

**T03 – FLUX**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_flux | PK | int | Identifiant |
| id_source | FK | int | Lien vers SOURCE |
| date_collecte |  | datetime | Date d’extraction |
| format |  | varchar(20) | CSV / JSON / XML |
| manifest_uri |  | text | Emplacement MinIO / S3 |
| Rôle : Trace d’une collecte automatisée. |  |  |  |
| Relation : FLUX 1—N DOCUMENT. |  |  |  |

# 🧾 DOMAINE 2 — DOCUMENTS & ANNOTATIONS

**🟨**

**T04 – DOCUMENT**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_doc | PK | int | Identifiant |
| id_flux | FK | int | Lien FLUX |
| id_territoire | FK | int | Lien TERRITOIRE |
| titre |  | text | Titre du texte |
| texte |  | text | Contenu |
| langue |  | varchar(10) | Langue détectée |
| date_publication |  | datetime | Date du texte |
| hash_fingerprint |  | varchar(64) | Empreinte anti-doublon |
| Rôle : Représente une unité textuelle (article, post, sondage). |  |  |  |
| Relation : DOCUMENT 1–N ANNOTATION, N–N THEME, N–N EVENEMENT. |  |  |  |

**🟨**

**T05 – ANNOTATION**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_annotation | PK | int | Identifiant |
| id_doc | FK | int | Lien DOCUMENT |
| id_user | FK | int | Lien UTILISATEUR |
| intensity |  | float | Intensité émotionnelle (0–1) |
| polarity |  | varchar(20) | Positive / Neutre / Négative |
| date_annotation |  | datetime | Date |
| Rôle : Annotation humaine ou automatique. |  |  |  |
| Relation : ANNOTATION 1–N META_ANNOTATION / N–N EMOTION. |  |  |  |

**🟨**

**T06 – ANNOTATION_EMOTION**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_annotation | FK | int | Lien ANNOTATION |
| id_emotion | FK | int | Lien EMOTION |
| relevance_score |  | float | Pertinence (0–1) |
| Rôle : Lien multi-étiquette entre annotations et émotions. |  |  |  |

**🟨**

**T07 – META_ANNOTATION**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_meta_annotation | PK | int | Identifiant |
| id_annotation | FK | int | Lien ANNOTATION |
| id_modele | FK | int | Lien MODELE_IA |
| coherence_score |  | float | Score cohérence IA/Humain |
| commentaire |  | text | Remarques |
| date_evaluation |  | datetime | Date |
| Rôle : Contrôle qualité des annotations. |  |  |  |

**🟥**

**T08 – EMOTION**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_emotion | PK | int | Identifiant |
| id_type_emotion | FK | int | Lien TYPE_EMOTION |
| id_modele | FK | int | Lien MODELE_IA |
| score_confiance |  | float | Confiance (0–1) |
| Rôle : Émotion détectée ou validée. |  |  |  |

**🟥**

**T09 – TYPE_EMOTION**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_type_emotion | PK | int | Identifiant |
| id_valence | FK | int | Lien VALENCE |
| libelle |  | varchar(100) | Nom (joie, peur, colère…) |
| description |  | text | Détail |
| Rôle : Dictionnaire des émotions. |  |  |  |

**🟥**

**T10 – VALENCE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_valence | PK | int | Identifiant |
| label |  | varchar(50) | Positive / neutre / négative |
| description |  | text | Détail |
| Rôle : Catégorie du ressenti émotionnel. |  |  |  |

**🟥**

**T11 – MODELE_IA**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_modele | PK | int | Identifiant |
| nom |  | varchar(100) | Nom du modèle |
| version |  | varchar(20) | Version |
| auteur |  | varchar(100) | Auteur |
| type_modele |  | varchar(50) | Type d’algorithme |
| source_repo |  | text | Lien GitHub / HuggingFace |
| Rôle : Registre des modèles IA utilisés. |  |  |  |

**🟩**

**T12 – UTILISATEUR**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_user | PK | int | Identifiant |
| nom |  | varchar(100) | Nom |
| role |  | varchar(50) | Annotateur / admin |
| organisation |  | varchar(100) | Entreprise / école |
| Rôle : Acteurs des traitements. |  |  |  |

# 🌍 DOMAINE 3 — GÉOGRAPHIE

**🟩**

**T13 – PAYS**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_pays | PK | int | Identifiant |
| nom |  | varchar(100) | Nom du pays |

**🟩**

**T14 – REGION**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_region | PK | int | Identifiant |
| id_pays | FK | int | Lien PAYS |
| nom |  | varchar(100) | Nom de la région |

**🟩**

**T15 – DEPARTEMENT**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_departement | PK | int | Identifiant |
| id_region | FK | int | Lien REGION |
| code_dept |  | varchar(5) | Code officiel |
| nom |  | varchar(100) | Nom du département |

**🟩**

**T16 – COMMUNE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_commune | PK | int | Identifiant |
| id_departement | FK | int | Lien DEPARTEMENT |
| code_insee |  | varchar(10) | Code INSEE |
| nom_commune |  | varchar(100) | Nom |
| lat |  | float | Latitude |
| lon |  | float | Longitude |
| population |  | int | Taille |
| Rôle : Référentiel géographique local. |  |  |  |

**🟩**

**T17 – TERRITOIRE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_territoire | PK | int | Identifiant |
| id_commune | FK | int | Lien COMMUNE |
| Rôle : Pivot territorial de rattachement. |  |  |  |

# 🌦️ DOMAINE 4 — MÉTÉO

**🟩**

**T18 – TYPE_METEO**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_type_meteo | PK | int | Identifiant |
| libelle |  | varchar(50) | Soleil, Pluie, Neige |
| description |  | text | Détail |
| Rôle : Dictionnaire des conditions météo. |  |  |  |

**🟩**

**T19 – METEO**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_meteo | PK | int | Identifiant |
| id_territoire | FK | int | Lien TERRITOIRE |
| id_type_meteo | FK | int | Lien TYPE_METEO |
| date_obs |  | datetime | Observation |
| temperature |  | float | °C |
| humidite |  | float | % |
| vent_kmh |  | float | km/h |
| pression |  | float | hPa |
| Rôle : Observations climatiques locales. |  |  |  |

# 📊 DOMAINE 5 — INDICATEURS

**🟩**

**T20 – TYPE_INDICATEUR**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_type_indic | PK | int | Identifiant |
| code |  | varchar(50) | Code unique |
| libelle |  | varchar(100) | Nom complet |
| unite |  | varchar(20) | Unité de mesure |
| Rôle : Dictionnaire des indicateurs. |  |  |  |

**🟩**

**T21 – SOURCE_INDICATEUR**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_source_indic | PK | int | Identifiant |
| nom |  | varchar(100) | Nom de l’organisme |
| url |  | text | Lien officiel |
| Rôle : Référentiel des producteurs. |  |  |  |

**🟩**

**T22 – INDICATEUR**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_indic | PK | int | Identifiant |
| id_territoire | FK | int | Lien TERRITOIRE |
| id_type_indic | FK | int | Lien TYPE_INDICATEUR |
| id_source_indic | FK | int | Lien SOURCE_INDICATEUR |
| valeur |  | float | Valeur observée |
| annee |  | int | Année |
| Rôle : Valeurs socio-économiques localisées. |  |  |  |

# 🧩 DOMAINE 6 — THÈMES & ÉVÉNEMENTS

**🟦**

**T23 – THEME_CATEGORY**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_theme_cat | PK | int | Identifiant |
| libelle |  | varchar(100) | Macro catégorie |
| description |  | text | Détail |
| Rôle : Classement des thèmes. |  |  |  |

**🟦**

**T24 – THEME**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_theme | PK | int | Identifiant |
| id_theme_cat | FK | int | Lien THEME_CATEGORY |
| libelle |  | varchar(100) | Nom du thème |
| description |  | text | Détail |
| Rôle : Thèmes précis (ex : “Pouvoir d’achat”). |  |  |  |

**🟦**

**T25 – EVENEMENT**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_event | PK | int | Identifiant |
| id_theme | FK | int | Lien THEME |
| date_event |  | datetime | Date |
| avg_tone |  | float | Tonalité moyenne |
| source_event |  | varchar(50) | Origine |
| Rôle : Événements médiatiques/économiques. |  |  |  |

**🟦**

**T26 – DOCUMENT_THEME**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_doc | FK | int | Lien DOCUMENT |
| id_theme | FK | int | Lien THEME |
| Rôle : Liaison N–N documents ↔ thèmes. |  |  |  |

**🟦**

**T27 – DOCUMENT_EVENEMENT**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_doc | FK | int | Lien DOCUMENT |
| id_event | FK | int | Lien EVENEMENT |
| Rôle : Liaison N–N documents ↔ événements. |  |  |  |

# 📈 DOMAINE 7 — SOURCES BAROMÉTRIQUES

**🟦**

**T28 – SOURCE_BAROMETRE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_source_baro | PK | int | Identifiant |
| nom |  | varchar(100) | Nom du baromètre |
| url |  | text | Lien officiel |
| Rôle : Référentiel Ifop, Cevipof, Ipsos… |  |  |  |

**🟦**

**T29 – DOCUMENT_BARO**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_document_baro | PK | int | Identifiant |
| id_source_baro | FK | int | Lien SOURCE_BAROMETRE |
| id_doc | FK | int | Lien DOCUMENT |
| date_pub |  | datetime | Date |
| titre |  | text | Titre |
| lien |  | text | Lien |
| Rôle : Indexe les baromètres liés à un document. |  |  |  |

# ⚙️ DOMAINE 8 — PIPELINE & QUALITÉ

**🟧**

**T30 – PIPELINE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_pipeline | PK | int | Identifiant |
| nom |  | varchar(100) | Nom du pipeline |
| description |  | text | Détail |
| owner |  | varchar(100) | Responsable |
| actif |  | boolean | Statut |
| Rôle : Orchestration ETL. |  |  |  |

**🟧**

**T31 – ETAPE_ETL**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_etape | PK | int | Identifiant |
| id_pipeline | FK | int | Lien PIPELINE |
| ordre |  | int | Ordre d’exécution |
| type |  | varchar(50) | Extraction / Nettoyage… |
| nom |  | varchar(100) | Nom étape |
| parametres_modele |  | text | Paramètres IA |
| Rôle : Étape d’un flux ETL. |  |  |  |

**🟧**

**T32 – EXEC_ETAPE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_exec | PK | int | Identifiant |
| id_etape | FK | int | Lien ETAPE_ETL |
| debut |  | datetime | Début |
| fin |  | datetime | Fin |
| statut |  | varchar(50) | Succès / Échec |
| nb_entrees |  | int | Entrées |
| nb_sorties |  | int | Sorties |
| erreurs_json |  | text | Logs d’erreurs |
| Rôle : Historique d’exécution ETL. |  |  |  |

**🟧**

**T33 – QC_RULE**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_qc | PK | int | Identifiant |
| code |  | varchar(50) | Code règle |
| libelle |  | varchar(100) | Nom |
| niveau |  | varchar(20) | Niveau |
| severite |  | varchar(20) | Alerte / Warning / Info |
| definition |  | text | Description |
| Rôle : Dictionnaire des contrôles qualité. |  |  |  |

**🟧**

**T34 – QC_RESULT**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_qc_result | PK | int | Identifiant |
| id_qc | FK | int | Lien QC_RULE |
| id_exec | FK | int | Lien EXEC_ETAPE |
| score |  | float | Score |
| nb_non_conformes |  | int | Erreurs |
| details |  | text | Logs |
| Rôle : Résultats des contrôles qualité. |  |  |  |

# 🔒 DOMAINE 9 — OPTIONNELLES (Audit / Version)

**🟫**

**T35 – TABLE_AUDIT**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_audit | PK | int | Identifiant |
| table_name |  | varchar(100) | Nom de la table concernée |
| record_id |  | int | Identifiant de l’enregistrement concerné |
| action |  | varchar(20) | Type d’action (INSERT, UPDATE, DELETE) |
| old_values |  | json | Valeurs avant modification |
| new_values |  | json | Valeurs après modification |
| user |  | varchar(100) | Utilisateur ayant effectué l’action |
| ts |  | timestamp | Horodatage exact de l’action |
| Rôle : |  |  |  |
| Journalise toutes les modifications sur les tables du schéma DataSens (traçabilité complète RGPD). |  |  |  |
| Particularité : |  |  |  |
| Aucune contrainte de clé étrangère (table générique indépendante). |  |  |  |

**🟫**

**T36 – TABLE_VERSION**

| **Champ** | **Clé** | **Type** | **Description** |
| --- | --- | --- | --- |
| id_version | PK | int | Identifiant |
| table_name |  | varchar(100) | Nom de la table versionnée |
| schema_hash |  | varchar(64) | Empreinte de structure (MD5 ou SHA256) |
| applied_at |  | timestamp | Date de migration / version appliquée |
| comment |  | text | Description ou justification du changement |
| Rôle : |  |  |  |
| Historise les changements de structure (migration, ajout de colonnes, refactorisation). |  |  |  |
| Utilité : |  |  |  |
| Assure la compatibilité des schémas entre versions du projet (important pour CI/CD). |  |  |  |

# 🧩 SYNTHÈSE DU DICTIONNAIRE COMPLET

| **Domaine** | **Tables** | **Description synthétique** |
| --- | --- | --- |
| Collecte | T01 → T03 | Provenance et flux d’ingestion des données (sources, formats, traçabilité) |
| Documents & Annotations | T04 → T12 | Corpus textuel, annotations humaines/IA, émotions et modèles |
| Géographie | T13 → T17 | Référentiel territorial complet (pays → commune → territoire) |
| Météo | T18 → T19 | Données climatiques liées aux territoires |
| Indicateurs | T20 → T22 | Données socio-économiques par zone géographique |
| Thèmes & Événements | T23 → T27 | Classification thématique et événements associés |
| Sources Barométriques | T28 → T29 | Référentiels d’enquêtes d’opinion et baromètres sociaux |
| Pipeline & Qualité | T30 → T34 | Orchestration ETL et contrôle qualité des données |
| Techniques (optionnelles) | T35 → T36 | Journalisation (audit) et gestion de version du schéma |

# 🧠 Récapitulatif des chiffres clés

| **Élément** | **Valeur** |
| --- | --- |
| Nombre total de tables | 36 |
| Tables cœur (métier) | 34 |
| Tables optionnelles (techniques) | 2 |
| Niveau de normalisation | 3NF (aucune redondance textuelle) |
| Nombre de dictionnaires séparés (TYPE / SOURCE) | 6 |
| Tables N–N (association) | 4 (Annotations↔Émotions, Documents↔Thèmes, Documents↔Événements, Flux↔Exécutions) |

# 📘 Étape suivante – à partir de ce dictionnaire

À partir de ce dictionnaire complet, voici le plan d’action pour lundi :

| **Étape** | **Objectif** | **Livrable** |
| --- | --- | --- |
| 1️⃣ | Générer le MPD PostgreSQL (avec contraintes, FK, index, inserts de dicos) | Fichier SQL structuré |
| 2️⃣ | Créer le notebook Jupyter CRUD minimal (lecture / ajout / modif / suppression sur 4 tables clés) | Fichier .ipynb |
| 3️⃣ | Documenter l’import automatique des fichiers bruts → MinIO DataLake | Script Python + doc |
| 4️⃣ | Vérifier avec ton prof que toutes les cases E1 sont cochées | Capture du tableau Excel E1 |
