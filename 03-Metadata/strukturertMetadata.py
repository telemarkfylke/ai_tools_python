# Henter ut tekst fra pdf-filer som ligger i en mappestruktur og lagrer i en tekstfil i samme mappe.

import os
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from openai import OpenAI
import pprint as pp
from pydantic import BaseModel
from enum import Enum

import os
from dotenv import load_dotenv
load_dotenv()

class Kategorier(str, Enum):
    økonomi = "økonomi"
    prosjekt = "prosjekt"
    annet = "annet"

class Kategorisering(BaseModel):
    tittel: str
    sammendrag: str
    epostadresse: str
    kategorier: list[str]
    kat2: Kategorier

client = OpenAI()

systemprompt = """
Du vil motta tekstutdrag fra ulike dokumenter. Din oppgave er å analysere konteksten og vurdere hvilken kategori teksten tilhører. Kategoriene er:
1. økonomi: Teksten inneholder informasjon relatert til økonomi, finans, regnskap, budsjett, eller lignende.
2. prosjekt: Teksten inneholder informasjon relatert til prosjekter, prosjektstyring, prosjektplaner, eller lignende.
3. annet: Hvis teksten ikke passer inn i noen av de ovennevnte kategoriene, skal den kategoriseres som 'annet'.

Svar med en kort oppsummering av teksten og angi hvilken kategori teksten tilhører.
"""

# Henter ut tekst fra pdf-filer som ligger i en mappestruktur og lagrer i en tekstfil i samme mappe.
def lagMetadata(mappe):
    for root, dirs, files in os.walk(mappe):
        for fil in files:
            if fil.endswith('.txt'):
                loader = TextLoader(os.path.join(root, fil))
                docs = loader.load()
                metadata = client.beta.chat.completions.parse(
                     model="gpt-4o-2024-11-20",
                     messages=[
                         {"role": "system", "content": systemprompt},
                         {"role": "user", "content": str(docs[0])},
                         ],
                         response_format=Kategorisering,
                         )
                print(len(docs))
                print(f"Oppsummering av {fil}:")
                pp.pprint(metadata.choices[0].message.parsed)
                # Write oppsummering to file in the current folder. Filename is "Vedleggtxt.txt".
                # with open(os.path.join(root, f"{fil}-vedleggtxt.txt"), "w") as f:
                #     f.write(f"Oppsummering av {fil}:\n")
                #     f.write(metadata.content)

lagMetadata('./uttrekk')