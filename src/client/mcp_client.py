# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import dotenv
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from utils.faiss_vector_db import create_vector_db
from langchain.chains import RetrievalQA

import json

# Load environment variables from .env file
dotenv.load_dotenv()

def get_llm_model(provider, temperature=0):
    """Get LLM model based on provider name"""
    if provider.lower() == "anthropic":
        return ChatAnthropic(
            model="claude-3-7-sonnet-latest",
            temperature=temperature,
        )
    elif provider.lower() == "groq":
        return ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=temperature
        )
    elif provider.lower() == "openai":
        return ChatOpenAI(
            model="gpt-4o",
            temperature=temperature
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    
def print_messages(messages):
    for msg in messages:
        # Determine the message role from the object's type
        role = type(msg).__name__
        
        # Get the message content, handling list-type content (as in AI messages)
        content = msg.content
        if isinstance(content, list):
            combined_parts = []
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    combined_parts.append(part["text"])
                else:
                    combined_parts.append(str(part))
            content = " ".join(combined_parts)
        
        # Initialize extra info strings for tool calls and token usage
        tool_calls_info = ""
        usage_info = ""
        
        # Check if the message has a 'tool_calls' attribute (typically on AI messages)
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.get('name')
                args = tool_call.get('args')
                tool_calls_info += f"\n    Tool used: {tool_name} with parameters: {args}"
        
        # Check for token usage information in usage_metadata or within response_metadata
        # (Depending on your implementation, these might be stored differently)
        usage = getattr(msg, 'usage_metadata', None)
        if not usage and hasattr(msg, 'response_metadata'):
            usage = msg.response_metadata.get('usage')
        if usage:
            input_tokens = usage.get('input_tokens')
            output_tokens = usage.get('output_tokens')
            total_tokens = usage.get('total_tokens')
            usage_info = f" [Input tokens: {input_tokens}, Output tokens: {output_tokens}, Total tokens: {total_tokens}]"
        
        # Print the formatted message with any additional info
        print(f"{role}: {content}{usage_info}{tool_calls_info}\n")

async def invoke_with_mcp(session, llm, query):
    await session.initialize()

    # Get tools
    tools = await load_mcp_tools(session)
    
    # Print available tools
    print("\n=== AVAILABLE TOOLS ===")
    for tool in tools:
        print(f"• {tool.name}: {tool.description}")
    
    query = (
        f"You are a smart AI assistant, and I want you to tell me {query}. "
        "Please understand the question properly, make use of tools only if needed, "
        "and provide the final answer in a single line."
    )
    print(f"\n=== QUERY ===\n{query}\n")

    # Create and run the agent
    agent = create_react_agent(get_llm_model(llm), tools)
    agent_response = await agent.ainvoke({"messages": query})
    
    # Print human-readable output
    print("=== EXECUTION PATH ===")
    
    # Extract the messages from the response
    messages = agent_response.get('messages', [])
    
    # Track tool usage
    tool_calls = []
    print_messages(messages)

async def run(transport, llm, query):
    if transport == "stdio":
        stdio_server_params = StdioServerParameters(
            command="python",
            # Make sure to update to the full absolute path to your math_server.py file
            args=["src/server/mcp_math_server.py", "--transport", "stdio"],
        )
        async with stdio_client(stdio_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await invoke_with_mcp(session, llm, query)
    else:
        async with sse_client("http://localhost:8000/sse") as (read, write):
            async with ClientSession(read, write) as session:
                await invoke_with_mcp(session, llm, query)

async def run_sse_with_resources(query):
    query = (
        f"You are a smart AI assistant, and I want you to tell me {query}. "
        "Please understand the question properly, make use of tools only if needed, "
        "Only make use of resources and documents which are provided to you, "
        "and provide the final answer in a single line."
    )

    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Get resources
            resources = await session.list_resources()
            print("\n=== AVAILABLE RESOURCES ===")
            for desc, items in resources:
                if desc == "resources" and items:
                    root_resource = await session.read_resource(items[0].name)
                    break
            resource_file_info = json.loads(root_resource.contents[0].text)
            resource_file_names = [r.get('name')  for r in resource_file_info]

            templates = await session.list_resource_templates()
            uri_template = templates.resourceTemplates[0].uriTemplate
            docs = []
            for file_name in resource_file_names:
                resources = await session.read_resource(uri_template.format(name=file_name))
                for resource, items in resources:
                    if items:
                        page_content = items[0].text
                        docs.append(Document(
                                page_content=page_content,
                                metadata={
                                    "source": file_name,
                                    "type": "document"
                                }
                            ))

            # Create vector database
            db = create_vector_db(docs)

            qa_chain = RetrievalQA.from_chain_type(
            llm=get_llm_model("anthropic"),
            chain_type="stuff",  # Simple method to stuff all documents into the prompt
            retriever=db.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
            )
            result = qa_chain({"query": query})
            print("\n====== Anthropic =======")
            print(query)
            print(result["result"], [doc.metadata["source"] for doc in result["source_documents"]])

if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Run both providers in sequence within the same event loop
        print("\n Invoke Anthropic with resources")
        await run_sse_with_resources("Give me area of forangle with base 5 and height 10")

        print("\n=== Anthropic ===")
        await run("stdio", "anthropic", "What is (1 * 2) divide by 10?")
        print("\n=== ChatGroq ===")
        await run("sse", "groq", "What is (1 * 2) divide by 10?")
        
        print("\n=== Anthropic ===")
        await run("sse", "anthropic", "What is the capital of USA?")
        print("\n=== ChatGroq ===")
        await run("sse", "groq", "What is the capital of USA?")

    # Use a single event loop for all async operations
    asyncio.run(main())