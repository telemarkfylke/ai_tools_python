from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import pprint as pp
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY =  os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(model_name="gpt-4o-2024-11-20", temperature=0)
folderpath = "./dokumenter/"

system_prompt = ("Svar på spørsmålet basert kun på den gitte konteksten. Den viktigste informasjon som kan gis som svar er kildene henvist i konteksten, men bør ha en assosiert tekst. Kilder fra kontekst skal legges ved i svaret som 'Andre relevante sider:")
user_prompt = "Forklar hvordan man løser oppgave 4.3.2a?"
embedding = OpenAIEmbeddings(model="text-embedding-3-large")
db = Chroma(persist_directory="./vectorstore", embedding_function=embedding)

# Henter relevante dokumenter fra vektordatabasen basert på brukerens spørsmål
retreived_docs = db.similarity_search(user_prompt, k=5)
print("Retreived docs: ", retreived_docs)

docs = ""
for doc in retreived_docs:
    docs += doc.page_content

llm_response = llm.invoke(system_prompt + user_prompt + docs)

pp.pprint("-------------------")
pp.pprint(llm_response.content)
pp.pprint("-------------------")