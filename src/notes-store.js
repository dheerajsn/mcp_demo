// Simple in-memory notes storage
const notes = {
    "1": {
      id: "1",
      title: "Welcome Note",
      content: "Welcome to the Simple Notes MCP server!",
      created: "2023-06-15T10:00:00Z"
    },
    "2": {
      id: "2",
      title: "Shopping List",
      content: "- Milk\n- Bread\n- Eggs\n- Apples",
      created: "2023-06-16T14:30:00Z"
    }
  };

  let nextId = 3;

  export function getAllNotes() {
    return Object.values(notes);
  }

  export function getNoteById(id) {
    return notes[id] || null;
  }

  export function createNote(title, content) {
    const id = String(nextId++);
    const created = new Date().toISOString();
    
    notes[id] = {
      id,
      title,
      content,
      created
    };
    
    return notes[id];
  }

  export function deleteNote(id) {
    if (!notes[id]) {
      return false;
    }
    
    delete notes[id];
    return true;
  }
