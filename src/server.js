import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';
    import { z } from 'zod';
    import { getAllNotes, getNoteById, createNote, deleteNote } from './notes-store.js';

    // Create an MCP server for simple notes
    const server = new McpServer({
      name: "Simple Notes",
      version: "1.0.0",
      description: "A simple note-taking MCP server"
    });

    // Resource: Get note by ID
    server.resource(
      "note",
      new ResourceTemplate("note://{id}", { list: undefined }),
      async (uri, { id }) => {
        const note = getNoteById(id);
        
        if (!note) {
          return {
            contents: [{
              uri: uri.href,
              text: `Note with ID ${id} not found.`
            }]
          };
        }
        
        return {
          contents: [{
            uri: uri.href,
            text: `# ${note.title}\n\n${note.content}\n\nCreated: ${note.created}`
          }]
        };
      }
    );

    // Tool: List all notes
    server.tool(
      "list_notes",
      {},
      async () => {
        const notes = getAllNotes();
        
        if (notes.length === 0) {
          return {
            content: [{ 
              type: "text", 
              text: "No notes found."
            }]
          };
        }
        
        const notesList = notes.map(note => 
          `- ID: ${note.id}, ${note.title}`
        ).join('\n');
        
        return {
          content: [{ 
            type: "text", 
            text: `Available notes:\n\n${notesList}`
          }]
        };
      },
      { description: "List all available notes" }
    );

    // Tool: Create a new note
    server.tool(
      "create_note",
      { 
        title: z.string().describe("Title of the note"),
        content: z.string().describe("Content of the note")
      },
      async ({ title, content }) => {
        const note = createNote(title, content);
        
        return {
          content: [{ 
            type: "text", 
            text: `Note created successfully!\n\nID: ${note.id}\nTitle: ${note.title}\nCreated: ${note.created}`
          }]
        };
      },
      { description: "Create a new note" }
    );

    // Tool: Delete a note
    server.tool(
      "delete_note",
      { 
        id: z.string().describe("ID of the note to delete")
      },
      async ({ id }) => {
        const success = deleteNote(id);
        
        if (!success) {
          return {
            content: [{ 
              type: "text", 
              text: `Note with ID ${id} not found.`
            }],
            isError: true
          };
        }
        
        return {
          content: [{ 
            type: "text", 
            text: `Note with ID ${id} deleted successfully.`
          }]
        };
      },
      { description: "Delete a note by ID" }
    );

    export { server };
