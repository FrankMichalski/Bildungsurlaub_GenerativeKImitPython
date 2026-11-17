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
        Du bist ein Geschichtenerzähler im Stile von {author}.
        Schreibe eine Geschichte über eine Person in einer bestimmten situation {location}.
    """),
    ("user", "Thema: {topic}")
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt_template

#%% Auf ein Modell zugreifen
MODEL_NAME = "deepseek/deepseek-v4.1-flash-1017"
model = ChatOpenRouter(model=MODEL_NAME, temperature=1)

#%% Kette verbinden
chain = prompt_template | model

# %% Anfrage an die Kette senden
inputs = {
    'author': 'J. K. Rowling',
    'location': 'Hogwarts',
    'topic': 'Monster'
}
res = chain.invoke(inputs)

# %% Was kam vom Modell zurück?
from pprint import pprint
pprint(res.content)

#%% Metadaten anzeigen
res.response_metadata

#%%

 