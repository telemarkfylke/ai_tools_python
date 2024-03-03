import ollama
from ollama import Client

client = Client(host='http://localhost:11434')

stream = ollama.chat(
    model='gemma',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)