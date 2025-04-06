//import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import express from "express";
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { server } from './server.js'; // Keep this import

console.log('Starting Simple Notes MCP server...');

const app = express();
let transport;

// Create your SSE transport
app.get("/sse", (req, res) => {
  transport = new SSEServerTransport("/messages", res);
  server.connect(transport);
});

app.post("/messages", (req, res) => {
  if (transport) {
    transport.handlePostMessage(req, res);
  }
});

app.listen(3000);
