#!/usr/bin/env python3
"""
Script d'initialisation Elasticsearch pour le projet MCP
Ce script configure un conteneur Elasticsearch, crée l'index artik_employees
et l'alimente avec les données du fichier liste_noms_age_v2.json
"""

import json
import time
import subprocess
import sys
import os
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth

# Configuration
ELASTICSEARCH_CONTAINER = "artik-elasticsearch"
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_URL = f"http://localhost:{ELASTICSEARCH_PORT}"
INDEX_NAME = "artik_employees"
DATA_FILE = Path(__file__).parent.parent / "data" / "liste_noms_age_v2.json"

def check_docker():
    """Vérifie si Docker est disponible"""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker n'est pas installé ou n'est pas dans le PATH")
        return False

def is_container_running(container_name):
    """Vérifie si un conteneur est en cours d'exécution"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
            check=True, capture_output=True, text=True
        )
        return container_name in result.stdout
    except subprocess.CalledProcessError:
        return False

def is_elasticsearch_responsive():
    """Vérifie si Elasticsearch répond déjà sur le port local"""
    try:
        response = requests.get(f"{ELASTICSEARCH_URL}/_cluster/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_elasticsearch():
    """Démarre le conteneur Elasticsearch"""
    print(f"🚀 Démarrage du conteneur Elasticsearch '{ELASTICSEARCH_CONTAINER}'...")
    
    # Arrêter le conteneur s'il existe déjà
    try:
        subprocess.run(["docker", "stop", ELASTICSEARCH_CONTAINER], check=False, capture_output=True)
        subprocess.run(["docker", "rm", ELASTICSEARCH_CONTAINER], check=False, capture_output=True)
    except:
        pass
    
    # Démarrer le nouveau conteneur
    cmd = [
        "docker", "run", "-d",
        "--name", ELASTICSEARCH_CONTAINER,
        "-p", f"{ELASTICSEARCH_PORT}:{ELASTICSEARCH_PORT}",
        "-e", "discovery.type=single-node",
        "-e", "xpack.security.enabled=false",
        "-e", "xpack.security.enrollment.enabled=false",
        "docker.elastic.co/elasticsearch/elasticsearch:8.15.0"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Conteneur Elasticsearch démarré")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du démarrage d'Elasticsearch: {e}")
        print("💡 Si vous avez des erreurs de permissions Docker, essayez:")
        print("   sudo usermod -aG docker $USER")
        print("   newgrp docker")
        print("   ou exécutez: sudo python3 scripts/setup_elasticsearch.py")
        return False

def wait_for_elasticsearch(max_wait=120):
    """Attend qu'Elasticsearch soit prêt"""
    print(f"⏳ Attente du démarrage d'Elasticsearch (timeout: {max_wait}s)...")
    
    for i in range(max_wait):
        try:
            response = requests.get(f"{ELASTICSEARCH_URL}/_cluster/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                status = health.get('status')
                if status in ['yellow', 'green']:
                    nodes = health.get('number_of_nodes', 0)
                    print(f"✅ Elasticsearch est prêt (status: {status}, nodes: {nodes})")
                    return True
                else:
                    if i % 15 == 0:
                        print(f"   Status actuel: {status} - attente de 'yellow' ou 'green'...")
            else:
                if i % 15 == 0:
                    print(f"   Réponse HTTP {response.status_code} - Elasticsearch démarre...")
        except requests.exceptions.RequestException as e:
            if i % 15 == 0:
                print(f"   Connexion en cours... (tentative {i+1}/{max_wait})")
        
        time.sleep(1)
    
    print(f"❌ Elasticsearch n'a pas démarré dans les {max_wait} secondes imparties")
    print("💡 Suggestions:")
    print("   - Vérifiez les logs du conteneur: docker logs artik-elasticsearch")
    print("   - Essayez d'augmenter le timeout ou redémarrez le conteneur")
    return False

def create_index():
    """Crée l'index artik_employees avec le mapping approprié"""
    print(f"📋 Préparation de l'index '{INDEX_NAME}'...")
    
    mapping = {
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "age": {
                    "type": "integer"
                }
            }
        }
    }
    
    try:
        # Vérifier d'abord si l'index existe
        check_response = requests.get(f"{ELASTICSEARCH_URL}/{INDEX_NAME}")
        if check_response.status_code == 200:
            print(f"✅ L'index '{INDEX_NAME}' existe déjà")
            
            # Vérifier si les données sont déjà présentes
            count_response = requests.get(f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_count")
            if count_response.status_code == 200:
                count = count_response.json().get('count', 0)
                if count > 0:
                    print(f"   📊 L'index contient déjà {count} documents")
                    return True
                else:
                    print("   📋 L'index existe mais est vide, prêt pour l'indexation")
                    return True
            else:
                print(f"   ⚠️  Impossible de vérifier le nombre de documents, mais l'index existe")
                return True
        
        # Créer l'index s'il n'existe pas
        response = requests.put(
            f"{ELASTICSEARCH_URL}/{INDEX_NAME}",
            json=mapping,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Index '{INDEX_NAME}' créé avec succès")
            return True
        else:
            print(f"❌ Erreur lors de la création de l'index: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à Elasticsearch: {e}")
        return False

def index_data():
    """Indexe les données du fichier JSON"""
    print(f"📊 Indexation des données depuis '{DATA_FILE}'...")
    
    if not DATA_FILE.exists():
        print(f"❌ Fichier de données non trouvé: {DATA_FILE}")
        print("💡 Vérifiez que le fichier existe dans le répertoire 'data/'")
        return False
    
    # Vérifier si l'index contient déjà des données
    try:
        count_response = requests.get(f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_count", timeout=10)
        if count_response.status_code == 200:
            existing_count = count_response.json().get('count', 0)
            if existing_count > 0:
                print(f"   ⚠️  L'index contient déjà {existing_count} documents")
                print("   🔄 Options disponibles:")
                print("      1. Conserver les données existantes (recommandé)")
                print("      2. Supprimer toutes les données et réindexer")
                
                # Pour l'instant, on conserve les données existantes
                print("   ✅ Conservation des données existantes")
                print(f"   📊 Total actuel: {existing_count} documents")
                return True
    except requests.exceptions.RequestException:
        pass  # Continuer avec l'indexation normale en cas d'erreur
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validation du format des données
        if not isinstance(data, dict):
            print("❌ Le fichier JSON doit contenir un objet avec la clé 'personne'")
            return False
            
        personnes = data.get('personne', [])
        if not isinstance(personnes, list):
            print("❌ La clé 'personne' doit contenir une liste d'objets")
            return False
        
        print(f"   📋 {len(personnes)} enregistrements trouvés dans le fichier")
        
        if len(personnes) == 0:
            print("⚠️  Le fichier ne contient aucun enregistrement à indexer")
            return True  # Considérer comme succès car rien à faire
        
        # Validation des données individuelles
        valid_records = 0
        for i, personne in enumerate(personnes):
            if not isinstance(personne, dict):
                print(f"   ⚠️  Enregistrement {i+1} invalide (n'est pas un objet)")
                continue
            if not personne.get('name') or not isinstance(personne.get('name'), str):
                print(f"   ⚠️  Enregistrement {i+1} invalide (nom manquant ou invalide)")
                continue
            if not isinstance(personne.get('age'), int):
                print(f"   ⚠️  Enregistrement {i+1} invalide (âge manquant ou invalide)")
                continue
            valid_records += 1
        
        if valid_records == 0:
            print("❌ Aucun enregistrement valide trouvé dans le fichier")
            return False
        
        if valid_records < len(personnes):
            print(f"   ⚠️  Seuls {valid_records} enregistrements valides sur {len(personnes)} seront indexés")
        
        # Préparer les documents pour l'indexation en bulk
        bulk_body = []
        for personne in personnes:
            if isinstance(personne, dict) and personne.get('name') and isinstance(personne.get('age'), int):
                # Index action
                bulk_body.append({
                    "index": {"_index": INDEX_NAME}
                })
                # Document
                bulk_body.append(personne)
        
        print(f"   🚀 Préparation de l'indexation de {len(bulk_body)//2} documents valides...")
        
        # Envoyer en bulk
        bulk_data = '\n'.join([json.dumps(item) for item in bulk_body]) + '\n'
        
        response = requests.post(
            f"{ELASTICSEARCH_URL}/_bulk",
            data=bulk_data,
            headers={"Content-Type": "application/x-ndjson"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            items = result.get('items', [])
            
            # Analyse détaillée des résultats
            successful = 0
            errors = 0
            error_details = []
            
            for item in items:
                if 'index' in item:
                    if item['index'].get('result') == 'created':
                        successful += 1
                    elif 'error' in item['index']:
                        errors += 1
                        error_info = item['index']['error']
                        error_details.append(f"   - {error_info.get('type', 'Unknown')}: {error_info.get('reason', 'No reason')}")
            
            print(f"✅ {successful} documents indexés avec succès")
            
            if errors > 0:
                print(f"⚠️  {errors} erreurs lors de l'indexation:")
                # Afficher seulement les 3 premières erreurs pour ne pas surcharger
                for error in error_details[:3]:
                    print(error)
                if len(error_details) > 3:
                    print(f"   ... et {len(error_details) - 3} autres erreurs")
            
            if successful == 0:
                print("❌ Aucun document n'a pu être indexé")
                return False
            
            return True
        else:
            print(f"❌ Erreur HTTP lors de l'indexation: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de lecture du fichier JSON: {e}")
        print("💡 Vérifiez que le fichier JSON est bien formaté")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à Elasticsearch: {e}")
        print("💡 Vérifiez qu'Elasticsearch est bien démarré et accessible")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue lors de l'indexation: {e}")
        return False

def verify_data():
    """Vérifie que les données ont été correctement indexées"""
    print("🔍 Vérification des données indexées...")
    
    # Petite pause pour laisser Elasticsearch finaliser l'indexation
    time.sleep(2)
    
    try:
        # Première vérification : compter les documents
        response = requests.get(f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_count", timeout=10)
        if response.status_code != 200:
            print(f"❌ Erreur lors de la vérification du comptage: {response.status_code} - {response.text}")
            return False
        
        count = response.json().get('count', 0)
        print(f"   📊 {count} documents trouvés dans l'index '{INDEX_NAME}'")
        
        if count == 0:
            print("⚠️  Aucun document trouvé - vérification de l'existence de l'index...")
            # Vérifier si l'index existe
            mapping_response = requests.get(f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_mapping", timeout=10)
            if mapping_response.status_code == 200:
                print("   📋 L'index existe mais est vide")
                return True
            else:
                print(f"   ❌ L'index n'existe pas ou est inaccessible: {mapping_response.status_code}")
                return False
        
        # Deuxième vérification : récupérer quelques documents pour validation
        sample_response = requests.get(
            f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_search?size=3&pretty", 
            timeout=10
        )
        if sample_response.status_code == 200:
            hits = sample_response.json().get('hits', {}).get('hits', [])
            if hits:
                print(f"   ✅ Échantillon de documents validé ({len(hits)} premiers documents)")
                # Afficher un exemple de document
                first_doc = hits[0]['_source']
                print(f"      📄 Exemple: {first_doc}")
            else:
                print("   ⚠️  L'index contient des documents mais la recherche ne retourne rien")
        
        print(f"✅ Vérification terminée avec succès - {count} documents dans l'index")
        return True
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à Elasticsearch lors de la vérification: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage de la réponse JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue lors de la vérification: {e}")
        return False

def print_next_steps():
    """Affiche les prochaines étapes"""
    print("\n🎉 Configuration Elasticsearch terminée !")
    print("\n📋 Prochaines étapes :")
    print("1. Configurez le client MCP avec les variables d'environnement:")
    print(f"   export ES_URL=\"{ELASTICSEARCH_URL}\"")
    print("   export ES_API_KEY=\"\" (non requis pour cette configuration locale)")
    print("   export ES_USERNAME=\"elastic\"")
    print("   export ES_PASSWORD=\"changeme\"")
    print("\n2. Démarrez le serveur MCP Elasticsearch:")
    print("   cd mcp-server-elasticsearch")
    print("   cargo run -- stdio")
    print("\n3. Démarrez le client MCP multi-serveurs:")
    print("   cd ../mcp-client-python")
    print("   uv run python client.py")
    print("\n💡 Exemples de requêtes:")
    print("   - 'Quel temps fait-il à Paris ?' (serveur météo)")
    print("   - 'Trouve les employés de plus de 30 ans' (serveur Elasticsearch)")
    print("   - 'Liste tous les employés' (serveur Elasticsearch)")

def main():
    """Fonction principale"""
    print("🔧 Script d'initialisation Elasticsearch pour MCP")
    print("=" * 50)
    
    # Vérifier si Elasticsearch répond déjà
    if is_elasticsearch_responsive():
        print("✅ Elasticsearch est déjà en cours d'exécution et répond correctement")
    else:
        # Vérifications préliminaires Docker uniquement si nécessaire
        if not check_docker():
            sys.exit(1)
        
        # Démarrer Elasticsearch si nécessaire
        if not is_container_running(ELASTICSEARCH_CONTAINER):
            if not start_elasticsearch():
                sys.exit(1)
            
            if not wait_for_elasticsearch():
                sys.exit(1)
        else:
            print("✅ Le conteneur Elasticsearch est en cours d'exécution mais ne répond pas encore")
            if not wait_for_elasticsearch():
                sys.exit(1)
    
    # Configuration de l'index et des données
    if not create_index():
        sys.exit(1)
    
    if not index_data():
        sys.exit(1)
    
    if not verify_data():
        sys.exit(1)
    
    print_next_steps()

if __name__ == "__main__":
    main()
