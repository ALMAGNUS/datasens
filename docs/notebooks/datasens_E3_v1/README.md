# 📊 DataSens E3_v1 - Dataset IA Territorial Français sur l'Humeur

## 🎯 Objectif

Créer le **meilleur dataset IA territorial français** sur l'humeur pour entraîner les modèles IA.

**Input** : Dataset fourni (algorithme de référence mondial)  
**Output** : Dataset GOLD optimisé (Parquet + CSV) prêt pour ML/DL

---

## 📁 Structure E3_v1

```
notebooks/datasens_E3_v1/
├── 01_prepare_dataset_input.ipynb    # Réception et validation dataset
├── 02_territorial_annotation.ipynb   # Annotation territoriale
├── 03_humeur_labeling.ipynb          # Labeling humeur
├── 04_quality_control.ipynb          # Contrôles qualité
└── 05_export_gold_dataset.ipynb      # Export dataset GOLD
```

---

## 🔄 Pipeline E3

```
Dataset Fourni (Algorithme référence)
    ↓
01_prepare_dataset_input.ipynb
    ↓
02_territorial_annotation.ipynb
    ↓
03_humeur_labeling.ipynb
    ↓
04_quality_control.ipynb
    ↓
05_export_gold_dataset.ipynb
    ↓
Dataset GOLD (data/gold/dataset_ia/humeur_territorial_fr_*.parquet)
```

---

## 📋 Spécifications Dataset GOLD

Voir `docs/PREPARATION_E3_DATASET_IA_HUMEUR.md` pour les détails complets.

---

## 🚀 Utilisation

1. Placer votre dataset dans `data/raw/e3_input/`
2. Exécuter les notebooks dans l'ordre (01 → 05)
3. Dataset GOLD généré dans `data/gold/dataset_ia/`

---

**En attente du dataset pour créer le meilleur dataset IA territorial français !** 🇫🇷

