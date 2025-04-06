# MCP Demo Project

A demonstration of the Model Context Protocol (MCP) with multiple services, including math operations and book information retrieval.

## Overview

This project showcases how to use the Model Context Protocol (MCP) to create tools that can be utilized by large language models (LLMs). It includes:

- **Math Operations Service**: A Python-based Stdio MCP server implemented in `src/math_server.py`.
- **Notes Service**: A Node.js-based service using Server-Sent Events (SSE) for book information or notes retrieval.
- **MCP Client**: A Python client (`src/mcp_clent.py`) that connects to the Stdio MCP server and provides tools to the LLM.

## Requirements

- **Python**: Version 3.9+ (developed with Python 3.13)
- **Node.js**: Version 18+ (for Node.js-based services)
- **npm**: For managing Node.js dependencies

## Installation

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

### Running the MCP Client

The MCP client (`src/mcp_clent.py`) connects to the Stdio MCP server and provides tools for math operations. To run the client:

```bash
python src/mcp_client.py
```

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



