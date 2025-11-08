"""
Script de test complet pour le service gRPC Users
Teste toutes les opérations CRUD
"""

import grpc
import users_pb2
import users_pb2_grpc
import sys

def print_separator(title=""):
    """Affiche un séparateur visuel"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    else:
        print('-'*60)

def test_create_users(stub):
    """Test de création d'utilisateurs"""
    print_separator("✅ Test 1: Création d'utilisateurs")
    
    users_data = [
        ("Amadou", "Diop", 25, "amadou.diop@example.com"),
        ("Fatou", "Sall", 30, "fatou.sall@example.com"),
        ("Moussa", "Ba", 28, "moussa.ba@example.com"),
        ("Aïssatou", "Ndiaye", 27, "aissatou.ndiaye@example.com"),
    ]
    
    created_ids = []
    for first_name, last_name, age, email in users_data:
        try:
            response = stub.CreateUser(users_pb2.UserCreateRequest(
                first_name=first_name,
                last_name=last_name,
                age=age,
                email=email
            ))
            created_ids.append(response.user.id)
            print(f"  ✓ Créé: {first_name} {last_name} (ID: {response.user.id}, Age: {age})")
        except grpc.RpcError as e:
            print(f"  ❌ Erreur: {e.details()}")
            return []
    
    print(f"\n  📊 Total créé: {len(created_ids)} utilisateurs")
    return created_ids

def test_list_users(stub):
    """Test de listage des utilisateurs"""
    print_separator("✅ Test 2: Liste de tous les utilisateurs")
    
    try:
        response = stub.ListUsers(users_pb2.ListUsersRequest())
        users = response.users
        
        print(f"  📋 Total: {len(users)} utilisateurs dans la base\n")
        
        for i, user in enumerate(users, 1):
            print(f"  {i}. [{user.id}] {user.first_name} {user.last_name}")
            print(f"     Âge: {user.age} ans | Email: {user.email}")
        
        return users
    except grpc.RpcError as e:
        print(f"  ❌ Erreur: {e.details()}")
        return []

def test_get_user(stub, user_id):
    """Test de récupération d'un utilisateur"""
    print_separator("✅ Test 3: Récupération d'un utilisateur spécifique")
    
    try:
        response = stub.GetUser(users_pb2.UserGetRequest(id=user_id))
        user = response.user
        
        print(f"  🔍 Utilisateur trouvé:")
        print(f"     ID: {user.id}")
        print(f"     Nom: {user.first_name} {user.last_name}")
        print(f"     Âge: {user.age} ans")
        print(f"     Email: {user.email}")
        
        return user
    except grpc.RpcError as e:
        print(f"  ❌ Erreur: {e.code().name} - {e.details()}")
        return None

def test_update_user(stub, user_id, user):
    """Test de mise à jour d'un utilisateur"""
    print_separator("✅ Test 4: Mise à jour d'un utilisateur")
    
    try:
        new_age = user.age + 1
        response = stub.UpdateUser(users_pb2.UserUpdateRequest(
            id=user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            age=new_age,
            email=user.email
        ))
        
        print(f"  ✏️  Mise à jour de l'utilisateur {user_id}")
        print(f"     Âge: {user.age} → {response.user.age} ans")
        print(f"  ✓ Mise à jour réussie!")
        
        return response.user
    except grpc.RpcError as e:
        print(f"  ❌ Erreur: {e.code().name} - {e.details()}")
        return None

def test_delete_user(stub, user_id):
    """Test de suppression d'un utilisateur"""
    print_separator("✅ Test 5: Suppression d'un utilisateur")
    
    try:
        response = stub.DeleteUser(users_pb2.UserDeleteRequest(id=user_id))
        
        if response.success:
            print(f"  🗑️  Utilisateur {user_id} supprimé avec succès")
            return True
        else:
            print(f"  ❌ Échec de la suppression de l'utilisateur {user_id}")
            return False
    except grpc.RpcError as e:
        print(f"  ❌ Erreur: {e.code().name} - {e.details()}")
        return False

def test_verify_deletion(stub, user_id):
    """Vérification de la suppression"""
    print_separator("✅ Test 6: Vérification de la suppression")
    
    try:
        stub.GetUser(users_pb2.UserGetRequest(id=user_id))
        print(f"  ❌ Erreur: L'utilisateur {user_id} existe encore!")
        return False
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"  ✓ Confirmation: Utilisateur {user_id} bien supprimé")
            print(f"     Code: {e.code().name}")
            print(f"     Message: {e.details()}")
            return True
        else:
            print(f"  ❌ Erreur inattendue: {e.code().name}")
            return False

def test_error_handling(stub):
    """Test de gestion d'erreur"""
    print_separator("✅ Test 7: Gestion d'erreur (utilisateur inexistant)")
    
    try:
        stub.GetUser(users_pb2.UserGetRequest(id="99999"))
        print("  ❌ Erreur: Devrait retourner NOT_FOUND")
        return False
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"  ✓ Erreur attendue capturée:")
            print(f"     Code: {e.code().name}")
            print(f"     Message: {e.details()}")
            return True
        else:
            print(f"  ❌ Code d'erreur inattendu: {e.code().name}")
            return False

def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("  🧪 SUITE DE TESTS - Service gRPC Users")
    print("="*60)
    
    # Connexion au serveur
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = users_pb2_grpc.UsersStub(channel)
        
        # Vérifier la connexion
        stub.ListUsers(users_pb2.ListUsersRequest(), timeout=2)
        print("\n✅ Connexion au serveur gRPC établie (localhost:50051)\n")
    except grpc.RpcError as e:
        print("\n❌ Impossible de se connecter au serveur gRPC!")
        print(f"   Erreur: {e.details()}")
        print("\n⚠️  Vérifiez que le serveur est démarré:")
        print("   python server.py")
        sys.exit(1)
    
    # Compteur de succès
    tests_passed = 0
    total_tests = 7
    
    # Test 1: Créer des utilisateurs
    created_ids = test_create_users(stub)
    if created_ids:
        tests_passed += 1
    
    # Test 2: Lister les utilisateurs
    users = test_list_users(stub)
    if users:
        tests_passed += 1
    
    # Test 3: Récupérer un utilisateur
    if created_ids:
        user = test_get_user(stub, created_ids[0])
        if user:
            tests_passed += 1
            
            # Test 4: Mettre à jour
            updated_user = test_update_user(stub, created_ids[0], user)
            if updated_user:
                tests_passed += 1
        
        # Test 5: Supprimer
        if len(created_ids) > 1:
            deleted = test_delete_user(stub, created_ids[1])
            if deleted:
                tests_passed += 1
                
                # Test 6: Vérifier la suppression
                verified = test_verify_deletion(stub, created_ids[1])
                if verified:
                    tests_passed += 1
    
    # Test 7: Gestion d'erreur
    error_handled = test_error_handling(stub)
    if error_handled:
        tests_passed += 1
    
    # Résumé
    print_separator()
    print("\n" + "="*60)
    print("  📊 RÉSUMÉ DES TESTS")
    print("="*60)
    print(f"\n  Tests réussis: {tests_passed}/{total_tests}")
    print(f"  Taux de réussite: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n  🎉 TOUS LES TESTS SONT PASSÉS! 🎉")
    else:
        print(f"\n  ⚠️  {total_tests - tests_passed} test(s) ont échoué")
    
    print("\n" + "="*60 + "\n")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
