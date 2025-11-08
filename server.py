import grpc
from concurrent import futures
import time
import users_pb2
import users_pb2_grpc

# Base de données temporaire (en mémoire)
users_db = {}

class UsersService(users_pb2_grpc.UsersServicer):
    def GetUser(self, request, context):
        user = users_db.get(request.id)
        if user:
            return users_pb2.UserGetReply(user=user)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User not found")
        return users_pb2.UserGetReply()

    def CreateUser(self, request, context):
        user_id = str(len(users_db) + 1)
        user = users_pb2.User(
            id=user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            age=request.age,
            email=request.email,
        )
        users_db[user_id] = user
        return users_pb2.UserCreateReply(user=user)

    def UpdateUser(self, request, context):
        if request.id in users_db:
            user = users_pb2.User(
                id=request.id,
                first_name=request.first_name,
                last_name=request.last_name,
                age=request.age,
                email=request.email,
            )
            users_db[request.id] = user
            return users_pb2.UserUpdateReply(user=user)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("User not found")
        return users_pb2.UserUpdateReply()

    def DeleteUser(self, request, context):
        if request.id in users_db:
            del users_db[request.id]
            return users_pb2.UserDeleteReply(success=True)
        return users_pb2.UserDeleteReply(success=False)

    def ListUsers(self, request, context):
        return users_pb2.ListUsersReply(users=list(users_db.values()))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ Serveur gRPC démarré sur le port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
