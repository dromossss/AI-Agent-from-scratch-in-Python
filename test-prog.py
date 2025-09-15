from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

# Use the current recommended model
llm = ChatOpenAI(
    model="llama-3.1-8b-instant",  
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = llm.invoke("Who is cristiano ronaldo in 3 saentences and name 2 qualities")
print(response.content)
