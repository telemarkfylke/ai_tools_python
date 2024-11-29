# Test av lokal embeddingmodell

from langchain_nomic import NomicEmbeddings

embeddings = NomicEmbeddings(
    model='nomic-embed-text-v1.5',
    inference_mode='local',
    device='gpu',
)

result = embeddings.embed_documents(['text to embed'])
print(result)