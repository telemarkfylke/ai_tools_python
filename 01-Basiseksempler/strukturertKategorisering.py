from pydantic import BaseModel
from openai import OpenAI
import json
import pprint as pp

import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

class Kategorisering(BaseModel):
    tittel: str
    sammendrag: str
    epostadresse: str
    kategorier: list[str]

folderpath = "./ukategorisert/"

system_prompt = (
    "Du er ekspert på klassifisering av eposter. Du skal alltid svare på norsk. Du skal klassifisere vedlagte epost. Hvilken kategori tilhører eposten? Svar med ett eller to ord som klassifiserer dokuementet på riktig måte. Du skal også skrive to setninger som beskriver eposten på riktig måte."
    "Ikke ta med personopplysninger i beskrivelsen."
    "Ikke ta med sensitive opplysninger i beskrivelsen."
    "Ikke ta med konfidensielle opplysninger i beskrivelsen."
    "Ikke ta med helseopplysninger i beskrivelsen."
    "Ikke ta med opplysninger om straffbare forhold i beskrivelsen."
    "Ikke ta med detlajer om lønn i beskrivelsen."
    "Ikke ta med personnnunmer i beskrivelsen."
    "Epostens og innhold er som følger:"
)

innhold = []

# For hver epost i eposdata.json kjør kategorisering
with open('epostdata.json', 'r') as file:
    epostdata = json.load(file)

for epost in epostdata:
    messageBody = str(epost.get('subject')) + str(epost.get('body')[:10000]) + str(epost.get('toRecipients'))
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": messageBody},
        ],
        response_format=Kategorisering,
    )

    kat = completion.choices[0].message.parsed

    pp.pprint("Tittel: " + kat.tittel)
    pp.pprint("Sammendrag: " + kat.sammendrag)
    pp.pprint("Epost: " + kat.epostadresse)
    pp.pprint(kat.kategorier)
    print("-------------------")

    # Legg til hver kategorisering i listen innhold
    innhold.append({
        'tittel': kat.tittel,
        'sammendrag': kat.sammendrag,
        'epostadresse': kat.epostadresse,
        'kategorier': kat.kategorier
    })

# Skriv kategoriseringene til en fil
with open('kategorisering.json', 'w') as file:
    json.dump(innhold, file, indent=4)



