from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from my_mcp_clent import get_llm_model, print_messages
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from mcp.types import (
    EmptyResult,
    ErrorData,
    InitializeResult,
    ReadResourceResult,
    TextContent,
    TextResourceContents,
    Tool,
)
from pydantic import AnyUrl


async def run(model):
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["src/math_server.py"],
                "transport": "stdio",
            },
            "notes": {
                "url": "http://localhost:3000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(get_llm_model(model), client.get_tools())
        math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
        all_notes_response = await agent.ainvoke({"messages": "List all notes"})
        create_note_response = await agent.ainvoke({"messages": "Get Capitals of all US States, create note with title US State capitals and US state capital as contents of notes"})

        print("=== EXECUTION PATH ===")
        # Extract the messages from the response
        messages = math_response.get('messages', [])
        print_messages(messages)

        messages = all_notes_response.get('messages', [])
        print_messages(messages)

        messages = create_note_response.get('messages', [])
        print_messages(messages)
    
    print("Resource with Note ID 3:")
    uri = "note://3"
    print(f"URI: {uri}")
    async with sse_client("http://localhost:3000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            resource = await session.read_resource(uri=AnyUrl(uri))
            text_content = resource.contents[0]
            if isinstance(text_content, TextResourceContents):
                print(f"Note content: {text_content.text}")
            
            session.ai

if __name__ == "__main__":
    import asyncio
    async def main():
        print("\n=== Anthropic ===")
        await run("anthropic") 

    asyncio.run(main())

