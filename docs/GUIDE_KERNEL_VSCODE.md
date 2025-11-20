# 🔧 Guide : Résoudre le problème de sélection du kernel dans VS Code

## Problème
Impossible de sélectionner un kernel dans VS Code pour les notebooks Jupyter.

## ✅ Solution rapide (3 étapes)

### Étape 1 : Vérifier les extensions VS Code
Assurez-vous d'avoir installé :
- **Extension "Jupyter"** (Microsoft)
- **Extension "Python"** (Microsoft)

Si ce n'est pas le cas : `Ctrl+Shift+X` → Recherchez "Jupyter" et "Python" → Installez

---

### Étape 2 : Sélectionner l'interpréteur Python directement

**Méthode A : Via la palette de commandes**
1. Ouvrez un notebook `.ipynb` (par exemple `01_setup_env.ipynb`)
2. Appuyez sur `Ctrl+Shift+P`
3. Tapez : `Python: Select Interpreter`
4. Choisissez : `.venv\Scripts\python.exe`

**Méthode B : Via le sélecteur de kernel**
1. Ouvrez un notebook `.ipynb`
2. En haut à droite, cliquez sur **"Select Kernel"**
3. Choisissez **"Python Environments..."**
4. Sélectionnez : `C:\Users\Utilisateur\Desktop\DataSens\.venv\Scripts\python.exe`

---

### Étape 3 : Redémarrer VS Code
1. Fermez **TOUTES** les fenêtres VS Code
2. Rouvrez VS Code
3. Rouvrez votre notebook

---

## 🔍 Vérification

Pour vérifier que ça fonctionne :
1. Ouvrez `01_setup_env.ipynb`
2. Exécutez la première cellule
3. Si ça fonctionne → ✅ Le kernel est correctement configuré !

---

## ❌ Si ça ne fonctionne toujours pas

### Option 1 : Réinstaller ipykernel
```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade ipykernel
.\.venv\Scripts\python.exe -m ipykernel install --user --name=datasens_venv --display-name="DataSens Python 3.11" --force
```

### Option 2 : Utiliser Jupyter Lab (alternative)
```powershell
.\.venv\Scripts\python.exe -m pip install jupyterlab
.\.venv\Scripts\jupyter.exe lab
```
Puis ouvrez vos notebooks dans le navigateur.

### Option 3 : Vérifier les logs VS Code
1. `Ctrl+Shift+P` → `Developer: Show Output`
2. Sélectionnez "Jupyter" dans la liste
3. Regardez les erreurs éventuelles

---

## 📝 Configuration actuelle

- **Kernel installé** : `datasens_venv`
- **Python** : `.venv\Scripts\python.exe`
- **Kernel configuré dans** : Tous les notebooks E1_v3

---

## 💡 Astuce

Si vous avez toujours des problèmes, vous pouvez utiliser directement l'interpréteur Python sans passer par le kernel Jupyter :
- VS Code devrait automatiquement détecter `.venv\Scripts\python.exe` grâce à `.vscode/settings.json`

