# MCP Demo Project

A demonstration of the Model Context Protocol (MCP) with multiple services, including math operations and notes information retrieval.

## Overview

This project showcases how to use the Model Context Protocol (MCP) to create tools that can be utilized by large language models (LLMs). It includes:

- **Math Operations Service**: A Python-based Stdio MCP server implemented in `src/math_server.py`.
- **Notes Service**: A Node.js-based service using Server-Sent Events (SSE) for notes retrieval.
- **MCP Client**: A Python client (`src/my_mcp_clent.py`) that connects to the Stdio & SSE MCP server and provides tools, resources to the LLM.

## Requirements

- **Python**: Version 3.9+ (developed with Python 3.13)
- **Node.js**: Version 18+ (for Node.js-based services)
- **npm**: For managing Node.js dependencies

## Installation

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

### Running the Node.js MCP Notes Server (SSEServerTransport)

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

### Running SSE (src/math_server.py) server.

We need to first run below script which starts MCP server with Sse Transport.
```bash
python src/math_server.py
```

### Running the MCP Client

The MCP client (`src/my_mcp_clent.py`) connects to the Stdio & SSE MCP (src/math_server.py) server and provides tools, resources for math operations. To run the client:

```bash
python src/my_mcp_clent.py
```

### Running the Multi-Server MCP Client

The multi-server MCP client (`src/multiserver_mcp_client.py`) connects to both the Python and Node.js servers, invokes the LLM with prompts, and uses tools supported by both MCP servers. To run it:

```bash
python src/multiserver_mcp_client.py
```

## Environment Variables

Ensure the following environment variables are set in the `.env` file:

```plaintext
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Replace `your_openai_api_key`, `your_groq_api_key`, and `your_anthropic_api_key` with your actual API keys.



