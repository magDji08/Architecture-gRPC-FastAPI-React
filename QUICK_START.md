# 🚀 Guide de Démarrage Rapide - Monitoring Inclus

## ⚡ Démarrage en 3 Étapes

### Étape 1: Démarrer le serveur gRPC
```powershell
# Terminal 1
python server.py
```
**Résultat attendu:**
```
✅ Serveur gRPC démarré sur le port 50051
```

---

### Étape 2: Démarrer l'API Gateway
```powershell
# Terminal 2
uvicorn gateway:app --reload --port 8000
```
**Résultat attendu:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### Étape 3: Démarrer le Frontend React
```powershell
# Terminal 3
cd web-app
npm start
```
**Résultat attendu:**
```
Compiled successfully!
You can now view web-app in the browser.
  Local:            http://localhost:3000
```

---

## 🎯 Accès à l'Application

Ouvrez votre navigateur: **http://localhost:3000**

Vous verrez:

```
╔══════════════════════════════════════════════════════════╗
║  🚀 Gestion des Utilisateurs                             ║
║  Architecture: gRPC + FastAPI + React                    ║
╚══════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────┐
│ 📊 Monitoring des Services         ✅ 2 actifs  ❌ 0     │
│ Dernière MAJ: 10:30:45               🔄 Actualiser       │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  🌐 API Gateway     ⚡ gRPC Server     💻 React Frontend │
│  ✅ HEALTHY         ✅ HEALTHY         ❓ UNKNOWN        │
│  Port: 8000         Port: 50051        Port: 3000        │
│                                                           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ ➕ Créer un utilisateur                                   │
├──────────────────────────────────────────────────────────┤
│  Prénom: [________]  Nom: [________]                     │
│  Âge: [___]  Email: [________]                           │
│  [➕ Créer]                                               │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 📋 Liste des Utilisateurs                    0 utilisateur│
├──────────────────────────────────────────────────────────┤
│  ID  │ Prénom │ Nom │ Âge │ Email │ Actions              │
│  📭 Aucun utilisateur trouvé                             │
└──────────────────────────────────────────────────────────┘
```

---

## 🧪 Test Rapide

### 1. Créer un Utilisateur

Dans le formulaire, saisir:
- **Prénom:** Amadou
- **Nom:** Diop
- **Âge:** 25
- **Email:** amadou@example.com

Cliquer sur **➕ Créer**

**Résultat:** 
```
✅ Utilisateur créé avec succès !
```

---

### 2. Observer le Monitoring

Le dashboard de monitoring se met à jour **automatiquement toutes les 10 secondes**.

**Statut normal (tous les services actifs):**
```
📊 Monitoring des Services         ✅ 2 actifs  ❌ 0
Dernière MAJ: 10:30:45

🌐 API Gateway     ⚡ gRPC Server     💻 React Frontend
✅ HEALTHY         ✅ HEALTHY         ❓ UNKNOWN
Port: 8000         Port: 50051        Port: 3000
Users: -           Users: 1           -
```

---

### 3. Tester une Panne

**Arrêter le serveur gRPC** (Ctrl+C dans Terminal 1)

**Après 10 secondes max:**
```
📊 Monitoring des Services         ✅ 1 actif  ❌ 1

🌐 API Gateway     ⚡ gRPC Server     💻 React Frontend
✅ HEALTHY         ❌ UNHEALTHY       ❓ UNKNOWN
Port: 8000         Port: 50051        Port: 3000
                   ⚠️ Erreur: Connection refused
```

**Redémarrer le serveur gRPC**
```powershell
python server.py
```

**Après 10 secondes:** Le service repasse en ✅ HEALTHY

---

## 📊 Fonctionnalités du Monitoring

### 🔄 Actualisation Automatique
- Vérification **toutes les 10 secondes**
- Pas besoin de rafraîchir la page
- Détection automatique des pannes

### 🎨 Indicateurs Visuels
- 🟢 **Vert (HEALTHY)** = Service actif
- 🔴 **Rouge (UNHEALTHY)** = Service en panne
- 🟡 **Orange (UNKNOWN)** = État inconnu

### 📈 Métriques Affichées
- **Nom du service**
- **Type** (REST, gRPC, WEB)
- **Statut** actuel
- **Port** d'écoute
- **URL** d'accès
- **Nombre d'utilisateurs** (pour gRPC)
- **Messages d'erreur** si panne
- **Horodatage** de la dernière vérification

### 🔘 Actions Disponibles
- **🔄 Actualiser** - Rafraîchir manuellement
- **Compteurs** - Services actifs/inactifs

---

## 🌐 URLs Importantes

| Service         | URL                               | Description                |
|-----------------|-----------------------------------|----------------------------|
| Frontend        | http://localhost:3000             | Interface utilisateur      |
| API Gateway     | http://localhost:8000             | API REST                   |
| API Docs        | http://localhost:8000/docs        | Documentation Swagger      |
| Health Gateway  | http://localhost:8000/health      | Status API Gateway         |
| Health gRPC     | http://localhost:8000/health/grpc | Status serveur gRPC        |
| Services Status | http://localhost:8000/services/status | Status tous services   |

---

## 🧪 Tests avec cURL

### Tester le monitoring depuis le terminal

**Status de tous les services:**
```powershell
curl http://localhost:8000/services/status
```

**Health de l'API Gateway:**
```powershell
curl http://localhost:8000/health
```

**Health du serveur gRPC:**
```powershell
curl http://localhost:8000/health/grpc
```

---

## 🐛 Dépannage Rapide

### Problème: Service en rouge ❌

**Solution:**
1. Vérifier que le service est démarré
2. Vérifier le port (8000 ou 50051)
3. Regarder les logs dans le terminal
4. Redémarrer le service

### Problème: Monitoring ne se met pas à jour

**Solution:**
1. Vérifier la connexion réseau
2. Ouvrir la console du navigateur (F12)
3. Regarder les erreurs dans Console
4. Cliquer sur "🔄 Actualiser" manuellement

### Problème: Erreur CORS

**Solution:**
1. Vérifier que `gateway.py` contient le middleware CORS
2. Redémarrer l'API Gateway
3. Vider le cache du navigateur (Ctrl+Shift+Del)

---

## ✅ Checklist de Démarrage

- [ ] Python installé (python --version)
- [ ] Node.js installé (node --version)
- [ ] protoc installé (protoc --version)
- [ ] Dépendances Python installées (pip install grpcio grpcio-tools fastapi uvicorn)
- [ ] Dépendances React installées (cd web-app && npm install)
- [ ] Fichiers proto générés (users_pb2.py, users_pb2_grpc.py)
- [ ] Serveur gRPC démarré ✅
- [ ] API Gateway démarrée ✅
- [ ] Frontend React démarré ✅
- [ ] Application accessible sur http://localhost:3000 ✅
- [ ] Monitoring visible et fonctionnel ✅

---

## 🎯 Utilisation Typique

### Workflow Normal

1. **Démarrer** les 3 services (gRPC, Gateway, React)
2. **Ouvrir** http://localhost:3000
3. **Vérifier** que le monitoring affiche tout en vert ✅
4. **Créer** des utilisateurs via le formulaire
5. **Observer** le monitoring qui affiche le nombre d'utilisateurs
6. **Modifier/Supprimer** des utilisateurs
7. **Utiliser** le monitoring pour surveiller l'état des services

### Démonstration

1. **Montrer** l'interface avec monitoring
2. **Créer** quelques utilisateurs
3. **Arrêter** le serveur gRPC volontairement
4. **Montrer** que le monitoring détecte la panne (rouge ❌)
5. **Redémarrer** le serveur gRPC
6. **Montrer** que le monitoring détecte le retour (vert ✅)
7. **Expliquer** l'architecture microservices

---

## 📚 Documentation Complète

Pour plus de détails, consultez:

| Fichier             | Contenu                                |
|---------------------|----------------------------------------|
| README.md           | Documentation générale                 |
| MONITORING.md       | Guide complet du monitoring            |
| ARCHITECTURE.md     | Diagrammes d'architecture              |
| QUICK_COMMANDS.md   | Commandes utiles                       |
| TESTING.md          | Guide de tests                         |

---

## 🎉 Résultat

Vous avez maintenant une **application web complète** avec:

✅ **CRUD** des utilisateurs  
✅ **Architecture microservices** (gRPC + REST)  
✅ **Interface moderne** React  
✅ **Monitoring en temps réel** des services  
✅ **Détection automatique** des pannes  
✅ **Dashboard professionnel** avec métriques  

**L'application est prête à être utilisée, démontrée ou déployée!** 🚀
