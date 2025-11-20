# 🚀 Script Push vers GitHub - DataSens

Write-Host "`n🚀 TRANSMISSION DATASENS VERS GITHUB`n" -ForegroundColor Green

# 1. Nettoyage
Write-Host "1️⃣ Nettoyage projet..." -ForegroundColor Cyan
& "$PSScriptRoot\clean_before_push.ps1"

# 2. Status
Write-Host "`n2️⃣ Vérification status..." -ForegroundColor Cyan
Write-Host "Repository: https://github.com/ALMAGNUS/datasens.git" -ForegroundColor Yellow
Write-Host "Branche: $(git branch --show-current)" -ForegroundColor Yellow

$fileCount = (git status --short | Measure-Object -Line).Lines
Write-Host "Fichiers modifiés: $fileCount" -ForegroundColor Yellow

# 3. Confirmation
Write-Host "`n3️⃣ Prêt à commiter et pusher?" -ForegroundColor Cyan
$confirm = Read-Host "Continuer? (O/N)"

if ($confirm -ne "O" -and $confirm -ne "o") {
    Write-Host "❌ Annulé" -ForegroundColor Red
    exit
}

# 4. Add all
Write-Host "`n4️⃣ Git add..." -ForegroundColor Cyan
git add .
Write-Host "   ✅ Fichiers ajoutés" -ForegroundColor Green

# 5. Commit
Write-Host "`n5️⃣ Git commit..." -ForegroundColor Cyan
$commitMsg = "feat: Production-ready DataSens - Phase 2 refactoring + GDELT BigData + ML Annotations (SpaCy NER + YAKE)"
git commit -m $commitMsg
Write-Host "   ✅ Commit créé" -ForegroundColor Green

# 6. Push
Write-Host "`n6️⃣ Git push..." -ForegroundColor Cyan
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ PUSH RÉUSSI!" -ForegroundColor Green
    Write-Host "`n📦 Repository disponible à:" -ForegroundColor Cyan
    Write-Host "   https://github.com/ALMAGNUS/datasens" -ForegroundColor Yellow
    Write-Host "`n📧 Partagez cette URL avec le client!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Erreur push. Vérifier credentials GitHub." -ForegroundColor Red
    Write-Host "   Solution: git config credential.helper store" -ForegroundColor Yellow
}

Write-Host "`n🎯 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "   1. Vérifier sur GitHub: https://github.com/ALMAGNUS/datasens"
Write-Host "   2. Envoyer URL au client"
Write-Host "   3. Client fait: git clone https://github.com/ALMAGNUS/datasens.git"
Write-Host "`n✅ Transmission complète!" -ForegroundColor Green
