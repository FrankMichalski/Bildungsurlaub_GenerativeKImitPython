#%% Pakete
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate 
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
load_dotenv()

# %%
web_search = TavilySearch(max_results=5)
# web_search.invoke("Was ist gestern im Bereich KI passiert?")

#%% Modelinstanz erstellen
MODEL_NAME = "deepseek/deepseek-v4.1-flash-1017"
model = ChatOpenRouter(model=MODEL_NAME)

#%% Agent (LLM + Tools) erstellen
agent = create_agent(
    model=model, 
    tools=[web_search],
    system_prompt="""
        Du bist ein hilfreicher Assistent.
        Du antwortest kurz und bündig.
    """)
    

# %%
messages = [
    ("user", "Wann bekommt Nvidia einen neuen CEO?")
]
res = agent.invoke({"messages": messages})

#%% Antwort des Modells herausschälen
model_answer = res["messages"][-1].content

# %%
from rich.console import Console
from rich.markdown import Markdown
console = Console()
console.print(Markdown(model_answer))

# %%
 