import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel

load_dotenv()

QUERIES_FILE = "data/queries.json"
HISTORY_FILE = "data/history.json"
MCP_SERVER_MODULE = "ai_postgres.mcp_server"

app = FastAPI()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite", 
    google_api_key=os.getenv("API_KEY")
)

def load_file(file_name):
    if not os.path.exists(file_name):
        return []
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

def save_file(file_name, data):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: ChatRequest):
    queries = load_file(QUERIES_FILE)
    last_five_queries = queries[-5:]
    memory = "\n".join(last_five_queries)

    mcp_client = MultiServerMCPClient(
        {
            "ai_postgres": {
                "transport": "stdio",
                "command": sys.executable,
                "args": ["-m", MCP_SERVER_MODULE],
            }
        }
    )
    
    tools = await mcp_client.get_tools()

    system_prompt = (
        "You are MegaTron, a library management and general-purpose AI.\n\n"
        "CONVERSATION CONTEXT:\n"
        f"Previous user questions:\n{memory}"
    )

    agent_executor = create_agent(llm, tools, system_prompt=system_prompt)

    result = await agent_executor.ainvoke(
        {"messages": [HumanMessage(content=data.message)]}
    )

    answer = result["messages"][-1].content

    queries.append(data.message)
    save_file(QUERIES_FILE, queries)

    history = load_file(HISTORY_FILE)
    history.append({"user": data.message, "assistant": answer[0]['text']})
    save_file(HISTORY_FILE, history)

    return {"response": answer[0]['text']}


