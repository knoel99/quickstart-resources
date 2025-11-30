# Quickstart Resources

Repository with Model Context Protocol (MCP) projects:
- MCP client with OpenAI integration
- MCP weather server

## Installation et Utilisation

Ce projet utilise **uv** pour la gestion des dépendances avec des environnements virtuels isolés par projet.

### Installation des dépendances
```bash
# Pour chaque projet individuellement
cd mcp-client-python
sudo uv sync

cd ../weather-server-python  
sudo uv sync
```

### Configuration

#### Client MCP (OpenAI)
```bash
cd mcp-client-python
# Configuration
cp .env.example .env
# Éditer .env pour ajouter votre OPENAI_API_KEY

# Lancement du client
uv run python client.py ../weather-server-python/weather.py
```

#### Serveur MCP Météo
```bash
cd weather-server-python
# Configuration
cp .env.example .env
# Éditer .env pour ajouter votre clé API météo

# Lancement du serveur
uv run python weather.py
```

## Gestion de l'Environnement

### uv par projet
Chaque projet utilise son propre environnement virtuel isolé :
- **Installation** : `uv sync` dans le dossier du projet crée un environnement virtuel local
- **Exécution** : `uv run <commande>` utilise l'environnement virtuel du projet courant
- **Environnement virtuel** : Créé automatiquement dans `.venv` dans chaque dossier de projet
- **Nettoyage** : `rm -rf .venv` pour supprimer l'environnement du projet

### Commandes utiles
```bash
# Depuis le dossier d'un projet
cd mcp-client-python
uv sync                    # Installer les dépendances
uv run python -c "import openai; print('OpenAI OK')"  # Vérifier l'installation

cd ../weather-server-python
uv sync                    # Installer les dépendances  
uv run python -c "import httpx; print('HTTPX OK')"  # Vérifier l'installation

# Mettre à jour une dépendance
cd mcp-client-python
uv add openai               # Ajouter/mettre à jour openai
```

## Structure du Projet

```
quickstart-resources/
├── mcp-client-python/          # Client MCP avec OpenAI
│   ├── .venv/                  # Environnement virtuel du client
│   ├── client.py
│   ├── .env.example
│   └── pyproject.toml
└── weather-server-python/      # Serveur MCP météo
    ├── .venv/                  # Environnement virtuel du serveur
    ├── weather.py
    ├── .env.example
    └── pyproject.toml
```

Chaque projet est totalement indépendant avec son propre environnement virtuel et ses propres dépendances.
