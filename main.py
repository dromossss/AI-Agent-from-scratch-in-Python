import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# =======================
# SETUP LLM
# =======================
load_dotenv()

llm = ChatOpenAI(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# =======================
# TOOLS
# =======================
class QueryInput(BaseModel):
    query: str = Field(description="The search or topic query")

class ContentInput(BaseModel):
    content: str = Field(description="The content to save")

def search_tool(query: str) -> str:
    return f"Search results for: {query} - (fake sample info)"

def wiki_tool(query: str) -> str:
    return f"Wikipedia info for: {query} - (fake sample summary)"

def save_tool(content: str) -> str:
    return f"Saved: {content[:50]}..."

def safe_call(func):
    def wrapper(x):
        if isinstance(x, dict):
            value = x.get("query") or x.get("content") or str(x)
        else:
            value = str(x)
        return func(value)
    return wrapper

tools = [
    Tool(
        name="search",
        func=safe_call(search_tool),
        args_schema=QueryInput,
        description="Search online information"
    ),
    Tool(
        name="wikipedia",
        func=safe_call(wiki_tool),
        args_schema=QueryInput,
        description="Get information from Wikipedia"
    ),
    Tool(
        name="save_research",
        func=safe_call(save_tool),
        args_schema=ContentInput,
        description="Save research content"
    )
]

# =======================
# PROMPT
# =======================
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful AI assistant. "
     "If the user asks for general info, just answer clearly. "
     "If they ask for deep research, you may use the available tools."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True)

# =======================
# GUI APP
# =======================
def send_message(event=None):
    user_msg = input_box.get("1.0", tk.END).strip()
    if len(user_msg.split()) > 100:
        messagebox.showerror("Error", "Message cannot exceed 100 words.")
        return
    if not user_msg:
        return

    timestamp = datetime.now().strftime("%H:%M")
    chat_area.config(state="normal")
    chat_area.insert(tk.END, f"[{timestamp}] 🧑 You: {user_msg}\n", "user")
    chat_area.config(state="disabled")
    chat_area.yview(tk.END)
    input_box.delete("1.0", tk.END)

    try:
        response = agent_executor.invoke({"input": user_msg})
        ai_msg = response.get("output") or str(response)
    except Exception as e:
        ai_msg = f"Error: {e}"

    timestamp = datetime.now().strftime("%H:%M")
    chat_area.config(state="normal")
    chat_area.insert(tk.END, f"[{timestamp}] 🤖 AI: {ai_msg}\n\n", "ai")
    chat_area.config(state="disabled")
    chat_area.yview(tk.END)

def clear_chat():
    chat_area.config(state="normal")
    chat_area.delete("1.0", tk.END)
    chat_area.config(state="disabled")

# =======================
# MODERN UI LAYOUT
# =======================
root = ttk.Window(themename="cyborg")
root.title("🧠 Research AI Assistant")
root.geometry("800x600")
root.minsize(500, 400)

root.rowconfigure(1, weight=1)   # make chat area expandable
root.columnconfigure(0, weight=1)

# Header
header_frame = ttk.Frame(root, padding=(10,5))
header_frame.grid(row=0, column=0, sticky="ew")
header_frame.columnconfigure(0, weight=1)

header = ttk.Label(header_frame, text="Research AI Assistant", font=("Segoe UI", 20, "bold"))
header.grid(row=0, column=0, sticky="w")

clear_button = ttk.Button(header_frame, text="Clear", bootstyle=SECONDARY, command=clear_chat)
clear_button.grid(row=0, column=1, sticky="e", padx=5)

# Chat area (with scrollbar)
frame_chat = ttk.Frame(root, padding=10)
frame_chat.grid(row=1, column=0, sticky="nsew")

chat_area = scrolledtext.ScrolledText(
    frame_chat, wrap=tk.WORD, state="disabled",
    bg="#1e1e1e", fg="white", font=("Segoe UI", 11),
    insertbackground="white", relief="flat"
)
chat_area.pack(fill=tk.BOTH, expand=True)

chat_area.tag_config("user", foreground="#4cc9f0")
chat_area.tag_config("ai", foreground="#f72585")

# Input + send
frame_input = ttk.Frame(root, padding=10)
frame_input.grid(row=2, column=0, sticky="ew")
frame_input.columnconfigure(0, weight=1)

input_box = tk.Text(
    frame_input, height=3, wrap=tk.WORD,
    bg="#2b2b2b", fg="white", font=("Segoe UI", 11),
    insertbackground="white", relief="flat"
)
input_box.grid(row=0, column=0, sticky="ew", padx=(0,10))

send_button = ttk.Button(
    frame_input, text="Send", bootstyle=SUCCESS, command=send_message
)
send_button.grid(row=0, column=1)

# Bind Enter (Shift+Enter for newline)
def handle_enter(event):
    if event.state & 0x0001:  # Shift pressed
        return
    send_message()
    return "break"

input_box.bind("<Return>", handle_enter)

root.mainloop()
