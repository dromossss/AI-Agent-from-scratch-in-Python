from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv() #to load  env variables files (.env)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
response=llm.invoke("Whhy dont't we ride cows?")
print(response)