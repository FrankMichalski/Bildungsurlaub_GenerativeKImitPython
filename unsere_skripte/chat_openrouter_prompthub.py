#%% Pakete
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate 
import os
from dotenv import load_dotenv
load_dotenv()
# Create a LangSmith API in Settings > API Keys
# Make sure API key env var is set:
# import os; os.environ["LANGSMITH_API_KEY"] = "<your-api-key>"
from langsmith import Client

client = Client()
prompt = client.pull_prompt("smithing-gold/assumption-checker", dangerously_pull_public_prompt=True)
from pprint import pprint
pprint(prompt)
# %% Umgebungsvariablen zugreifen
os.getenv("OPENROUTER_API_KEY")

#%% Auf ein Modell zugreifen
MODEL_NAME = "deepseek/deepseek-v4.1-flash-1017"
model = ChatOpenRouter(model=MODEL_NAME)

#%% Kette verbinden
chain = prompt | model

# %% Anfrage an die Kette senden
inputs = {
    'question': 'Warum sollte man nach dem Essen 30 Minuten nicht schwimmen?',
}
res = chain.invoke(inputs)

# %% Was kam vom Modell zurück?
from rich.console import Console
from rich.markdown	 import Markdown
console = Console()
console.print(Markdown(res.content))
