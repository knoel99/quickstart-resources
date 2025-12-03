# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, weather information, and extensible tool integrations via the MCP (Model Context Protocol) architecture.

## Features

- 🤖 **Claude Integration**: Direct communication with Claude AI
- 🔧 **Native Tools**: Built-in tools for web search and file operations
- 🌤️ **Weather API**: Integrated National Weather Service for alerts and forecasts
- 📚 **Document Management**: Read and edit documents via MCP
- 🔄 **MCP Protocol**: Full Model Context Protocol support
- 💬 **Interactive Chat**: Conversational CLI interface

## Architecture

- `core/` - Core functionality
  - `tools.py` - Native tool system with web search and file operations
  - `weather.py` - Weather API integration (NWS)
  - `chat.py` - Chat orchestration
  - `claude.py` - Claude API integration
  - `cli_chat.py` - CLI chat interface
- `mcp_server.py` - MCP server with document management and weather tools
- `main.py` - CLI entry point
- `weather_demo.py` - Demo script for weather functionality

## Prerequisites

- Python 3.9+
- Anthropic API Key
- Internet connection for weather API

## Setup

### Step 1: Configure environment variables

1. Create or edit `.env` file in project root and verify that the following variables are set correctly:

```
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0" httpx
```

3. Run project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use / prefix to execute commands defined in MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

### Weather Integration

The application now supports weather information through MCP tools:

**Available weather tools:**
- `get_weather_alerts(state)` - Get weather alerts for a US state
- `get_weather_forecast(latitude, longitude)` - Get weather forecast for coordinates

**Example usage:**
```
> Check for weather alerts in California
> What's the weather forecast for San Francisco?
```

### Native Tools

Access additional native tools through the MCP interface:

- `list_native_tools()` - Lists all available native tools
- `execute_native_tool(tool_name, arguments)` - Executes a native tool

**Available native tools:**
- `web_search` - Search the web
- `create_file` - Create a new file
- `read_file` - Read file contents
- `write_file` - Write to a file
- `delete_file` - Delete a file
- `list_directory` - List directory contents

## Demo

Run the weather demo to test functionality:

```bash
python weather_demo.py
```

This will demonstrate:
- Weather API functionality
- Tool manager capabilities
- MCP integration examples

## Development

### Adding New Documents

Edit `mcp_server.py` file to add new documents to the `docs` dictionary.

### Adding New Tools

1. Add your tool to `core/tools.py` in the appropriate category
2. Update the `ToolManager` class to include your new tool
3. Restart the MCP server to make tools available

### Weather API Integration

The weather functionality is implemented in `core/weather.py`:
- Uses National Weather Service (NWS) API
- Supports weather alerts for US states
- Provides detailed forecasts for coordinates
- Handles API errors gracefully

### MCP Tools Available

**Document Management:**
- `read_doc_contents(doc_id)` - Read document contents
- `edit_document(doc_id, old_str, new_str)` - Edit document
- `list_docs()` - List all documents (resource)
- `fetch_doc(doc_id)` - Fetch document (resource)

**Weather Information:**
- `get_weather_alerts(state)` - Get weather alerts
- `get_weather_forecast(latitude, longitude)` - Get weather forecast

**Native Tool Bridge:**
- `list_native_tools()` - List available native tools
- `execute_native_tool(tool_name, arguments)` - Execute native tool

**Prompts:**
- `format(doc_id)` - Format document in markdown

### Linting and Typing Check

There are no lint or type checks implemented.

## Project Structure

```
exercice1/cli_project_progress/
├── core/
│   ├── __init__.py
│   ├── tools.py          # Native tool system
│   ├── weather.py         # Weather API integration
│   ├── chat.py           # Chat orchestration
│   ├── claude.py         # Claude API integration
│   └── cli_chat.py       # CLI chat interface
├── mcp_server.py         # MCP server with tools
├── main.py               # CLI entry point
├── weather_demo.py        # Weather functionality demo
├── pyproject.toml         # Project dependencies
└── README.md             # This file
