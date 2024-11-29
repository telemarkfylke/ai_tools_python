# Henter ut tekst fra pdf-filer som ligger i en mappestruktur og lagrer i en tekstfil i samme mappe.

import os
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
import pprint as pp

import os
from dotenv import load_dotenv
load_dotenv()

client = ChatOpenAI(model="gpt-4o")
systemprompt = "Vedlagt er tekst som er hentet fra et vedlegg til en epost. Skriv en kort oppsummering av teksten. Ta med viktig informasjon som firmanavn, epostadresser, henvisninger til lover, regler eller prosjekt og tilsvarende. Her er teksten:"

# Henter ut tekst fra pdf-filer som ligger i en mappestruktur og lagrer i en tekstfil i samme mappe.
def lagMetadata(mappe):
    for root, dirs, files in os.walk(mappe):
        for fil in files:
            if fil.endswith('.txt'):
                loader = TextLoader(os.path.join(root, fil))
                docs = loader.load()
                oppsummering = client.invoke(f"{systemprompt} {docs[0]}")
                print(len(docs))
                print(f"Oppsummering av {fil}:")
                print(oppsummering.content)
                # Write oppsummering to file in the current folder. Filename is "Vedleggtxt.txt".
                with open(os.path.join(root, f"{fil}-vedleggtxt.txt"), "w") as f:
                    f.write(f"Oppsummering av {fil}:\n")
                    f.write(oppsummering.content)

lagMetadata('./uttrekk')