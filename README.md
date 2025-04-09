# MCP Demo Project

A demonstration of the Model Context Protocol (MCP) with multiple services, including math operations and notes information retrieval mcp servers.

## Overview

This project showcases how to use the Model Context Protocol (MCP) to create tools & resources that can be utilized by large language models (LLMs). It includes:

- **Math Operations Service**: A Python-based Stdio MCP server implemented in `src/server/mcp_math_server.py`.
- **Notes Service**: A Node.js-based service using Server-Sent Events (SSE) for notes retrieval. Server is implemented in `src/index.js`
- **MCP Client**: A Python client (`src/client/mcp_client.py`) that connects to mcp_math_server queries llm and utlizes server tools and resources.

## Requirements

- **Python**: Version 3.9+ (developed with Python 3.13)
- **Node.js**: Version 18+ (for Node.js-based services)
- **npm**: For managing Node.js dependencies

## Installation

## Getting Started

### Clone the Repository

First, clone the repository to your local machine:

```bash
# Clone the repository
git clone https://github.com/dheerajsn/mcp_demo.git

#or you can fork from above repo and clone it from your forked repo.

# Navigate to the project directory
cd mcp_demo
```

## Add the Project to PYTHONPATH
```bash
# On macOS/Linux (add to your .bashrc or .zshrc for permanence)
export PYTHONPATH=$PYTHONPATH:/path/to/mcp_demo

# On Windows (Command Prompt)
set PYTHONPATH=%PYTHONPATH%;C:\path\to\mcp_demo

# On Windows (PowerShell)
$env:PYTHONPATH += ";C:\path\to\mcp_demo"
```

## Python Virtual Environment

First, create and activate a Python virtual environment:

```bash
# Create a virtual environment
# On macOS/Linux:
python -m venv .venv

# On Windows:
python -m venv .venv
# or if you have multiple Python versions:
py -3 -m venv .venv
```

Activate the virtual environment:
```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Node.js Dependencies

Install the required Node.js packages:

```bash
npm install
```

## Usage

### 1. Running the Node.js MCP Notes Server (SSEServerTransport)

For the Node.js-based service (e.g.,notes service), follow these steps:

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Run the notes server in development mode (with live reloading):
   ```bash
   npm run dev
   ```

3. Run the MCP Inspector for debugging:
   ```bash
   npm run inspect
   ```

### 2. Running SSE (src/server/mcp_math_server.py) server. After running, you can test it through MCP inspector (port 8000)

We need to first run below script which starts MCP server with Sse Transport.
```bash
python src/server/mcp_math_server.py
```

### Running single MCP Client

The MCP client (`src/client/mcp_client.py`) connects to the Stdio & SSE MCP (src/server/mcp_math_server.py) server and provides tools, resources for math operations. To run the client:

```bash
python src/client/mcp_client.py
```

### Running the Multi-Server MCP Client

The multi-server MCP client (`src/client/mcp_multiserver_client.py`) connects to both the Python (Stdio) and Node.js (SSE) servers, invokes the LLM with prompts, and uses tools/resources supported by both MCP servers. To run it:

```bash
python src/client/mcp_multiserver_client.py
```

## Environment Variables

Ensure the following environment variables are set in the `.env` file:

```plaintext
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Replace `your_openai_api_key`, `your_groq_api_key`, and `your_anthropic_api_key` with your actual API keys.



