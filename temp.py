import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel

load_dotenv()

QUERIES_FILE = "data/queries.json"
HISTORY_FILE = "data/history.json"
MCP_SERVER_MODULE = "ai_postgres.mcp_server"
MCP_SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", MCP_SERVER_MODULE],
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


app = FastAPI()
client = genai.Client(api_key=os.getenv("API_KEY"))


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(data: ChatRequest):
    queries = load_file(QUERIES_FILE)
    last_five_queries = queries[-5:]
    memory = "\n".join(last_five_queries)

    async with Client(stdio_client(MCP_SERVER_PARAMS)) as mcp_client:
        tools = await mcp_client.list_tools()
        tool_catalog = "\n".join(
            f"- {tool.name}: {tool.description or 'No description'}"
            for tool in tools.tools
        )

        prompt = f"""
You are MegaTron, a library management and general-purpose AI.

CONVERSATION CONTEXT
The following contains some of the user's recent questions.
IMPORTANT:
- This information is provided only to maintain conversational continuity.
- Do not answer these previous questions.
- Do not assume the user is asking any of these questions again.
- Use this information only when it helps understand the current user message.
- The current user message always has priority.

Previous user questions:
{memory}

AVAILABLE MCP TOOLS
{tool_catalog}

CURRENT USER MESSAGE
{data.message}

Response format rules:
- If you need a tool, respond with JSON only in this shape:
  {{"action": "tool_call", "tool_name": "name_here", "arguments": {{}}}}
- If no tool is needed, respond with JSON only in this shape:
  {{"action": "final", "answer": "your answer here"}}
""".strip()

        first_response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )

        response_text = (first_response.text or "").strip()
        response_text = response_text.removeprefix("```json").removeprefix("```")
        response_text = response_text.removesuffix("```").strip()

        try:
            parsed = json.loads(response_text)
        except json.JSONDecodeError:
            parsed = {}

        if parsed and parsed.get("action") == "tool_call":
            tool_name = parsed.get("tool_name")
            tool_arguments = parsed.get("arguments", {})

            if not isinstance(tool_name, str) or not isinstance(tool_arguments, dict):
                answer = "The model produced an invalid MCP tool request."
            else:
                try:
                    tool_result = await mcp_client.call_tool(tool_name, arguments=tool_arguments)
                    normalized_result = getattr(tool_result, "structured_content", None)
                    if normalized_result is None:
                        normalized_result = getattr(tool_result, "structuredContent", None)

                    if normalized_result is None:
                        normalized_result = [
                            getattr(item, "text", str(item))
                            for item in (tool_result.content or [])
                        ]

                    follow_up_prompt = f"""
You are MegaTron. Answer the user naturally and clearly.
Do not mention JSON, MCP, or internal implementation details.

User message:
{data.message}

Tool used:
{tool_name}

Tool result:
{json.dumps(normalized_result, indent=2, ensure_ascii=False)}
""".strip()
                    final_response = await asyncio.to_thread(
                        client.models.generate_content,
                        model="gemini-3.1-flash-lite",
                        contents=follow_up_prompt,
                    )
                    answer = final_response.text or "I got the tool result, but no response text was returned."
                except Exception as exc:
                    answer = f"I could not run the MCP tool `{tool_name}`: {exc}"
        elif parsed and parsed.get("action") == "final":
            answer = str(parsed.get("answer", "")).strip() or (first_response.text or "")
        else:
            answer = first_response.text or ""

    queries.append(data.message)
    save_file(QUERIES_FILE, queries)

    history = load_file(HISTORY_FILE)
    history.append({"user": data.message, "assistant": answer})
    save_file(HISTORY_FILE, history)

    return {"response": answer}

