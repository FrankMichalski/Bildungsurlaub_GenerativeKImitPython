#%% Pakete
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate 
import os
from dotenv import load_dotenv
load_dotenv()
# %% Umgebungsvariablen zugreifen
os.getenv("OPENROUTER_API_KEY")

#%% Promptvorlage
messages = [
    ("system", """
        Du bist ein Witzeerzähler.
        Der Nutzer übergibt dir ein Thema und du erzählst einen kurzen Witz.
    """),
    ("user", "Thema: {topic}")
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt_template

#%% Auf ein Modell zugreifen
MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"
model = ChatOpenRouter(model=MODEL_NAME)

#%% Kette verbinden
chain = prompt_template | model

# %% Anfrage an die Kette senden
inputs = {
    'topic': 'erzähl mir einen Witz'
}
res = chain.invoke(inputs)

# %% Was kam vom Modell zurück?
from pprint import pprint
pprint(res.content)

#%% Metadaten anzeigen
res.response_metadata

#%%

