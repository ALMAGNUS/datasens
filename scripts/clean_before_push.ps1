# 🧹 Script Nettoyage Avant Transmission

# Supprimer fichiers temporaires
Write-Host "🧹 Nettoyage fichiers temporaires..." -ForegroundColor Yellow

# Fichiers dev/debug
Remove-Item check_columns.py -ErrorAction SilentlyContinue
Write-Host "   ✅ check_columns.py supprimé"

# Logs temporaires
Remove-Item -Recurse -Force docs/logs/ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force notebooks/datasens_E1_v3/logs/ -ErrorAction SilentlyContinue
Write-Host "   ✅ Logs temporaires supprimés"

# Données temporaires
Remove-Item -Recurse -Force notebooks/datasens_E1_v3/data/ -ErrorAction SilentlyContinue
Write-Host "   ✅ Données temporaires supprimées"

# Nettoyer cache Python
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "   ✅ Cache Python nettoyé"

# Nettoyer checkpoints Jupyter
Get-ChildItem -Path . -Include .ipynb_checkpoints -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "   ✅ Checkpoints Jupyter nettoyés"

Write-Host "`n✅ Nettoyage terminé!" -ForegroundColor Green
Write-Host "`n📊 Statut Git:" -ForegroundColor Cyan
git status --short
