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
uv sync

cd ../weather-server-python  
uv sync
```

Définir la clef API:
```bash
cd mcp-client-python
cp .env.example .env
# Éditer .env pour ajouter votre OPENAI_API_KEY
```

### Exécution

```bash
uv run python client.py ../weather-server-python/weather.py
```

Exemple d'exécution :
```bash
kim@ARTIK-PCA41-KNO:~/quickstart-resources$ cd mcp-client-python && uv run python client.py ../weather-server-python/weather.py
[11/30/25 11:00:35] INFO     Processing request of type ListToolsRequest                                                                  server.py:674

Connected to server with tools: ['get_alerts', 'get_forecast']

MCP Client Started!
Type your queries or 'quit' to exit.

Query: quel temps à SF
[11/30/25 11:00:56] INFO     Processing request of type ListToolsRequest                                                                  server.py:674
[11/30/25 11:01:05] INFO     Processing request of type CallToolRequest                                                                   server.py:674
                    INFO     HTTP Request: GET https://api.weather.gov/points/37.7749,-122.4194 "HTTP/1.1 200 OK"                       _client.py:1740
                    INFO     HTTP Request: GET https://api.weather.gov/gridpoints/MTR/85,105/forecast "HTTP/1.1 200 OK"                 _client.py:1740
[DEBUG] Tool get_forecast returned: [TextContent(type='text', text='\nOvernight:\nTemperature: 47°F\nWind: 2 mph N\nForecast: Mostly cloudy, with a low around 47. North wind around 2 mph.\n\n---\n\nSunday:\nTemperature: 55°F\nWind: 2 to 6 mph NNE\nForecast: Mostly sunny. High near 55, with temperatures falling to around 53 in the afternoon. North northeast wind 2 to 6 mph.\n\n---\n\nSunday Night:\nTemperature: 46°F\nWind: 5 mph N\nForecast: Partly cloudy, with a low around 46. North wind around 5 mph.\n\n---\n\nMonday:\nTemperature: 61°F\nWind: 5 to 8 mph NNE\nForecast: Sunny, with a high near 61. North northeast wind 5 to 8 mph.\n\n---\n\nMonday Night:\nTemperature: 47°F\nWind: 3 to 7 mph NE\nForecast: Mostly clear, with a low around 47. Northeast wind 3 to 7 mph.\n', annotations=None, meta=None)]

[Calling tool get_forecast with args {'latitude': 37.7749, 'longitude': -122.4194}]
Result: [TextContent(type='text', text='\nOvernight:\nTemperature: 47°F\nWind: 2 mph N\nForecast: Mostly cloudy, with a low around 47. North wind around 2 mph.\n\n---\n\nSunday:\nTemperature: 55°F\nWind: 2 to 6 mph NNE\nForecast: Mostly sunny. High near 55, with temperatures falling to around 53 in the afternoon. North northeast wind 2 to 6 mph.\n\n---\n\nSunday Night:\nTemperature: 46°F\nWind: 5 mph N\nForecast: Partly cloudy, with a low around 46. North wind around 5 mph.\n\n---\n\nMonday:\nTemperature: 61°F\nWind: 5 to 8 mph NNE\nForecast: Sunny, with a high near 61. North northeast wind 5 to 8 mph.\n\n---\n\nMonday Night:\nTemperature: 47°F\nWind: 3 to 7 mph NE\nForecast: Mostly clear, with a low around 47. Northeast wind 3 to 7 mph.\n', annotations=None, meta=None)]
Voici la météo pour San Francisco:

- Cette nuit: Ciel souvent nuageux, min ~8°C (47°F), vent faible du nord.
- Dimanche: Plutôt ensoleillé, max ~13°C (55°F) puis ~12°C (53°F) l’après-midi, vent léger NNE.
- Dimanche soir: Partiellement nuageux, min ~8°C (46°F), vent faible du nord.
- Lundi: Ensoleillé, max ~16°C (61°F), vent léger NNE.
- Lundi nuit: Ciel dégagé, min ~8°C (47°F), vent faible NE.

Vous préférez les températures uniquement en °C ou en °F ?

Query: en celcius
[11/30/25 11:01:39] INFO     Processing request of type ListToolsRequest                                                                  server.py:674

D’accord, voici en °C:

- Cette nuit: min ~8°C, ciel souvent nuageux.
- Dimanche: max ~13°C (puis ~12°C l’après-midi), plutôt ensoleillé.
- Dimanche soir: min ~8°C, partiellement nuageux.
- Lundi: max ~16°C, ensoleillé.
- Lundi nuit: min ~8°C, ciel dégagé.

Query:
```

## Gestion de l'Environnement

### uv par projet
Chaque projet utilise son propre environnement virtuel isolé :
- **Installation** : `uv sync` dans le dossier du projet crée un environnement virtuel local
- **Exécution** : `uv run <commande>` utilise l'environnement virtuel du projet courant
- **Environnement virtuel** : Créé automatiquement dans `.venv` dans chaque dossier de projet
- **Nettoyage** : `rm -rf .venv` pour supprimer l'environnement du projet


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

## Architecture du Projet


### Structure des Composants

Ce diagramme détaille l'architecture interne des composants MCP. Le côté client montre la classe MCPClient qui orchestre la ClientSession pour la communication MCP, l'OpenAI Client pour les appels IA, et maintient l'historique de conversation. Du côté serveur, FastMCP gère l'enregistrement des outils get_alerts et get_forecast, qui utilisent HTTP Request Handler pour communiquer avec l'API externe. Les dépendances incluent les bibliothèques MCP pour le protocole, HTTPX pour les requêtes HTTP, OpenAI SDK pour l'intégration IA, et python-dotenv pour la gestion des variables d'environnement.

```mermaid
graph LR
    subgraph "Client MCP"
        MC[MCPClient]
        CS[ClientSession]
        OC[OpenAI Client]
        CH[Conversation History]
    end
    
    subgraph "Serveur MCP"
        FM[FastMCP Server]
        GA[get_alerts tool]
        GF[get_forecast tool]
        HR[HTTP Request Handler]
    end
    
    subgraph "Dependencies"
        MCP[MCP Library]
        HTTPX[HTTPX Client]
        OPENAI[OpenAI SDK]
        DOTENV[Python-dotenv]
    end
    
    MC --> CS
    MC --> OC
    MC --> CH
    CS --> MCP
    
    FM --> GA
    FM --> GF
    GA --> HR
    GF --> HR
    HR --> HTTPX
    
    OC --> OPENAI
    MC --> DOTENV
    
    style MC fill:#e1f5fe
    style FM fill:#f3e5f5
```

### Flow de Décision MCP

Ce flowchart représente la logique de décision d'OpenAI lorsqu'il traite une requête utilisateur. OpenAI analyse d'abord la requête pour déterminer si un outil est nécessaire. Si aucun outil n'est requis, il fournit une réponse directe. Si un outil est nécessaire, il détermine lequel des deux outils météo utiliser : get_alerts pour les alertes par état, ou get_forecast pour les prévisions par coordonnées. Chaque outil déclenche des requêtes spécifiques à l'API NWS (alerts, points, ou forecast), puis les données sont formatées et renvoyées à OpenAI pour synthèse avant la réponse finale à l'utilisateur.

```mermaid
flowchart TD
    A[Query Utilisateur] --> B{OpenAI analyse}
    B -->|Besoin d'outil| C[Déterminer l'outil requis]
    B -->|Pas d'outil| F[Réponse directe]
    
    C --> G{get_alerts?}
    C --> H{get_forecast?}
    
    G --> I["Appel get_alerts(state)"]
    H --> J["Appel get_forecast(lat, lon)"]
    
    I --> K[Requête NWS alerts]
    J --> L[Requête NWS points]
    L --> M[Requête NWS forecast]
    
    K --> N[Formatage alertes]
    M --> O[Formatage prévisions]
    
    N --> P[Résultat outil]
    O --> P
    
    P --> Q[OpenAI synthétise]
    Q --> R[Réponse utilisateur]
    
    F --> R
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style P fill:#e8f5e8
    style R fill:#e1f5fe
```


## Flux des Appels MCP

### Diagramme de Séquence Complet

Ce diagramme de séquence illustre le flux complet d'une requête MCP, divisé en quatre phases principales. La phase d'initialisation établit la connexion entre client et serveur via stdio et découvre les outils disponibles. La phase de conversation capture la requête utilisateur et l'envoie à OpenAI avec les outils disponibles. La phase d'exécution d'outil déclenche quand OpenAI détermine qu'un outil est nécessaire : le client appelle le serveur MCP, qui effectue les requêtes HTTP vers l'API NWS (d'abord pour obtenir les points de grille, puis les prévisions). La phase de synthèse intègre les résultats de l'outil dans le contexte OpenAI pour générer une réponse finale contextuelle.

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant C as Client MCP
    participant O as OpenAI API
    participant S as Serveur MCP
    participant NWS as NWS API
    
    Note over C,S: Phase d'Initialisation
    C->>S: Connection (stdio)
    C->>S: session.initialize()
    C->>S: list_tools()
    S-->>C: [get_alerts, get_forecast]
    
    Note over U,O: Phase de Conversation
    U->>C: "Quelle est la météo à New York ?"
    C->>C: Ajoute à conversation_history
    C->>O: chat.completions.create()<br/>avec tools disponibles
    
    Note over O: Analyse et décision d'outil
    O-->>C: tool_calls: get_forecast(lat, lon)
    C->>C: Ajoute tool_calls à l'historique
    
    Note over C,S: Phase d'Exécution d'Outil
    C->>S: call_tool("get_forecast", {lat, lon})
    S->>NWS: GET /points/{lat},{lon}
    NWS-->>S: Points data avec forecast URL
    S->>NWS: GET /forecast
    NWS-->>S: Forecast data
    S-->>C: Formatted forecast result
    
    Note over C,O: Phase de Synthèse
    C->>C: Ajoute tool_result à l'historique
    C->>O: chat.completions.create()<br/>avec contexte complet
    O-->>C: Response finale avec météo
    C->>U: "Il fait 15°C à New York..."
    
    Note over C,S: Nettoyage
    C->>S: cleanup()
```


## Détails des Composants MCP

### Client MCP Features
- **Session Management** : Gestion des connexions stdio avec les serveurs
- **Tool Discovery** : Découverte automatique des outils disponibles
- **OpenAI Integration** : Conversion des outils MCP en format OpenAI functions
- **Conversation History** : Maintien du contexte de conversation
- **Error Handling** : Gestion robuste des erreurs

### Serveur MCP Features
- **FastMCP Framework** : Utilisation du framework FastMCP pour le développement rapide
- **Tool Registration** : Décoration des fonctions avec `@mcp.tool()`
- **Async Operations** : Support des opérations asynchrones
- **API Integration** : Intégration avec l'API National Weather Service
- **Data Formatting** : Formatage des réponses pour une meilleure lisibilité

### Protocole MCP
- **Transport** : Communication via stdio (standard input/output)
- **Message Format** : JSON-RPC 2.0 pour les échanges
- **Tool Calling** : Mécanisme standardisé pour l'appel d'outils
- **Resource Sharing** : Partage de ressources entre client et serveur
