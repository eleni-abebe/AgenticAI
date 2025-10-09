from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool, save_to_file

# Load environment variables
load_dotenv()

# Define the structure of the research output
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini")
# llm2 = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Create parser and prompt
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that helps generate structured research outputs.
            Answer the user query and use the necessary tools.
            Wrap your output exactly in this format and provide no other text:
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Register tools
tools = [search_tool, wiki_tool, save_tool]

# Create the agent and executor
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Ask the user for a research topic
query = input("What can I help you research? ")

# Run the agent
raw_response = agent_executor.invoke({"query": query})

# Parse and save the output
try:
    structured_response = parser.parse(raw_response.get("output"))
    print("\n✅ Structured Research Output:")
    print(structured_response)

    # Save the formatted version
    save_to_file(structured_response, "research_output.txt")

except Exception as e:
    print("⚠️ Error parsing output:", e)
