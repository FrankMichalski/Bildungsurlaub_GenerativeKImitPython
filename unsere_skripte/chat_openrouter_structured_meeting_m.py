#%% Pakete
import json
from langchain_openrouter import ChatOpenRouter
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field  # langchain_core.pydantic_v1 existiert in der installierten Version nicht mehr
from dotenv import load_dotenv

load_dotenv()  # liest die .env-Datei mit dem API-Key ein

#%% Schritt 1: Ausgabeschema definieren
# Hier legen wir fest, wie das Ergebnis aussehen soll.
# Die Beschreibungen (description=...) verstehen auch das LLM und
# erklären ihm, welche Information in welches Feld gehört.

class Aufgabe(BaseModel): 
    beschreibung: str = Field(description="Was muss getan werden?")
    verantwortlich: str = Field(description="Wer ist zuständig? Wenn nicht genannt: 'nicht genannt'")
    frist: str = Field(description="Bis wann? Wenn nicht genannt: 'nicht genannt'")


class MeetingProtokoll(BaseModel):
    thema: str = Field(description="Worum geht es im Meeting? Ein kurzer Satz")
    teilnehmer: list[str] = Field(description="Alle im Transkript genannten Personen")
    zusammenfassung: str = Field(description="Die wichtigsten Punkte in 3 bis 5 Sätzen")
    entscheidungen: list[str] = Field(description="Was wurde beschlossen?")
    aufgaben: list[Aufgabe] = Field(description="Alle Aufgaben (To-dos) aus dem Meeting")


#%% Schritt 2: Parser erstellen
# Der Parser macht zwei Dinge:
#  a) get_format_instructions() erzeugt eine Anleitung für das LLM (JSON-Schema)
#  b) parst die Antwort des LLM am Ende in ein Python-Dict
parser = JsonOutputParser(pydantic_object=MeetingProtokoll)

#%% Schritt 3: Promptvorlage
# {format_instructions} wird über .partial() mit der Anleitung aus Schritt 2 befüllt.
# {transkript} wird später beim Aufruf der Kette eingesetzt.
messages = [
    ("system", """
        Du bist ein Protokollant und erstellst aus einem Meeting-Transkript ein Protokoll.
        Erfinde keine Informationen, die nicht im Transkript stehen.
        Halte dich strikt an die Formatanweisungen: {format_instructions}
    """),
    ("user", "Meetingtranskript:\n{transkript}"),
]
prompt_template = ChatPromptTemplate.from_messages(messages).partial(
    format_instructions=parser.get_format_instructions()
)

#%% Schritt 4: Modell
# temperature=0 -> möglichst deterministische Ausgabe, wichtig bei strukturiertem Output
MODEL_NAME = "deepseek/deepseek-v4.1-flash-1017"
model = ChatOpenRouter(model=MODEL_NAME, temperature=0)

#%% Schritt 5: Kette verbinden (Pipe-Operator "|")
# Die Daten fließen von links nach rechts:
#   Eingabe-Dict -> Prompt -> Modell -> Parser -> Ergebnis
chain = prompt_template | model | parser

#%% Schritt 6: Beispiel-Transkript und Aufruf
transkript = """
Anna: Guten Morgen, wir sollten heute über die neue Website sprechen.
Ben: Ja. Die Startseite lädt zu langsam, das muss bis zum 15.12.2026 gefixt werden.
Clara: Ich kann mich um die Bilder kümmern, die sind zu groß.
Anna: Gut, Clara, bitte bis zum 05.12.2026.
Ben: Wir haben uns außerdem entschieden, Hosting-Anbieter zu wechseln.
Anna: Richtig. Ben, kannst du bis Ende der Woche zwei Angebote einholen?
Ben: Mache ich.
"""

res = chain.invoke({"transkript": transkript})

#%% Schritt 7: Ausgabe
# res ist ein Python-Dict, z.B. res["aufgaben"][0]["verantwortlich"]
print(json.dumps(res, ensure_ascii=False, indent=2))
