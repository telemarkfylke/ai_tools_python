# Henter ut tekst fra pdf-filer som ligger i en mappestruktur og lagrer i en tekstfil i samme mappe.

import os
from langchain_community.document_loaders import PyPDFLoader
from openai import OpenAI
import pprint as pp

import os
from dotenv import load_dotenv
load_dotenv()

# Henter ut tekst fra pdf-filer som ligger i en mappestruktur og lagrer i en tekstfil i samme mappe.
def pdf_til_tekst(mappe):
    for root, dirs, files in os.walk(mappe):
        for fil in files:
            if fil.endswith('.pdf'):
                loader = PyPDFLoader(os.path.join(root, fil))
                docs = loader.load()
                # Write docs[0] to file in current folder
                with open(os.path.join(root, fil.replace('.pdf', '.txt')), 'w') as file:
                    for doc in docs:
                        file.write(str(doc))

pdf_til_tekst('./uttrekk')