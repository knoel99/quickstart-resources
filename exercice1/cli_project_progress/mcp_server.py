from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tools import ToolManager
from core.weather import WeatherAPI


mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]

@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""
    
    return [
        base.UserMessage(prompt)
    ]


# Initialize tool manager and weather API
tool_manager = ToolManager()
weather_api = WeatherAPI()

# Expose native tools as MCP tools
@mcp.tool(
    name="list_native_tools",
    description="List all available native tools"
)
def list_native_tools():
    """List all available native tools."""
    return tool_manager.list_tools()

@mcp.tool(
    name="execute_native_tool",
    description="Execute a native tool with given arguments"
)
def execute_native_tool(
    tool_name: str = Field(description="Name of the tool to execute"),
    arguments: str = Field(description="JSON string of arguments for the tool")
):
    """Execute a native tool with given arguments."""
    import json
    
    try:
        args = json.loads(arguments)
        result = tool_manager.execute_tool(tool_name, args)
        return str(result)
    except Exception as e:
        return f"Error executing tool {tool_name}: {str(e)}"

# Weather tools
@mcp.tool(
    name="get_weather_alerts",
    description="Get weather alerts for a US state"
)
def get_weather_alerts(
    state: str = Field(description="Two-letter US state code (e.g. CA, NY)")
):
    """Get weather alerts for a US state."""
    try:
        result = weather_api.get_alerts(state)
        return result
    except Exception as e:
        return f"Error getting weather alerts: {str(e)}"

@mcp.tool(
    name="get_weather_forecast",
    description="Get weather forecast for a location"
)
def get_weather_forecast(
    latitude: float = Field(description="Latitude of the location"),
    longitude: float = Field(description="Longitude of the location")
):
    """Get weather forecast for a location."""
    try:
        result = weather_api.get_forecast(latitude, longitude)
        return result
    except Exception as e:
        return f"Error getting weather forecast: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
