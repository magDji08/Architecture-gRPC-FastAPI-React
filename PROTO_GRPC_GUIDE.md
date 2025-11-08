# 📘 Guide Protocol Buffers & gRPC

## 🔷 Protocol Buffers (protobuf)

### Qu'est-ce que Protocol Buffers ?

Protocol Buffers est un mécanisme de **sérialisation de données structurées** développé par Google. C'est comme JSON ou XML, mais :
- ✅ **Plus rapide** (3-10x)
- ✅ **Plus petit** (binaire au lieu de texte)
- ✅ **Type-safe** (contrat fort)
- ✅ **Multi-langage** (Java, Python, Go, C++, etc.)

### Syntaxe de Base

```protobuf
syntax = "proto3";  // Version du protocole

// Package pour éviter les conflits de noms
package sn.bambey.users;

// Options pour la génération Java
option java_package = "sn.bambey.users";
option java_multiple_files = true;

// Message = Structure de données
message User {
  string id = 1;           // Numéro de champ (tag)
  string first_name = 2;
  string last_name = 3;
  int32 age = 4;
  string email = 5;
}
```

### Types de Données Protobuf

| Type Protobuf | Python     | Java       | Description           |
|---------------|------------|------------|-----------------------|
| `bool`        | bool       | boolean    | Booléen               |
| `string`      | str        | String     | Texte UTF-8           |
| `bytes`       | bytes      | ByteString | Données binaires      |
| `int32`       | int        | int        | Entier 32 bits        |
| `int64`       | int        | long       | Entier 64 bits        |
| `float`       | float      | float      | Flottant 32 bits      |
| `double`      | float      | double     | Flottant 64 bits      |

### Modificateurs

```protobuf
message Example {
  string single_value = 1;              // Valeur unique
  repeated string list_values = 2;      // Liste/Array
  optional string maybe_value = 3;      // Optionnel (peut être null)
}
```

### Énumérations

```protobuf
enum Status {
  UNKNOWN = 0;   // Toujours commencer à 0
  ACTIVE = 1;
  INACTIVE = 2;
  DELETED = 3;
}

message User {
  string id = 1;
  Status status = 2;
}
```

### Messages Imbriqués

```protobuf
message Address {
  string street = 1;
  string city = 2;
  string country = 3;
}

message User {
  string id = 1;
  string name = 2;
  Address address = 3;      // Message imbriqué
}
```

---

## 🔷 gRPC (gRPC Remote Procedure Call)

### Qu'est-ce que gRPC ?

gRPC est un framework **RPC (Remote Procedure Call)** moderne développé par Google :
- Utilise **HTTP/2** (multiplexing, streaming)
- Sérialisation via **Protocol Buffers**
- **Bidirectionnel** (streaming)
- **Multi-langage**

### Types de Services gRPC

#### 1. **Unary RPC** (Requête-Réponse simple)

```protobuf
service Users {
  rpc GetUser (UserGetRequest) returns (UserGetReply);
}
```

**Client envoie 1 requête → Serveur répond 1 fois**

```python
# Client Python
response = stub.GetUser(UserGetRequest(id="123"))
print(response.user.first_name)
```

#### 2. **Server Streaming RPC**

```protobuf
service Users {
  rpc ListUsers (ListUsersRequest) returns (stream User);
}
```

**Client envoie 1 requête → Serveur répond avec un flux**

```python
# Client Python
for user in stub.ListUsers(ListUsersRequest()):
    print(user.first_name)
```

#### 3. **Client Streaming RPC**

```protobuf
service Users {
  rpc CreateBatch (stream UserCreateRequest) returns (BatchReply);
}
```

**Client envoie un flux → Serveur répond 1 fois**

#### 4. **Bidirectional Streaming RPC**

```protobuf
service Chat {
  rpc Chat (stream Message) returns (stream Message);
}
```

**Client et serveur envoient des flux**

---

## 🛠️ Génération de Code

### Commande protoc

```bash
python -m grpc_tools.protoc \
  -I.                          # Dossier des fichiers .proto
  --python_out=.               # Génère les messages Python
  --grpc_python_out=.          # Génère les services gRPC
  users.proto                  # Fichier source
```

### Fichiers Générés

```
users.proto
  ↓
[protoc]
  ↓
├── users_pb2.py          # Messages (User, UserCreateRequest, etc.)
└── users_pb2_grpc.py     # Services (UsersServicer, UsersStub)
```

---

## 🔧 Implémentation Python

### Serveur gRPC

```python
import grpc
from concurrent import futures
import users_pb2
import users_pb2_grpc

# 1. Implémenter le service
class UsersService(users_pb2_grpc.UsersServicer):
    def GetUser(self, request, context):
        # request.id contient l'ID demandé
        user = get_user_from_db(request.id)
        
        if not user:
            # Retourner une erreur
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.UserGetReply()
        
        # Retourner la réponse
        return users_pb2.UserGetReply(user=user)

# 2. Démarrer le serveur
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

### Client gRPC

```python
import grpc
import users_pb2
import users_pb2_grpc

def run():
    # 1. Créer un channel (connexion)
    with grpc.insecure_channel('localhost:50051') as channel:
        # 2. Créer un stub (client)
        stub = users_pb2_grpc.UsersStub(channel)
        
        # 3. Appeler le service
        response = stub.GetUser(users_pb2.UserGetRequest(id="123"))
        
        # 4. Utiliser la réponse
        print(f"User: {response.user.first_name} {response.user.last_name}")

if __name__ == "__main__":
    run()
```

---

## 🔍 Comparaison REST vs gRPC

| Aspect              | REST API             | gRPC                    |
|---------------------|----------------------|-------------------------|
| **Protocol**        | HTTP/1.1             | HTTP/2                  |
| **Format**          | JSON (texte)         | Protobuf (binaire)      |
| **Performance**     | Moyen                | Rapide                  |
| **Taille**          | Grande               | Petite                  |
| **Streaming**       | Limité               | Natif                   |
| **Browser**         | ✅ Natif             | ⚠️ gRPC-Web nécessaire  |
| **Lisibilité**      | ✅ Humaine           | ❌ Binaire              |
| **Type Safety**     | ❌ Faible            | ✅ Fort                 |
| **Documentation**   | Swagger/OpenAPI      | .proto files            |

### Quand utiliser quoi ?

**REST API** :
- ✅ Applications web classiques
- ✅ APIs publiques
- ✅ Debugging facile
- ✅ Compatibilité maximale

**gRPC** :
- ✅ Microservices internes
- ✅ Communication serveur-serveur
- ✅ Performance critique
- ✅ Streaming temps réel
- ✅ Type safety important

---

## 📊 Exemple de notre Application

### 1. Définition du Contrat (users.proto)

```protobuf
syntax = "proto3";

service Users {
  rpc CreateUser (UserCreateRequest) returns (UserCreateReply);
}

message UserCreateRequest {
  string first_name = 1;
  string last_name = 2;
  int32 age = 3;
  string email = 4;
}

message UserCreateReply {
  User user = 1;
}

message User {
  string id = 1;
  string first_name = 2;
  string last_name = 3;
  int32 age = 4;
  string email = 5;
}
```

### 2. Génération du Code

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. users.proto
```

Génère :
- `users_pb2.py` - Classes Python pour User, UserCreateRequest, etc.
- `users_pb2_grpc.py` - Classes pour UsersServicer, UsersStub

### 3. Implémentation Serveur

```python
class UsersService(users_pb2_grpc.UsersServicer):
    def CreateUser(self, request, context):
        user_id = str(len(users_db) + 1)
        user = users_pb2.User(
            id=user_id,
            first_name=request.first_name,  # Depuis UserCreateRequest
            last_name=request.last_name,
            age=request.age,
            email=request.email
        )
        users_db[user_id] = user
        return users_pb2.UserCreateReply(user=user)  # Retourne UserCreateReply
```

### 4. Gateway REST → gRPC

```python
from fastapi import FastAPI

@app.post("/users")
def create_user(user: dict):
    # Conversion JSON → Protobuf
    req = users_pb2.UserCreateRequest(
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"]
    )
    
    # Appel gRPC
    res = stub.CreateUser(req)
    
    # Conversion Protobuf → JSON
    return {"id": res.user.id}
```

---

## 🔐 Gestion des Erreurs gRPC

### Codes d'Erreur

```python
from grpc import StatusCode

# OK - Succès
StatusCode.OK

# Erreurs communes
StatusCode.NOT_FOUND          # 404 - Ressource non trouvée
StatusCode.INVALID_ARGUMENT   # 400 - Argument invalide
StatusCode.ALREADY_EXISTS     # 409 - Déjà existant
StatusCode.PERMISSION_DENIED  # 403 - Permission refusée
StatusCode.UNAUTHENTICATED    # 401 - Non authentifié
StatusCode.INTERNAL           # 500 - Erreur serveur
StatusCode.UNAVAILABLE        # 503 - Service indisponible
```

### Serveur - Retourner une Erreur

```python
def GetUser(self, request, context):
    user = users_db.get(request.id)
    if not user:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(f"User {request.id} not found")
        return users_pb2.UserGetReply()
    return users_pb2.UserGetReply(user=user)
```

### Client - Gérer une Erreur

```python
try:
    response = stub.GetUser(users_pb2.UserGetRequest(id="999"))
except grpc.RpcError as e:
    print(f"Error: {e.code()} - {e.details()}")
    # Error: StatusCode.NOT_FOUND - User 999 not found
```

---

## 🚀 Avantages de notre Architecture

### 1. **Contrat Clair**
Le fichier `.proto` sert de documentation et de contrat

### 2. **Type Safety**
Impossible d'envoyer des données mal formées

### 3. **Performance**
- Binaire plus rapide que JSON
- HTTP/2 plus efficace que HTTP/1.1

### 4. **Évolutivité**
- Ajouter de nouveaux champs sans casser l'ancien code
- Compatibilité ascendante et descendante

### 5. **Multi-langage**
- Serveur en Python
- Client en Java, Go, Node.js, etc.

---

## 📚 Ressources

- [Protocol Buffers Tutorial](https://protobuf.dev/getting-started/pythontutorial/)
- [gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)
- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/)
