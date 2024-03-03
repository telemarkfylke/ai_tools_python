import ollama
from ollama import Client

client = Client(host='http://localhost:11434')

historikk = []
kontekst = "You are Shakespeare. Always answer as if you were Shakespeare."

historikk.append({'role': 'system', 'content': kontekst})

while True:
    historikk.append({'role': 'user', 'content': input("Nytt spm: ")})
    respons = ollama.chat(
        model='gemma',
        messages=historikk,
        stream=False,
    )
    historikk.append({'role': 'assistant', 'content': respons['message']['content']})
    print(historikk)