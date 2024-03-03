from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

ollama = Ollama(base_url='http://localhost:11434', model="llama2")

loader = WebBaseLoader("https://en.wikipedia.org/wiki/Norway")
data = loader.load()

text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = text_splitter.split_documents(data)

oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

question="Give me a short summary of the most important facts about Norway"
docs = vectorstore.similarity_search(question)
print(len(docs))

qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
res = qachain.invoke({"query": question})

print(res["result"])
