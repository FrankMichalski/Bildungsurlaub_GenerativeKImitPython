#%% Pakete
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()
import base64
#%% Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
# %% Test, ob API Key verfügbar ist
os.getenv("OPENROUTER_API_KEY")

#%% Sprachmodellinstanz erstellen
model = ChatOpenRouter(
    model="nvidia/nemotron-3.5-super-vl:free", 
    # api_key=os.getenv("OPENROUTER_API_KEY")
    )  

#%% Bild laden
user_prompt = "Was ist auf dem Bild zu sehen?"
img_path = "kiki.jpg"
encode_image(img_path)

# %%
messages = [
    ("system", """
    Du bist ein Experte für Bildanalyse.
    Du analysierst Bilder und beschreibst was du siehst.
    Du bist sehr detailiert und beschreibst alles was du siehst.
    """),    
    {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image(img_path)}"      }
                }]
        }
        ]


# %% Prompt Template
prompt_template = ChatPromptTemplate.from_messages(messages)
# # %%

# %% Chain verbinden
chain = prompt_template | model

# %% Chain ausführen
res = chain.invoke(input={})
# %%
from pprint import pprint
pprint(res.content)
# %%