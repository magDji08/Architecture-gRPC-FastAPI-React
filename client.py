import grpc
import users_pb2
import users_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        # 1️⃣ Créer un utilisateur
        print("\n==> Création d’un utilisateur")
        create_response = stub.CreateUser(users_pb2.UserCreateRequest(
            first_name="Mamadou",
            last_name="Gueye",
            age=25,
            email="mamadou@example.com"
        ))
        print("Utilisateur créé :", create_response.user)

        # 2️⃣ Récupérer cet utilisateur
        print("\n==> Récupération de l’utilisateur")
        user_id = create_response.user.id
        get_response = stub.GetUser(users_pb2.UserGetRequest(id=user_id))
        print("Utilisateur récupéré :", get_response.user)

        # 3️⃣ Lister tous les utilisateurs
        print("\n==> Liste des utilisateurs")
        list_response = stub.ListUsers(users_pb2.ListUsersRequest())
        for u in list_response.users:
            print(f"- {u.first_name} {u.last_name}, {u.email}")

if __name__ == "__main__":
    run()
