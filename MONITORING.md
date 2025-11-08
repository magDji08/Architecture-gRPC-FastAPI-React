# 📊 Monitoring des Services en Temps Réel

## 🎯 Objectif

Cette fonctionnalité permet de surveiller l'état de tous les services de l'application en temps réel directement depuis l'interface web React.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              React Frontend (Port 3000)             │
│                                                     │
│  ┌─────────────────────────────────────┐          │
│  │     ServiceMonitor Component        │          │
│  │                                     │          │
│  │  • Polling toutes les 10 secondes  │          │
│  │  • Affichage visuel de l'état      │          │
│  │  • Indicateurs colorés             │          │
│  └──────────────┬──────────────────────┘          │
└─────────────────┼────────────────────────────────────┘
                  │
                  │ HTTP GET /services/status
                  │ Toutes les 10 secondes
                  ▼
┌─────────────────────────────────────────────────────┐
│         FastAPI Gateway (Port 8000)                 │
│                                                     │
│  Endpoints:                                        │
│  • GET /health           → Statut Gateway         │
│  • GET /health/grpc      → Statut gRPC Server     │
│  • GET /services/status  → Statut de tous         │
│                                                     │
│  └─────────┬─────────────────────────────────────┘│
└────────────┼───────────────────────────────────────┘
             │
             │ gRPC ListUsers (timeout 2s)
             │ Pour tester la connexion
             ▼
┌─────────────────────────────────────────────────────┐
│          gRPC Server (Port 50051)                   │
│                                                     │
│  • Répond aux requêtes de test                    │
│  • Retourne le nombre d'utilisateurs              │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Composants Créés

### 1. Backend - Endpoints de Monitoring (`gateway.py`)

#### **GET /health**
Vérifie la santé de l'API Gateway
```json
{
  "service": "API Gateway",
  "status": "healthy",
  "timestamp": "2025-11-08T10:30:45.123456"
}
```

#### **GET /health/grpc**
Vérifie la santé du serveur gRPC
```json
{
  "service": "gRPC Server",
  "status": "healthy",
  "port": 50051,
  "users_count": 5,
  "timestamp": "2025-11-08T10:30:45.123456"
}
```

#### **GET /services/status**
Retourne le statut de tous les services
```json
{
  "services": [
    {
      "name": "API Gateway",
      "type": "rest",
      "status": "healthy",
      "port": 8000,
      "url": "http://localhost:8000",
      "timestamp": "2025-11-08T10:30:45.123456"
    },
    {
      "name": "gRPC Server",
      "type": "grpc",
      "status": "healthy",
      "port": 50051,
      "url": "localhost:50051",
      "users_count": 5,
      "timestamp": "2025-11-08T10:30:45.123456"
    },
    {
      "name": "React Frontend",
      "type": "web",
      "status": "unknown",
      "port": 3000,
      "url": "http://localhost:3000",
      "timestamp": "2025-11-08T10:30:45.123456"
    }
  ]
}
```

### 2. Frontend - API Client (`api.js`)

Nouvelles fonctions ajoutées :
```javascript
export const getServicesStatus = () => api.get("/services/status");
export const checkGatewayHealth = () => api.get("/health");
export const checkGrpcHealth = () => api.get("/health/grpc");
```

### 3. Frontend - Composant ServiceMonitor

**Fichiers:**
- `src/components/ServiceMonitor.jsx` - Composant React
- `src/components/ServiceMonitor.css` - Styles

**Fonctionnalités:**
- ✅ Affichage en grille des services
- ✅ Indicateurs visuels colorés (vert/rouge/orange)
- ✅ Polling automatique toutes les 10 secondes
- ✅ Bouton de rafraîchissement manuel
- ✅ Affichage de l'heure de dernière mise à jour
- ✅ Compteur de services actifs/inactifs
- ✅ Détails de chaque service (port, URL, erreurs)
- ✅ Animation de pulsation pour les services actifs
- ✅ Design responsive

---

## 🎨 Interface Utilisateur

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Monitoring des Services     ✅ 3 actifs  ❌ 0 inactifs  │
│  Dernière mise à jour: 10:30:45           🔄 Actualiser      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 🌐 API       │  │ ⚡ gRPC       │  │ 💻 React     │     │
│  │ Gateway      │  │ Server       │  │ Frontend     │     │
│  │              │  │              │  │              │     │
│  │ ✅ HEALTHY   │  │ ✅ HEALTHY   │  │ ❓ UNKNOWN   │     │
│  │              │  │              │  │              │     │
│  │ Type: REST   │  │ Type: GRPC   │  │ Type: WEB    │     │
│  │ Port: 8000   │  │ Port: 50051  │  │ Port: 3000   │     │
│  │ URL: http:// │  │ URL: local.. │  │ URL: http:// │     │
│  │ localhost... │  │              │  │ localhost... │     │
│  │              │  │ Users: 5     │  │              │     │
│  │ ● 10:30:45   │  │ ● 10:30:45   │  │ ● 10:30:45   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ℹ️ Les services sont vérifiés automatiquement toutes     │
│     les 10 secondes                                         │
└─────────────────────────────────────────────────────────────┘
```

### Codes Couleur

- 🟢 **Vert (HEALTHY)**: Service actif et fonctionnel
- 🔴 **Rouge (UNHEALTHY)**: Service inactif ou en erreur
- 🟡 **Orange (UNKNOWN)**: État inconnu

---

## 🔄 Fonctionnement

### 1. Polling Automatique

```javascript
useEffect(() => {
  // Récupération initiale
  fetchServicesStatus();

  // Récupération toutes les 10 secondes
  const interval = setInterval(() => {
    fetchServicesStatus();
  }, 10000);

  // Nettoyage
  return () => clearInterval(interval);
}, []);
```

### 2. Gestion des Erreurs

Si l'API Gateway est inaccessible, le composant affiche automatiquement tous les services comme "unhealthy" avec un message d'erreur.

### 3. Test de Connexion gRPC

L'API Gateway teste la connexion au serveur gRPC en appelant `ListUsers` avec un timeout de 2 secondes :

```python
try:
    response = stub.ListUsers(users_pb2.ListUsersRequest(), timeout=2)
    # Service OK
except grpc.RpcError:
    # Service KO
```

---

## 🚀 Utilisation

### Démarrage

1. **Démarrer le serveur gRPC:**
   ```powershell
   python server.py
   ```

2. **Démarrer l'API Gateway:**
   ```powershell
   uvicorn gateway:app --reload --port 8000
   ```

3. **Démarrer le Frontend:**
   ```powershell
   cd web-app
   npm start
   ```

4. **Accéder à l'application:**
   ```
   http://localhost:3000
   ```

Le dashboard de monitoring s'affiche automatiquement en haut de la page.

---

## 🧪 Tests

### Test Manuel - Arrêter un Service

1. **Arrêter le serveur gRPC** (Ctrl+C dans son terminal)
2. **Observer le dashboard React** (dans les 10 secondes):
   - Le service "gRPC Server" passe en rouge ❌
   - Un message d'erreur s'affiche
   - Le compteur de services actifs diminue

3. **Redémarrer le serveur gRPC**
4. **Observer le dashboard** (dans les 10 secondes):
   - Le service "gRPC Server" repasse en vert ✅
   - Le compteur de services actifs augmente

### Test avec cURL

**Vérifier le statut des services:**
```bash
curl http://localhost:8000/services/status
```

**Vérifier l'API Gateway:**
```bash
curl http://localhost:8000/health
```

**Vérifier le serveur gRPC:**
```bash
curl http://localhost:8000/health/grpc
```

---

## 📊 Métriques Affichées

### Pour chaque service:

| Métrique       | Description                           |
|----------------|---------------------------------------|
| **Nom**        | Nom du service                        |
| **Type**       | Type (REST, gRPC, WEB)                |
| **Statut**     | État actuel (healthy/unhealthy)       |
| **Port**       | Port d'écoute                         |
| **URL**        | Adresse d'accès                       |
| **Timestamp**  | Heure de dernière vérification        |
| **Users**      | Nombre d'utilisateurs (gRPC seulement)|
| **Erreur**     | Message d'erreur si échec             |

---

## 🎯 Scénarios d'Utilisation

### Scénario 1: Développement
- Vérifier que tous les services sont lancés
- Détecter rapidement un service qui plante
- Débugger les problèmes de connexion

### Scénario 2: Démo
- Montrer l'architecture distribuée
- Illustrer la communication entre services
- Démontrer la résilience de l'application

### Scénario 3: Production (futur)
- Monitoring en temps réel
- Alertes en cas de panne
- Métriques de disponibilité

---

## 🔧 Personnalisation

### Changer l'intervalle de polling

Dans `ServiceMonitor.jsx`:
```javascript
const interval = setInterval(() => {
  fetchServicesStatus();
}, 5000); // 5 secondes au lieu de 10
```

### Ajouter un nouveau service

Dans `gateway.py`:
```python
services.append({
    "name": "Base de données",
    "type": "database",
    "status": "healthy",
    "port": 5432,
    "url": "localhost:5432"
})
```

---

## 📈 Améliorations Futures

- [ ] **Graphiques de disponibilité** sur 24h
- [ ] **Notifications push** en cas de panne
- [ ] **Historique des états** des services
- [ ] **Temps de réponse** moyen de chaque service
- [ ] **Métriques CPU/RAM** des services
- [ ] **Logs en temps réel** dans l'interface
- [ ] **Alertes par email/Slack** en cas de problème
- [ ] **Dashboard admin** dédié au monitoring

---

## 🎓 Concepts Démontrés

✅ **Polling HTTP** régulier depuis le frontend  
✅ **Health checks** pour services distribués  
✅ **Monitoring en temps réel** avec React  
✅ **useEffect** et cleanup avec intervalles  
✅ **Gestion d'état** avec useState  
✅ **Communication HTTP** entre frontend et backend  
✅ **Test de connexion gRPC** avec timeout  
✅ **UI/UX moderne** avec indicateurs visuels  
✅ **Design responsive** et animations CSS  

---

## 🏆 Résultat

L'application dispose maintenant d'un **système de monitoring complet** qui permet de:
- ✅ Voir l'état de tous les services en temps réel
- ✅ Détecter automatiquement les pannes
- ✅ Avoir une vue d'ensemble de l'architecture
- ✅ Faciliter le debugging et le développement

**Cette fonctionnalité transforme l'application en un véritable système distribué professionnel avec monitoring intégré!** 🎉
