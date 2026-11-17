#%% Pakete
from langchain_openrouter import ChatOpenRouter
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate 
import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown
console = Console()
#%% output parser
class MovieOutput(BaseModel):
    title: str
    director: str = Field(description="der Regisseur des Films", examples=["Spielberg, Steven", "Kubrick, Stanley"])
    main_actors: list[str]
    release_year: int
    box_office: int = Field(description="der weltweite Umsatz gemessen in Mio. $")


parser = JsonOutputParser(pydantic_object=MovieOutput)
from pprint import pprint

console.print(Markdown(parser.get_format_instructions()))

#%% Promptvorlage
messages = [
    ("system", """
        Du bist ein Filmexperte und lieferst den wahrscheinlichsten Film zurück.
        Der Nutzer übergibt dir eine Filmbeschreibung.
        Halte dich strikt an die Formatanweisungen: {format_instructions}
    """),
    ("user", "Filmbeschreibung: {description}")
]
prompt_template = ChatPromptTemplate.from_messages(messages).partial(format_instructions=parser.get_format_instructions())
prompt_template

#%% Auf ein Modell zugreifen
MODEL_NAME = "deepseek/deepseek-v4.1-flash-1017"
model = ChatOpenRouter(model=MODEL_NAME)

#%% Kette verbinden
chain = prompt_template | model | parser
chain
# %% Anfrage an die Kette senden
inputs = {
    'description': 'Viele Menschen sterben und ein maskierter Killer ist verantwortlich.'
}
res = chain.invoke(inputs)

#%% Ausgabe
res