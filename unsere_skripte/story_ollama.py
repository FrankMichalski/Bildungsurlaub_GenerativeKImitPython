#%% Pakete
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

#%% Promptvorlage
# Aufgabe: Geschichte über eine Person ({character}) in einer Situation ({location})
messages = [
    ("system", """
        Du schreibst kurze, anschauliche Geschichten auf Deutsch.
        Die Geschichte handelt von der genannten Person an dem genannten Ort.
    """),
    ("user", "Schreibe eine Geschichte über {character} in folgender Situation: {location}.")
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt_template

#%% Auf ein Modell zugreifen
MODEL_NAME = "qwen3.5:2b"
model = ChatOllama(model=MODEL_NAME, temperature=2)

#%% Kette verbinden: Prompt Template | LLM
chain = prompt_template | model
chain
# %% Anfrage an die Kette senden (User Input)
inputs = {
    "character": "Harry Potter",
    "location": "International Space Station",
}
assistant_message = chain.invoke(inputs)

# %% Was kam vom Modell zurück?
from pprint import pprint
pprint(assistant_message.content)

#%% Metadaten anzeigen
assistant_message.response_metadata

#%%
