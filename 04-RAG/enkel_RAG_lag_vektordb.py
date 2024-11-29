from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import pprint as pp
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY =  os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(model_name="gpt-4o-2024-11-20", temperature=0)
folderpath = "./dokumenter/"

# Laster inn dokumentene fra PDF-filen og klar
loader = PyPDFLoader("./dokumenter/MB_bm.pdf")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# Lager og lagrer vektordatabasen på disk
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model="text-embedding-3-large"), persist_directory="./vectorstore")

