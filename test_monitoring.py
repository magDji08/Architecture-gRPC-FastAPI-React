"""
Script de test rapide pour le monitoring des services
Teste les endpoints de health check
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def print_separator(title=""):
    """Affiche un séparateur visuel"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    else:
        print('-'*60)

def test_api_gateway_health():
    """Test du health check de l'API Gateway"""
    print_separator("🌐 Test Health Check - API Gateway")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Status: {response.status_code}")
            print(f"  📊 Service: {data.get('service')}")
            print(f"  🟢 État: {data.get('status')}")
            print(f"  ⏰ Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"  ❌ Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_grpc_health():
    """Test du health check du serveur gRPC"""
    print_separator("⚡ Test Health Check - gRPC Server")
    try:
        response = requests.get(f"{BASE_URL}/health/grpc", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Status: {response.status_code}")
            print(f"  📊 Service: {data.get('service')}")
            print(f"  🟢 État: {data.get('status')}")
            print(f"  🔌 Port: {data.get('port')}")
            print(f"  👥 Utilisateurs: {data.get('users_count')}")
            print(f"  ⏰ Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"  ❌ Status: {response.status_code}")
            print(f"  ⚠️  Le serveur gRPC est probablement arrêté")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_services_status():
    """Test de l'endpoint de status de tous les services"""
    print_separator("📊 Test Status de Tous les Services")
    try:
        response = requests.get(f"{BASE_URL}/services/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', [])
            
            print(f"  ✅ Status: {response.status_code}")
            print(f"  📋 Nombre de services: {len(services)}\n")
            
            for i, service in enumerate(services, 1):
                status_icon = "✅" if service.get('status') == 'healthy' else "❌" if service.get('status') == 'unhealthy' else "❓"
                print(f"  {i}. {service.get('name')}")
                print(f"     {status_icon} Status: {service.get('status').upper()}")
                print(f"     🔌 Port: {service.get('port')}")
                print(f"     🌐 URL: {service.get('url')}")
                if service.get('users_count') is not None:
                    print(f"     👥 Utilisateurs: {service.get('users_count')}")
                if service.get('error'):
                    print(f"     ⚠️  Erreur: {service.get('error')}")
                print()
            
            # Résumé
            healthy = sum(1 for s in services if s.get('status') == 'healthy')
            unhealthy = sum(1 for s in services if s.get('status') == 'unhealthy')
            unknown = sum(1 for s in services if s.get('status') == 'unknown')
            
            print(f"  📊 Résumé:")
            print(f"     ✅ Actifs: {healthy}")
            print(f"     ❌ Inactifs: {unhealthy}")
            print(f"     ❓ Inconnus: {unknown}")
            
            return True
        else:
            print(f"  ❌ Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_monitoring_loop():
    """Test du monitoring en boucle (simulation du polling React)"""
    print_separator("🔄 Test Monitoring en Boucle (3 cycles)")
    print("  ℹ️  Simulation du polling automatique (comme dans React)")
    print("  ⏱️  Vérification toutes les 5 secondes...\n")
    
    for i in range(3):
        print(f"  📡 Cycle {i+1}/3 - {time.strftime('%H:%M:%S')}")
        try:
            response = requests.get(f"{BASE_URL}/services/status", timeout=2)
            if response.status_code == 200:
                services = response.json().get('services', [])
                healthy = sum(1 for s in services if s.get('status') == 'healthy')
                print(f"     ✅ Services actifs: {healthy}/{len(services)}")
            else:
                print(f"     ❌ Erreur HTTP: {response.status_code}")
        except Exception as e:
            print(f"     ❌ Erreur: {str(e)[:50]}")
        
        if i < 2:  # Ne pas attendre après le dernier cycle
            print(f"     ⏳ Attente de 5 secondes...")
            time.sleep(5)
        print()

def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("  🧪 TESTS DU SYSTÈME DE MONITORING")
    print("="*60)
    print(f"\n  🌐 API Gateway: {BASE_URL}")
    print(f"  ⏰ Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Vérifier que l'API Gateway est accessible
    print("  🔍 Vérification de la disponibilité de l'API Gateway...")
    try:
        response = requests.get(BASE_URL, timeout=2)
        print(f"  ✅ API Gateway accessible (Status: {response.status_code})\n")
    except requests.exceptions.RequestException:
        print("\n  ❌ ERREUR: API Gateway inaccessible!")
        print("  ⚠️  Vérifiez que le serveur est démarré:")
        print("     uvicorn gateway:app --reload --port 8000\n")
        return False
    
    # Tests individuels
    results = []
    
    results.append(("API Gateway Health", test_api_gateway_health()))
    results.append(("gRPC Server Health", test_grpc_health()))
    results.append(("Services Status", test_services_status()))
    
    # Test en boucle
    test_monitoring_loop()
    
    # Résumé final
    print_separator()
    print("\n" + "="*60)
    print("  📊 RÉSUMÉ DES TESTS")
    print("="*60 + "\n")
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"  {status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n  📈 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n  🎉 TOUS LES TESTS SONT PASSÉS!")
        print("  ✅ Le système de monitoring fonctionne parfaitement!")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) ont échoué")
        print("  💡 Vérifiez que tous les services sont démarrés:")
        print("     1. python server.py")
        print("     2. uvicorn gateway:app --reload --port 8000")
    
    print("\n" + "="*60)
    print("  ℹ️  Pour tester dans l'interface web:")
    print("     http://localhost:3000")
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n  ⚠️  Tests interrompus par l'utilisateur\n")
        exit(1)
