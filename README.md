# ai_tools_python
Diverse eksempler på bruk av ulike ai-tjenester. Koden er skrevet i Python for enkel prototyping og bruker ulike biblioteker for å kalle på tjenestene.

## Mappestruktur
📂 [01 - Basiseksempler](./01%20-%20Basiseksempler/) -> enkle eksempler med bruk av OpenAI-API'et.<br>
📂 [02 - Lokal LLM](./02%20-%20Lokal%20LLM/) -> eksempler med lokal språkmodell og Ollama

## Miljøvariabler
For å kunne kjøre eksemplene må du sette opp miljøvariabler for de ulike tjenestene. Dette gjøres ved å opprette en fil med navn .env i rotmappen. Filen skal inneholde følgende variabler:

```
OPENAI_API_KEY=sk-....
LANGCHAIN_API_KEY=ls__....
LANGCHAIN_PROJECT=<MyLangSmithProject>
LANGCHAIN_TRACING_V2 = true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
HUGGINGFACEHUB_API_TOKEN=hf_...
```
