from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Dagen i dag er en fin dag å bygge noe på!"
)

response.write_to_file(speech_file_path)
