from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceHub

import logging

from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from langchain_community.llms import Ollama

import pprint as pp
import dotenv
dotenv.load_dotenv()

# Laster inn dokumentet
loader = UnstructuredPDFLoader("./orden.pdf", mode="single", strategy="fast")
doc = loader.load()

# Konteks som skal brukes i spørsmålet
# kontekst = "Du er ekspert på matematikk og skal alltid svare på med et enkelt og forståelig språk. Svar alltid på norsk. På slutten av responsen skal du alltid skrive teksten: 'Husk at responsen fra denne chatboten kan være upresis eller faktisk feil. Det er derfor viktig at du sjekker informasjonen du får her med med informasjon fra kilden.'";

# Splitter og lager en vectorstore av dokumentet
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)
all_splits = text_splitter.split_documents(doc)
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# Løkke som lar brukeren stille spørsmål til dokumentet
while True:
    question = input("Tast inn ditt spørsmål: ")
    docs = vectorstore.similarity_search(question)

    logging.basicConfig()
    logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

    retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=ChatOpenAI(temperature=0))
    unique_docs = retriever_from_llm.get_relevant_documents(query=question)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0)
    llm2 = HuggingFaceHub(repo_id="RuterNorway/Llama-2-13b-chat-norwegian-GPTQ", model_kwargs={"temperature":0, "max_new_tokens":250})
    llm3 = Ollama(model="gemma")
    qa_chain = RetrievalQA.from_chain_type(llm3,retriever=vectorstore.as_retriever())
    pp.pprint(qa_chain({"query": question})["result"])
    # pp.pprint(docs)
    print("\n")