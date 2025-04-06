from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from my_mcp_clent import get_llm_model, print_messages

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
        

        print("=== EXECUTION PATH ===")
        # Extract the messages from the response
        messages = math_response.get('messages', [])
        print_messages(messages)

        messages = all_notes_response.get('messages', [])
        print_messages(messages)

if __name__ == "__main__":
    import asyncio
    async def main():
        print("\n=== Anthropic ===")
        await run("anthropic") 

    asyncio.run(main())

