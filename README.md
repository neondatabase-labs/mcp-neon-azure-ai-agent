# Azure AI Agent Service, MCP and Neon Integration

This project connects **Azure AI Agent Service** with **Neon Serverless Postgres** using **MCP (Model Context Protocol)**. It lets you send commands to an AI agent that can create a Neon management Agent to manage Neon projects, databases, and more.

![Azure AI Agent Service, MCP and Neon Integration](/assets/Neon%20MCP%20Azure%20AI%20Foundry.gif)

## What It Does
- MCP server integrates with Azure AI Foundry to enable connections to your existing Azure AI Agents.
- MCP tool creates a new Neon management agent in the Azure AI Foundry. Starts an AI Agent with tools like `create_project` (via Neon API).
- Lets you ask the agent to do tasks like creating a Neon project.
- Uses MCP to communicate with the agent in real time.

## Why Use This?
- Use natural language to control your Neon database
- Automate project and database management
- Build powerful RAG (Retrieval-Augmented Generation) apps using Neon

## How It Works
1. When the server starts, it:
   - Loads environment variables
   - Connects to Azure AI Agent Service
   - Creates an AI Agent with tool functions (like `create_project`)
2. The agent listens for queries through MCP
3. When a query is sent, it:
   - Creates a thread
   - Adds a message
   - Runs the tool automatically
   - Returns the result

## Requirements
- Python 3.9+
- An **[Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal)** setup
- A **[Neon API Key](https://neon.tech/docs/manage/api-keys#creating-api-keys?refcode=44WD03UH)**
- MCP installed and running. Refer to the [Claude Desktop Users get started guide](https://modelcontextprotocol.io/quickstart/user)

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/neondatabase-labs/mcp-neon-azure-ai-agent.git
   cd mcp-neon-azure-ai-agent
   ```
2. Create a new virtual environment:
   ```bash
   python -m venv venv && source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```ini
   PROJECT_CONNECTION_STRING=your_azure_project_connection_string
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_deployment_name
   NEON_API_KEY=your_neon_api_key
   ```
5.  Configure Claude Desktop (or another MCP client)

    Update your MCP client configuration (claude_desktop_config.json) to integrate the MCP server with the following in any text editor:

    ```json
    {
        "mcpServers": {
          "azure-agent": {
            "command": "/ABSOLUTE/PATH/TO/neon-mcp-azure-ai-agent/venv/bin/python",
            "args": [
              "-m",
              "azure_agent_mcp_server"
            ],
            "cwd": "/ABSOLUTE/PATH/TO/neon-mcp-azure-ai-agent",
            "env": {
              "PYTHONPATH": "/Users/boburumurzokov/Neon/neon-mcp-azure-ai-agent",
              "PROJECT_CONNECTION_STRING": "eastus.api.azureml.ms;7a478544-9d2b-4f43-9916-7787f55aa58d;ai-agents-demo;mcp-neon-demo",
              "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": "gpt4o",
              "NEON_API_KEY": "napi_oigyl7kyhd69jmi3w3tlmfs6zbrna2u3hi1d3s94clputmvmoa1c6ej30p1536al"
            }
          }
        }
      }
    ```

    Replace `/ABSOLUTE/PATH/TO` to your valid directory path where `neon-mcp-azure-ai-agent` folder is located.

 6. Restart Claude

    After updating your configuration file, you need to restart Claude for Desktop. Upon restarting, you should see a hammer icon in the bottom right corner of the input box. After clicking on the hammer icon, you should see the tools.

## Try a Query
From your MCP client or Claude App interface, try:
```text
Create a Neon database project named 'My MCP'.
```

## What's Next
- Add more Neon tools (create_branch, create_database, etc.)
- Log results
- Support SQL queries

---
Built with ❤️ using Azure + Neon + MCP

## Other useful resources

- [Neon MCP Server](https://neon.tech/docs/ai/neon-mcp-server)
- [Build AI Agents with Azure AI Agent Service and Neon](https://neon.tech/blog/build-ai-agents-with-azure-ai-agent-service-and-neon)