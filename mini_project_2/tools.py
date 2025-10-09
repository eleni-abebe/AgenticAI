from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# ✅ Custom save function with nice formatting
def save_to_file(data: dict | str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d")

    # Handle both dict-like and string data
    if isinstance(data, dict):
        topic = data.get("topic", "")
        summary = data.get("summary", "")
        sources = "\n".join(f"- {s}" for s in data.get("sources", []))
        tools_used = "\n".join(f"- {t}" for t in data.get("tools_used", []))
    else:
        # For Pydantic object or other types, convert to str
        try:
            topic = getattr(data, "topic", "N/A")
            summary = getattr(data, "summary", str(data))
            sources = "\n".join(f"- {s}" for s in getattr(data, "sources", []))
            tools_used = "\n".join(f"- {t}" for t in getattr(data, "tools_used", []))
        except Exception:
            topic = "N/A"
            summary = str(data)
            sources = tools_used = "N/A"

    formatted_text = f"""
-- Research Output --
Timestamp: {timestamp}

🧠 Topic:
{topic}

📄 Summary:
{summary}

📚 Sources:
{sources}

🧰 Tools Used:
{tools_used}

{'=' * 50}

"""

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"✅ Data successfully saved to {filename}"

# Create a Tool wrapper so the agent can use it directly
save_tool = Tool(
    name="save_to_file",
    func=save_to_file,
    description="Save research results to a local text file.",
)

# Wikipedia search tool
wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# DuckDuckGo search tool
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search_web",
    func=search.run,
    description="Search the web for information using DuckDuckGo.",
)
