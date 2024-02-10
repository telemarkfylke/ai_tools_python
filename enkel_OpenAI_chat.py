from openai import OpenAI
import pprint as pp
client = OpenAI()

message_history = [
    {"role": "system", "content": "You are a helpful assistant. Always answer the user's questions in Norwegian as polite as possible."},
  ]

while True:
    message_history.append({"role": "user", "content": input("Tast inn spørsmål: ")})
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=message_history
    )
    message_history.append({"role": "system", "content": completion.choices[0].message.content})
    pp.pprint(message_history)
    
