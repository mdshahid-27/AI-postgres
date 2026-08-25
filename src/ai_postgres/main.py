import os, json
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from ai_postgres.tools.curd import create_user, create_book, create_author, create_slot, update_user, update_book, update_author, update_slot
from ai_postgres.tools.curd import book_start_from, book_end_with, total_slots, view_genres, search_book, search_author, search_user, search_book_isavail
from ai_postgres.tools.curd import get_all_authors, get_all_books, get_all_slots, get_all_users
from ai_postgres.tools.curd import delete_author, delete_book, delete_slot, delete_user, search_books_by_description

load_dotenv()

QUERIES_FILE = 'data/queries.json'
HISTORY_FILE = 'data/history.json'

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

tools = [create_user,
        create_book, 
        create_author, 
        create_slot, 
        update_user, 
        update_book, 
        update_author, 
        update_slot,
        book_start_from, 
        book_end_with, 
        total_slots, 
        view_genres, 
        search_book, 
        search_author, 
        search_user, 
        search_book_isavail,
        get_all_authors, 
        get_all_books, 
        get_all_slots, 
        get_all_users,
        delete_author, 
        delete_book, 
        delete_slot, 
        delete_user,
        search_books_by_description]

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(data: ChatRequest):
    queries = load_file(QUERIES_FILE)
    last_five_queries = queries[-5:]
    memory = "\n".join(last_five_queries)
    
    prompt = f"""
    CONVERSATION CONTEXT
    The following contains some of the user's recent questions.
    IMPORTANT:
    - This information is provided ONLY to maintain conversational continuity.
    - Do NOT answer these previous questions.
    - Do NOT assume that the user is asking any of these questions again.
    - Use this information only when it helps understand the CURRENT USER MESSAGE.
    - The current user message always has priority.
    
    Previous user questions:
    {memory}
    
    CURRENT USER MESSAGE
    This is the user's actual request. Answer ONLY the current user message:
    {data.message}
    """
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", 
        contents=prompt,
        config={
            "system_instruction": (
                "Your name is : MegaTron, you're an library management and general purpose AI"
                "You must use your available tools to find accurate, real-time facts before answering any user question. "
                "Do not rely only on memory if a tool can check the data. "
                "Always run a tool call when you need specific numbers, current events, locations, or factual lookups."
                "if user asks to search anything from web, then use your knowledge to answer the user"
            ),
            "tools": tools
        }
    )
    
    
    answer = response.text
    

    queries.append(data.message)
    save_file(QUERIES_FILE, queries)

    history = load_file(HISTORY_FILE)
    history.append({"user": data.message, "assistant": answer})
    save_file(HISTORY_FILE, history)
    
    return {"response": answer}
