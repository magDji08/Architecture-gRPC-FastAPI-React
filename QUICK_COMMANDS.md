# ⚡ Commandes Rapides - Aide Mémoire

## 🚀 Démarrage Rapide

### Option 1: Installation Automatique
```powershell
# Exécuter le script d'installation
.\start.ps1
```

### Option 2: Manuel (Étape par étape)

```powershell
# 1. Installer protoc
winget install Google.Protobuf

# 2. Installer dépendances Python
pip install grpcio grpcio-tools fastapi uvicorn

# 3. Générer les fichiers Proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. users.proto

# 4. Installer dépendances React
cd web-app
npm install
cd ..
```

---

## 🔧 Lancement des Services

### Serveur gRPC (Terminal 1)
```powershell
python server.py
```

### API Gateway (Terminal 2)
```powershell
uvicorn gateway:app --reload --port 8000
```

### Frontend React (Terminal 3)
```powershell
cd web-app
npm start
```

---

## 🧪 Tests

### Tests Automatiques
```powershell
python test_users.py
```

### Client gRPC de Test
```powershell
python client.py
```

---

## 🔍 Tests avec grpcurl

### Liste des services
```bash
grpcurl -plaintext localhost:50051 list
```

### Créer un utilisateur
```bash
grpcurl -plaintext -d '{"first_name":"John","last_name":"Doe","age":30,"email":"john@example.com"}' localhost:50051 sn.bambey.users.Users/CreateUser
```

### Lister les utilisateurs
```bash
grpcurl -plaintext -d '{}' localhost:50051 sn.bambey.users.Users/ListUsers
```

### Récupérer un utilisateur
```bash
grpcurl -plaintext -d '{"id":"1"}' localhost:50051 sn.bambey.users.Users/GetUser
```

### Mettre à jour
```bash
grpcurl -plaintext -d '{"id":"1","first_name":"Jane","last_name":"Doe","age":31,"email":"jane@example.com"}' localhost:50051 sn.bambey.users.Users/UpdateUser
```

### Supprimer
```bash
grpcurl -plaintext -d '{"id":"1"}' localhost:50051 sn.bambey.users.Users/DeleteUser
```

---

## 🌐 Tests API REST (cURL)

### Liste
```bash
curl http://localhost:8000/users
```

### Créer
```bash
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"first_name":"Alice","last_name":"Smith","age":28,"email":"alice@example.com"}'
```

### Récupérer
```bash
curl http://localhost:8000/users/1
```

### Mettre à jour
```bash
curl -X PUT http://localhost:8000/users/1 -H "Content-Type: application/json" -d '{"first_name":"Alice","last_name":"Johnson","age":29,"email":"alice@example.com"}'
```

### Supprimer
```bash
curl -X DELETE http://localhost:8000/users/1
```

---

## 💻 Tests PowerShell

### Liste
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/users" -Method Get
```

### Créer
```powershell
$body = @{first_name="Bob";last_name="Wilson";age=35;email="bob@example.com"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/users" -Method Post -Body $body -ContentType "application/json"
```

### Mettre à jour
```powershell
$body = @{first_name="Bob";last_name="Wilson";age=36;email="bob@example.com"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method Put -Body $body -ContentType "application/json"
```

### Supprimer
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method Delete
```

---

## 🔨 Régénération des Fichiers Proto

```powershell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. users.proto
```

---

## 📦 Nettoyage

### Arrêter tous les services
```powershell
# Ctrl+C dans chaque terminal
```

### Supprimer les fichiers générés
```powershell
Remove-Item users_pb2.py, users_pb2_grpc.py, __pycache__ -Recurse -Force
```

### Réinstaller les dépendances
```powershell
pip install --upgrade grpcio grpcio-tools fastapi uvicorn
cd web-app
npm install
```

---

## 🐛 Dépannage

### Erreur: protoc non trouvé
```powershell
winget install Google.Protobuf
# Redémarrer le terminal
protoc --version
```

### Erreur: Module grpc non trouvé
```powershell
pip install grpcio grpcio-tools
```

### Erreur: Port déjà utilisé (50051)
```powershell
# Trouver le processus
netstat -ano | findstr :50051
# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F
```

### Erreur: Port déjà utilisé (8000)
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erreur: CORS
Vérifier que `gateway.py` contient:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📍 URLs Importantes

| Service         | URL                          |
|-----------------|------------------------------|
| Frontend        | http://localhost:3000        |
| API Gateway     | http://localhost:8000        |
| API Docs        | http://localhost:8000/docs   |
| gRPC Server     | localhost:50051              |

---

## 📊 Vérification de l'État

### Vérifier les ports
```powershell
netstat -ano | findstr "3000 8000 50051"
```

### Tester la connectivité gRPC
```bash
grpcurl -plaintext localhost:50051 list
```

### Tester l'API REST
```powershell
curl http://localhost:8000/
```

### Tester le Frontend
Ouvrir dans le navigateur: http://localhost:3000

---

## 📚 Documentation

| Fichier                | Description                       |
|------------------------|-----------------------------------|
| README.md              | Documentation principale          |
| ARCHITECTURE.md        | Diagrammes et architecture        |
| PROTO_GRPC_GUIDE.md    | Guide Protocol Buffers & gRPC     |
| TESTING.md             | Guide de tests détaillé           |
| RAPPORT.md             | Rapport final du projet           |
| QUICK_COMMANDS.md      | Ce fichier (aide-mémoire)         |

---

## ⌨️ Raccourcis Utiles

### VS Code
- `Ctrl+Shift+P` - Palette de commandes
- `Ctrl+J` - Toggle terminal
- `Ctrl+B` - Toggle sidebar

### Terminal
- `Ctrl+C` - Arrêter un processus
- `Ctrl+L` ou `cls` - Effacer l'écran
- `Tab` - Autocomplétion

---

## 🎯 Workflow Typique

1. **Démarrer les services**
   ```powershell
   # Terminal 1
   python server.py
   
   # Terminal 2
   uvicorn gateway:app --reload --port 8000
   
   # Terminal 3
   cd web-app; npm start
   ```

2. **Ouvrir le navigateur**
   ```
   http://localhost:3000
   ```

3. **Tester l'application**
   - Créer des utilisateurs
   - Modifier
   - Supprimer
   - Vérifier la liste

4. **Tests automatiques**
   ```powershell
   python test_users.py
   ```

5. **Arrêter proprement**
   - `Ctrl+C` dans chaque terminal

---

## 🔄 Mise à Jour du Code

### Après modification du .proto
```powershell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. users.proto
# Redémarrer server.py et gateway.py
```

### Après modification du backend Python
```powershell
# Le serveur se recharge automatiquement avec --reload
# Sinon, Ctrl+C et relancer
```

### Après modification du frontend
```powershell
# React recharge automatiquement
# Si besoin: Ctrl+C et npm start
```

---

## 💾 Sauvegarde du Projet

```powershell
# Créer une archive
Compress-Archive -Path grpc_users -DestinationPath grpc_users_backup.zip

# Ou utiliser Git
git init
git add .
git commit -m "Initial commit"
```

---

## ✅ Checklist de Validation

- [ ] protoc installé et fonctionnel
- [ ] Dépendances Python installées
- [ ] Dépendances Node.js installées
- [ ] Fichiers Proto générés (users_pb2.py, users_pb2_grpc.py)
- [ ] Serveur gRPC démarre sans erreur
- [ ] API Gateway démarre sans erreur
- [ ] Frontend React démarre sans erreur
- [ ] Tests automatiques passent (7/7)
- [ ] Interface web accessible et fonctionnelle
- [ ] CRUD complet fonctionne

---

## 📞 Aide

En cas de problème:
1. Vérifier que tous les services sont démarrés
2. Consulter les logs dans les terminaux
3. Vérifier les ports avec `netstat`
4. Relire la documentation (README.md)
5. Tester avec grpcurl/curl
