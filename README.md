# 🚀 Projet gRPC + React - Gestion des Utilisateurs

## 📋 Description

Application web moderne de gestion des utilisateurs utilisant une architecture microservices avec **gRPC**, **Protocol Buffers**, **FastAPI** et **React**.

### 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  React Frontend │ ─HTTP──▶│  FastAPI Gateway │ ─gRPC──▶│  gRPC Server    │
│  (Port 3000)    │         │  (Port 8000)     │         │  (Port 50051)   │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

#### Couches de l'application :

1. **Frontend (React)**
   - Interface utilisateur moderne et responsive
   - Gestion d'état avec React Hooks
   - Validation des formulaires
   - Notifications utilisateur

2. **API Gateway (FastAPI)**
   - Convertit HTTP REST → gRPC
   - Gestion CORS
   - Validation des données
   - Gestion des erreurs

3. **Backend (gRPC Server)**
   - Service Users avec CRUD complet
   - Communication via Protocol Buffers
   - Base de données en mémoire

---

## 🛠️ Technologies Utilisées

### Backend
- **Python 3.x**
- **gRPC** - Communication inter-services
- **Protocol Buffers** - Sérialisation de données
- **FastAPI** - API Gateway REST
- **Uvicorn** - Serveur ASGI

### Frontend
- **React 19.x**
- **Axios** - Client HTTP
- **CSS3** - Design moderne

---

## 📦 Prérequis

### Installation de protoc

**Windows:**
```powershell
winget install Google.Protobuf
```

**Linux:**
```bash
apt install -y protobuf-compiler
```

**macOS:**
```bash
brew install protobuf
```

Vérifier l'installation:
```bash
protoc --version  # Version 3+ requise
```

### Dépendances Python

```bash
pip install grpcio grpcio-tools fastapi uvicorn
```

### Dépendances Node.js

```bash
cd web-app
npm install
```

---

## 🚀 Démarrage de l'application

### 1. Générer les fichiers Protocol Buffers (si nécessaire)

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. users.proto
```

Cela génère:
- `users_pb2.py` - Messages Protocol Buffers
- `users_pb2_grpc.py` - Services gRPC

### 2. Démarrer le serveur gRPC

```powershell
python server.py
```
✅ Serveur démarré sur `localhost:50051`

### 3. Démarrer l'API Gateway

```powershell
uvicorn gateway:app --reload --port 8000
```
✅ API Gateway disponible sur `http://localhost:8000`

### 4. Démarrer le Frontend React

```powershell
cd web-app
npm start
```
✅ Application disponible sur `http://localhost:3000`

---

## 📁 Structure du Projet

```
grpc_users/
│
├── users.proto              # Contrat Protocol Buffers
├── users_pb2.py            # Généré: Messages Proto
├── users_pb2_grpc.py       # Généré: Services gRPC
│
├── server.py               # Serveur gRPC (port 50051)
├── gateway.py              # API Gateway REST (port 8000)
├── client.py               # Client gRPC de test
│
├── web-app/                # Application React
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.jsx         # Component principal
│       ├── App.css         # Styles
│       └── services/
│           └── api.js      # Client API REST
│
└── README.md               # Ce fichier
```

---

## 🔌 API Endpoints

### REST API (Gateway - Port 8000)

| Méthode | Endpoint          | Description                |
|---------|-------------------|----------------------------|
| GET     | `/`               | Documentation API          |
| GET     | `/users`          | Liste tous les utilisateurs|
| GET     | `/users/{id}`     | Récupère un utilisateur    |
| POST    | `/users`          | Crée un utilisateur        |
| PUT     | `/users/{id}`     | Met à jour un utilisateur  |
| DELETE  | `/users/{id}`     | Supprime un utilisateur    |

### Exemples de requêtes

**Créer un utilisateur:**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Mamadou",
    "last_name": "Diop",
    "age": 25,
    "email": "mamadou@example.com"
  }'
```

**Lister les utilisateurs:**
```bash
curl http://localhost:8000/users
```

---

## 🧪 Tester avec grpcurl

### Installation de grpcurl

**Windows:**
```powershell
winget install --id=fullstorydev.grpcurl -e
```

**macOS:**
```bash
brew install grpcurl
```

**Linux:**
```bash
sudo snap install grpcurl --edge
```

### Tester le service gRPC

**Lister les services:**
```bash
grpcurl -plaintext localhost:50051 list
```

**Créer un utilisateur:**
```bash
grpcurl -plaintext -d '{
  "first_name": "Fatou",
  "last_name": "Sall",
  "age": 30,
  "email": "fatou@example.com"
}' localhost:50051 sn.bambey.users.Users/CreateUser
```

---

## 📝 Contrat Protocol Buffers

Le fichier `users.proto` définit:

### Service Users
- `GetUser` - Récupérer un utilisateur
- `CreateUser` - Créer un utilisateur
- `UpdateUser` - Mettre à jour un utilisateur
- `DeleteUser` - Supprimer un utilisateur
- `ListUsers` - Lister tous les utilisateurs

### Message User
```protobuf
message User {
  string id = 1;
  string first_name = 2;
  string last_name = 3;
  int32 age = 4;
  string email = 5;
}
```

---

## 🎨 Features de l'Interface

✅ **CRUD complet** - Créer, Lire, Mettre à jour, Supprimer
✅ **Design responsive** - Fonctionne sur mobile et desktop
✅ **Validation des formulaires** - Email, champs requis
✅ **Gestion d'erreurs** - Messages d'erreur clairs
✅ **Notifications** - Feedback visuel des actions
✅ **Loading states** - Indicateurs de chargement
✅ **UI moderne** - Design professionnel avec animations
✅ **🆕 Monitoring en temps réel** - Statut des services actualisé toutes les 10s
✅ **🆕 Dashboard de surveillance** - Vue d'ensemble de l'architecture

---

## 🔧 Améliorations Possibles

### Backend
- [ ] Ajouter une vraie base de données (PostgreSQL, MongoDB)
- [ ] Authentification JWT
- [ ] Pagination et filtrage
- [ ] Validation avancée des données
- [ ] Logging structuré
- [ ] Tests unitaires et d'intégration

### Frontend
- [ ] Recherche et filtrage des utilisateurs
- [ ] Tri des colonnes
- [ ] Pagination
- [ ] Mode sombre
- [ ] Gestion d'état avec Redux ou Zustand
- [ ] Tests avec Jest et React Testing Library

### DevOps
- [ ] Docker Compose pour l'orchestration
- [ ] CI/CD avec GitHub Actions
- [ ] Monitoring avec Prometheus/Grafana
- [ ] Documentation API avec Swagger

---

## 📚 Ressources

- [Protocol Buffers Documentation](https://protobuf.dev/)
- [gRPC Documentation](https://grpc.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

## 👨‍🎓 Auteur

**Projet académique** - Web Avancé  
Master 2 - 2025

---

## 📄 Licence

Ce projet est à usage éducatif.
