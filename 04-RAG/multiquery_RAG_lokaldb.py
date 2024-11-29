from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import BaseOutputParser
from typing import List
from langchain_core.prompts import PromptTemplate

import json
import logging
import pprint as pp
import os
from dotenv import load_dotenv
load_dotenv()

# Output parser will split the LLM result into a list of queries
class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return list(filter(None, lines))  # Remove empty lines


QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines. Use Norwegian language.
    Original question: {question}""",
)

# Definerer modeller og vektordatabase
llm = ChatOpenAI(model_name="gpt-4o-2024-11-20", temperature=0)
output_parser = LineListOutputParser()
embedding = OpenAIEmbeddings(model="text-embedding-3-large")
db = Chroma(persist_directory="./vectorstore", embedding_function=embedding)

# Pipeline for å sette opp input til retruever
llm_chain = QUERY_PROMPT | llm | output_parser

# Other inputs
question = "Forklar hvordan man løser oppgave 4.3.2a?"



# Henter relevante dokumenter fra vektordatabasen basert på brukerens spørsmål (Fem varianter av spørsmålet)
retriever = MultiQueryRetriever(retriever=db.as_retriever(), llm_chain=llm_chain, verbose=True)
print("Retrieving documents...")
# Log queries
logging.basicConfig(level=logging.INFO)
logging.getLogger("langchain").setLevel(logging.INFO)

unique_docs = retriever.invoke(question)
pp.pprint(unique_docs)



# Results


NewQuery = f"Svar på {question} basert på den gitte konteksten. Kontekst: {unique_docs}"

r = llm.invoke(NewQuery)

pp.pprint(json.dumps(r.content, indent=4))