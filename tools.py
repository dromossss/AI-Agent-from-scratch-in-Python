from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from pydantic import BaseModel, Field
from datetime import datetime

# -----------------------------
# Define schemas for tool inputs
# -----------------------------
class QueryInput(BaseModel):
    query: str = Field(description="The search or topic query")

class SaveInput(BaseModel):
    data: str = Field(description="The content to save into a text file")

# -----------------------------
# Tool functions
# -----------------------------
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

# -----------------------------
# Tool instances
# -----------------------------
# DuckDuckGo search
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=lambda x: search.run(x["query"]),
    args_schema=QueryInput,
    description="Search the web for information."
)

# Wikipedia
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)
wiki_tool = Tool(
    name="wikipedia",
    func=lambda x: wiki.run(x["query"]),
    args_schema=QueryInput,
    description="Get information from Wikipedia."
)

# Save to file
save_tool = Tool(
    name="save_text_to_file",
    func=lambda x: save_to_txt(x["data"]),
    args_schema=SaveInput,
    description="Saves structured research data to a text file."
)
