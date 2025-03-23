"""Azure AI Agent Service MCP Server (Synchronous)"""

import os
import sys
import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole, FunctionTool, ToolSet
from azure.identity import DefaultAzureCredential
from datetime import datetime
from neon_functions import create_project, list_projects

# Logging setup
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("azure_agent_mcp")

# Global variables
ai_client = None
agent_cache = {}
default_agent_id = None


def initialize_server():
    """Initialize the Azure AI Agent client."""
    global ai_client, default_agent_id

    project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")
    default_agent_id = os.getenv("DEFAULT_AGENT_ID")

    if not project_connection_string:
        logger.error("Missing required environment variable: PROJECT_CONNECTION_STRING")
        return False

    try:
        credential = DefaultAzureCredential()
        ai_client = AIProjectClient.from_connection_string(
            credential=credential,
            conn_str=project_connection_string,
            user_agent="mcp-azure-ai-agent",
        )
        return True
    except Exception as e:
        logger.error(f"Failed to initialize AIProjectClient: {str(e)}")
        return False


# Load env and init
load_dotenv()
server_initialized = initialize_server()

# MCP Server
mcp = FastMCP(
    "azure-agent",
    description="MCP server for Azure AI Agent Service integration",
    dependencies=["azure-identity", "python-dotenv", "azure-ai-projects"],
)


@mcp.tool()
def query_agent(agent_id: str, query: str, ctx: Context = None) -> str:
    """Send a query to the specific agent in Azure AI Agent and get the response."""
    if not server_initialized:
        return "Error: Azure AI Agent server is not initialized. Check server logs for details."

    try:
        thread = ai_client.agents.create_thread()
        thread_id = thread.id
        print(f"✅ Created thread, ID: {thread_id}")

        ai_client.agents.create_message(
            thread_id=thread_id, role=MessageRole.USER, content=query
        )

        run = ai_client.agents.create_and_process_run(
            thread_id=thread_id,
            agent_id=agent_id,
            max_prompt_tokens=500,
            max_completion_tokens=1000,
        )

        print(f"✅ Run finished with status: {run.status}")

        if run.status == "failed":
            error_msg = f"Agent run failed: {run.last_error}"
            logger.error(error_msg)
            return f"Error: {error_msg}"

        response_messages = ai_client.agents.list_messages(thread_id=thread_id)
        response_message = response_messages.get_last_message_by_role(MessageRole.AGENT)

        result = ""
        if response_message:
            for text in response_message.text_messages:
                result += text.text.value + "\n"

        return result.strip()

    except Exception as e:
        logger.error(f"Agent query failed - ID: {agent_id}, Error: {str(e)}")
        return f"Error querying agent: {str(e)}"


@mcp.tool()
def list_agents() -> str:
    """List available agents in the Azure AI Agent Service."""
    if not server_initialized:
        return "Error: Azure AI Agent server is not initialized. Check server logs for details."

    try:
        agents = ai_client.agents.list_agents()
        if not agents or not agents.data:
            return "No agents found in the Azure AI Agent Service."

        result = "## Available Azure AI Agents\n\n"
        for agent in agents.data:
            result += f"- **{agent.name}**: `{agent.id}`\n"

        return result
    except Exception as e:
        return f"Error listing agents: {str(e)}"


@mcp.tool()
def create_neon_management_agent() -> str:
    """Create a new Neon database management agent."""
    if not server_initialized:
        return "Error: Azure AI Agent server is not initialized. Check server logs for details."

    try:
        toolset = ToolSet()
        functions = FunctionTool({create_project, list_projects})
        toolset.add(functions)

        agent = ai_client.agents.create_agent(
            model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
            name=f"neon-db-agent-{datetime.now().strftime('%Y%m%d%H%M')}",
            description="AI Agent for managing Neon databases and running SQL queries.",
            instructions=f"""
        You are an AI assistant that helps users create and manage Neon projects, databases, 
        branches. Use the provided functions to perform actions.
        The current date is {datetime.now().strftime("%Y-%m-%d")}.
        """,
            toolset=toolset,
        )

        return f"✅ Created agent - **{agent.name}**: `{agent.id}`\n"

    except Exception as e:
        return f"Error creating agent: {str(e)}"


# Start server
if __name__ == "__main__":
    status = (
        "successfully initialized" if server_initialized else "initialization failed"
    )
    print(
        f"\n{'=' * 50}\nAzure AI Agent MCP Server {status}\nStarting server...\n{'=' * 50}\n"
    )
    mcp.run()
