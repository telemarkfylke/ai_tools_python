from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY =  os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

folderpath = "./dokumenter/"

system_prompt = (
    "Du er ekspert på klassifisering av dokumenter. Du skal alltid svare på norsk. Du skal klassifisere vedlagte dokument. Hvilken kategori tilhører dokumentet? Svar med ett eller to ord som klassifiserer dokuementet på riktig måte. Du skal også skrive to setninger som beskriver dokumentet på riktig måte. Skriv svaret som gyldig JSON-kode med nøklene 'filnavn', 'kategori' og 'beskrivelse'"
    "Ikke ta med personopplysninger i beskrivelsen."
    "Ikke ta med sensitive opplysninger i beskrivelsen."
    "Ikke ta med konfidensielle opplysninger i beskrivelsen."
    "Ikke ta med helseopplysninger i beskrivelsen."
    "Ikke ta med opplysninger om straffbare forhold i beskrivelsen."
    "Ikke ta med detlajer om lønn i beskrivelsen."
    "Ikke ta med personnnunmer i beskrivelsen."
    "Responsen skal være gyldig JSON-kode på formatet: {'filnavn': 'dokumentets filnavn', 'kategori': 'dokumentets kategori', 'beskrivelse': 'dokumentets beskrivelse'}"    
    "Dokumentets filnavn og innhold er som følger:"
)


# Kjør kategorisering på hvert dokument i mappa
for filename in os.listdir(folderpath):
    loader = PyPDFLoader(folderpath + filename)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Henter ut blokker med tekst fra dokumentet som er relevante for ledeteksten
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    docContent = ""
    for doc in docs:
        # print(doc.page_content)
        docContent += doc.page_content

    llm_response = llm.invoke(system_prompt + docContent)

    # # Skriver ut "Kategori" og "Beskrivelse" fra dokumentene i mappa"
    with open("katDok.json", "a") as f:
        f.write(llm_response.content + ",\n")

    print("-------------------")
    print(filename)
    print(llm_response.content)
    print("-------------------")