# Script de démarrage automatique pour Windows PowerShell
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🚀 Démarrage de l'application gRPC + React           ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Vérifier si protoc est installé
Write-Host "🔍 Vérification de protoc..." -ForegroundColor Yellow
$protoc = Get-Command protoc -ErrorAction SilentlyContinue
if ($null -eq $protoc) {
    Write-Host "❌ protoc n'est pas installé!" -ForegroundColor Red
    Write-Host "Installer avec: winget install Google.Protobuf" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "✅ protoc trouvé: $($protoc.Version)" -ForegroundColor Green
}

# Vérifier Python
Write-Host "🔍 Vérification de Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $python) {
    Write-Host "❌ Python n'est pas installé!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ Python trouvé" -ForegroundColor Green
}

# Vérifier Node.js
Write-Host "🔍 Vérification de Node.js..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
if ($null -eq $node) {
    Write-Host "❌ Node.js n'est pas installé!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ Node.js trouvé" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📦 Installation des dépendances Python..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

pip install grpcio grpcio-tools fastapi uvicorn

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔨 Génération des fichiers Protocol Buffers..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. users.proto

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Fichiers générés avec succès!" -ForegroundColor Green
} else {
    Write-Host "❌ Erreur lors de la génération des fichiers" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📦 Installation des dépendances Node.js..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Set-Location web-app
npm install
Set-Location ..

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🚀 Démarrage des services..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📍 Serveur gRPC       : http://localhost:50051" -ForegroundColor Magenta
Write-Host "📍 API Gateway        : http://localhost:8000" -ForegroundColor Magenta
Write-Host "📍 Frontend React     : http://localhost:3000" -ForegroundColor Magenta
Write-Host ""
Write-Host "⚠️  Ouvrez 3 terminaux séparés et exécutez:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Terminal 1: python server.py" -ForegroundColor Cyan
Write-Host "Terminal 2: uvicorn gateway:app --reload --port 8000" -ForegroundColor Cyan
Write-Host "Terminal 3: cd web-app ; npm start" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Installation terminée!" -ForegroundColor Green
Write-Host ""
