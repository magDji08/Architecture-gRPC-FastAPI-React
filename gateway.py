from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import grpc
import users_pb2
import users_pb2_grpc

app = FastAPI(
    title="Users API Gateway",
    description="REST API Gateway pour le service gRPC Users",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion au serveur gRPC
channel = grpc.insecure_channel("localhost:50051")
stub = users_pb2_grpc.UsersStub(channel)

@app.get("/")
def root():
    return {
        "message": "Users API Gateway",
        "endpoints": {
            "GET /users": "Liste tous les utilisateurs",
            "GET /users/{id}": "Récupère un utilisateur",
            "POST /users": "Crée un utilisateur",
            "PUT /users/{id}": "Met à jour un utilisateur",
            "DELETE /users/{id}": "Supprime un utilisateur"
        }
    }

@app.get("/health")
def health_check():
    """Endpoint pour vérifier la santé de l'API Gateway"""
    return {
        "service": "API Gateway",
        "status": "healthy",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }

@app.get("/health/grpc")
def grpc_health_check():
    """Endpoint pour vérifier la santé du serveur gRPC"""
    try:
        # Tenter une connexion rapide au serveur gRPC
        response = stub.ListUsers(users_pb2.ListUsersRequest(), timeout=2)
        return {
            "service": "gRPC Server",
            "status": "healthy",
            "port": 50051,
            "users_count": len(response.users),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "service": "gRPC Server",
                "status": "unhealthy",
                "port": 50051,
                "error": f"{e.code().name}: {e.details()}",
                "timestamp": __import__("datetime").datetime.now().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "service": "gRPC Server",
                "status": "unhealthy",
                "port": 50051,
                "error": str(e),
                "timestamp": __import__("datetime").datetime.now().isoformat()
            }
        )

@app.get("/users")
def list_users():
    try:
        response = stub.ListUsers(users_pb2.ListUsersRequest())
        users = [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "age": u.age,
                "email": u.email
            }
            for u in response.users
        ]
        return {"users": users}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"Erreur gRPC: {e.details()}")

@app.post("/users")
def create_user(user: dict):
    try:
        # Validation des champs requis
        required_fields = ["first_name", "last_name", "age", "email"]
        for field in required_fields:
            if field not in user:
                raise HTTPException(status_code=400, detail=f"Le champ '{field}' est requis")
        
        req = users_pb2.UserCreateRequest(
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"]
        )
        res = stub.CreateUser(req)
        return {
            "id": res.user.id,
            "first_name": res.user.first_name,
            "last_name": res.user.last_name,
            "age": res.user.age,
            "email": res.user.email
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"Erreur gRPC: {e.details()}")

@app.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        res = stub.GetUser(users_pb2.UserGetRequest(id=user_id))
        if not res.user.id:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        u = res.user
        return {
            "id": u.id,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "age": u.age,
            "email": u.email
        }
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        raise HTTPException(status_code=500, detail=f"Erreur gRPC: {e.details()}")

@app.put("/users/{user_id}")
def update_user(user_id: str, user: dict):
    try:
        req = users_pb2.UserUpdateRequest(
            id=user_id,
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"]
        )
        res = stub.UpdateUser(req)
        if not res.user.id:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        u = res.user
        return {
            "id": u.id,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "age": u.age,
            "email": u.email
        }
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        raise HTTPException(status_code=500, detail=f"Erreur gRPC: {e.details()}")

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        res = stub.DeleteUser(users_pb2.UserDeleteRequest(id=user_id))
        if not res.success:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return {"success": res.success, "message": "Utilisateur supprimé avec succès"}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"Erreur gRPC: {e.details()}")

@app.get("/services/status")
def services_status():
    """Endpoint pour obtenir le statut de tous les services"""
    services = []
    
    # Statut de l'API Gateway (toujours healthy si on peut répondre)
    services.append({
        "name": "API Gateway",
        "type": "rest",
        "status": "healthy",
        "port": 8000,
        "url": "http://localhost:8000",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    })
    
    # Statut du serveur gRPC
    try:
        response = stub.ListUsers(users_pb2.ListUsersRequest(), timeout=2)
        services.append({
            "name": "gRPC Server",
            "type": "grpc",
            "status": "healthy",
            "port": 50051,
            "url": "localhost:50051",
            "users_count": len(response.users),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        })
    except Exception as e:
        services.append({
            "name": "gRPC Server",
            "type": "grpc",
            "status": "unhealthy",
            "port": 50051,
            "url": "localhost:50051",
            "error": str(e),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        })
    
    # Statut du Frontend (on suppose qu'il est up si l'API Gateway est appelée)
    services.append({
        "name": "React Frontend",
        "type": "web",
        "status": "unknown",
        "port": 3000,
        "url": "http://localhost:3000",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    })
    
    return {"services": services}
