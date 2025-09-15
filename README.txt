🧠 Research AI Assistant

A modern desktop application that lets you chat with an AI assistant to perform quick research, retrieve information, and save notes — all within a stylish graphical interface built with Tkinter and ttkbootstrap, powered by LangChain and the Groq API.

✨ Features

💬 AI Chat Interface — Talk with an AI model powered by Groq (LLaMA 3.1 8B).

🧩 Tool-Using Agent — The AI can call three tools:

search: Simulates searching the web

wikipedia: Simulates getting Wikipedia summaries

save_research: Saves content

💻 Modern UI — Clean dark theme using ttkbootstrap for a polished look.

📄 Auto-saving — Saves responses or research notes via the save_research tool.

⚡ Lightweight and Fast — No heavy dependencies; quick startup.

📦 Requirements

Make sure you have Python 3.10+ installed.
Install dependencies with:

pip install langchain langchain-openai python-dotenv pydantic ttkbootstrap

⚙️ Setup

Clone this repository or copy the script to a local folder.

Create a .env file in the project root with your Groq API key:

GROQ_API_KEY=your_groq_api_key_here


Run the app:

python app.py

🖥️ Usage

Type a question or topic in the input box.

Press Enter or click Send.

The AI will respond in the chat area.

Click Clear to reset the conversation.

💡 Tip: Keep messages under 100 words — longer inputs are blocked.

⚙️ Architecture Overview

LangChain Agent with create_tool_calling_agent

Tools implemented using langchain.tools.Tool

Chat Interface using Tkinter + ttkbootstrap

Prompts managed with ChatPromptTemplate

Model: llama-3.1-8b-instant through the Groq API

📸 UI Preview

Top Bar: Title and clear chat button

Middle Section: Scrollable chat area with color-coded messages

Bottom Section: Input box and send button

⚠️ Notes

Current search and wikipedia tools are placeholders returning fake data.

Replace their functions with real implementations as needed.

Do not exceed 100 words per message.

📜 License

MIT License — feel free to modify and use this project.