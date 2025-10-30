# Dictionnaire des relations DataSens (MLD → MPD)

| **Domaine** | **Relation** | **Cardinalité** | **PK / FK concernées** | **Verbe d’action** | **Rôle fonctionnel** |
| --- | --- | --- | --- | --- | --- |
| 🟦 Collecte | T01_TYPE_DONNEE → T02_SOURCE | 1–N | id_type_donnee → id_type_donnee | catégorise | Classe les sources selon leur type (API, fichier, etc.) |
|  | T02_SOURCE → T03_FLUX | 1–N | id_source → id_source | alimente | Une source produit plusieurs flux de collecte |
|  | T03_FLUX → T04_DOCUMENT | 1–N | id_flux → id_flux | génère | Chaque flux alimente plusieurs documents |
|  | T02_SOURCE → T37_ARCHIVE_FLUX | 1–N | id_source → id_source | historise | Historise les versions antérieures des flux |
| 🟧 Annotation & Émotions | T04_DOCUMENT → T05_ANNOTATION | 1–N | id_doc → id_doc | contient | Un document peut être annoté plusieurs fois |
|  | T05_ANNOTATION → T06_ANNOTATION_EMOTION | 1–N | id_annotation → id_annotation | associe | Lie une annotation à une ou plusieurs émotions |
|  | T08_EMOTION → T06_ANNOTATION_EMOTION | 1–N | id_emotion → id_emotion | rattachée | Associe une émotion à plusieurs annotations |
|  | T08_EMOTION → T09_TYPE_EMOTION | N–1 | id_type_emotion → id_type_emotion | appartient à | Chaque émotion est d’un type précis |
|  | T09_TYPE_EMOTION → T10_VALENCE | N–1 | id_valence → id_valence | porte | Chaque type d’émotion a une valence (positive, neutre, négative) |
|  | T08_EMOTION → T11_MODELE_IA | N–1 | id_modele → id_modele | produite par | Émotion détectée par un modèle IA |
|  | T05_ANNOTATION → T07_META_ANNOTATION | 1–N | id_annotation → id_annotation | évaluée par | Chaque annotation peut être auditée |
|  | T11_MODELE_IA → T07_META_ANNOTATION | 1–N | id_modele → id_modele | produit | L’IA génère une évaluation automatique |
|  | T12_UTILISATEUR → T05_ANNOTATION | 1–N | id_user → id_user | valide | Un utilisateur humain valide plusieurs annotations |
| 🟩 Géographie | T13_PAYS → T14_REGION | 1–N | id_pays → id_pays | contient | Chaque pays regroupe plusieurs régions |
|  | T14_REGION → T15_DEPARTEMENT | 1–N | id_region → id_region | contient | Une région contient plusieurs départements |
|  | T15_DEPARTEMENT → T16_COMMUNE | 1–N | id_departement → id_departement | contient | Un département contient plusieurs communes |
|  | T16_COMMUNE → T17_TERRITOIRE | 1–N | id_commune → id_commune | référence | Le territoire correspond à une commune précise |
|  | T04_DOCUMENT → T17_TERRITOIRE | N–1 | id_territoire → id_territoire | localisé dans | Chaque document est géolocalisé |
| 🟨 Contexte : météo & indicateurs | T18_TYPE_METEO → T19_METEO | 1–N | id_type_meteo → id_type_meteo | qualifie | Type de conditions météo |
|  | T17_TERRITOIRE → T19_METEO | 1–N | id_territoire → id_territoire | possède | Relevés météo par territoire |
|  | T20_TYPE_INDICATEUR → T22_INDICATEUR | 1–N | id_type_indic → id_type_indic | définit | Définit la nature de l’indicateur |
|  | T21_SOURCE_INDICATEUR → T22_INDICATEUR | 1–N | id_source_indic → id_source_indic | publie | Source de l’indicateur (INSEE, etc.) |
|  | T17_TERRITOIRE → T22_INDICATEUR | 1–N | id_territoire → id_territoire | constate | Données socio-éco par commune |
| 🟪 Thèmes / Événements | T23_THEME_CATEGORY → T24_THEME | 1–N | id_theme_cat → id_theme_cat | classe | Catégorisation des thèmes |
|  | T24_THEME → T25_EVENEMENT | 1–N | id_theme → id_theme | influence | Thème relié à plusieurs événements |
|  | T04_DOCUMENT ↔ T26_DOCUMENT_THEME | N–N | id_doc ↔ id_theme | traite | Document lié à un ou plusieurs thèmes |
|  | T04_DOCUMENT ↔ T27_DOCUMENT_EVENEMENT | N–N | id_doc ↔ id_event | lié à | Document lié à un événement |
|  | T24_THEME → T25_EVENEMENT | 1–N | id_theme → id_theme | thématise | Un thème regroupe plusieurs événements |
| 🟧 Baromètres | T28_SOURCE_BAROMETRE → T29_DOCUMENT_BARO | 1–N | id_source_baro → id_source_baro | documente | Source de sondage / baromètre |
|  | T29_DOCUMENT_BARO → T04_DOCUMENT | 1–1 | id_doc → id_doc | décrit | Associe un document externe à une source barométrique |
| 🟥 Pipeline & Qualité | T30_PIPELINE → T31_ETAPE_ETL | 1–N | id_pipeline → id_pipeline | compose | Un pipeline regroupe plusieurs étapes |
|  | T31_ETAPE_ETL → T32_EXEC_ETAPE | 1–N | id_etape → id_etape | exécutée par | Étapes concrètement exécutées |
|  | T03_FLUX ↔ T32_EXEC_ETAPE | N–N | id_flux ↔ id_exec | alimente | Lien entre flux source et exécution |
|  | T04_DOCUMENT ↔ T32_EXEC_ETAPE | N–N | id_doc ↔ id_exec | produit | Sortie documentaire des jobs ETL |
|  | T31_ETAPE_ETL ↔ T33_QC_RULE | N–N | id_etape ↔ id_qc | applique | Étape liée à des règles de qualité |
|  | T32_EXEC_ETAPE → T34_QC_RESULT | 1–N | id_exec → id_exec | génère | Exécution génère un rapport de qualité |
|  | T33_QC_RULE → T34_QC_RESULT | 1–N | id_qc → id_qc | vérifie | Chaque règle produit plusieurs résultats |
| ⚙️ Gouvernance / Versionning | T12_UTILISATEUR → T35_TABLE_AUDIT | 1–N | id_user → user | opère | Un utilisateur effectue des opérations sur la base |
|  | T35_TABLE_AUDIT → T36_TABLE_VERSION | N–1 | table_name → table_name | trace | Journalisation des modifications |
|  | T36_TABLE_VERSION → T30_PIPELINE | N–1 | table_name → id_pipeline | versionne | Permet le suivi des schémas de pipeline |
