# Dette scriptet henter e-post fra en bruker i Microsoft Graph og skriver innholdet til en fil
# For å kjøre scriptet må du ha en token.txt fil med et gyldig token for Microsoft Graph
# Scriptet henter de 10 nyeste e-postene fra brukeren og skriver innholdet til en fil
# HTML-innholdet blir parsert med BeautifulSoup før det skrives til fil

import requests
import json
from bs4 import BeautifulSoup
import pprint as pp
import base64
from dotenv import load_dotenv
import os

# Laster miljøvariabler fra .env
load_dotenv()

# Setter diverse variabler
postboks = os.getenv("POSTBOKS")
token = os.getenv("TOKEN")
innhold = []

print(postboks)
print(token)

headers = {
    'Authorization': 'Bearer ' + token
}

params = {
    'top': 40,
    # '$select': 'importance, subject, body, toRecipients, from, hasAttachments, receivedDateTime',
    '$orderby': 'receivedDateTime desc'
}

# Henter epostene
response = requests.get(f'https://graph.microsoft.com/v1.0/users/{postboks}/messages/', headers=headers, params=params)
print(response)

# For hver epost hent ut innhold. Body må parses med beautifulsoup for å gjøre den lesbar for mennesker.
for value in response.json()['value']:
    importance = value['importance']
    subject = value['subject']
    body = "TestTestTest" # value['body']['content']
    soup = BeautifulSoup(body, 'html.parser')
    bodytext = soup.get_text()
    toRecipients = value['toRecipients']
    hasAttachments = value['hasAttachments']
    receivedDateTime = value['receivedDateTime']
    innholdjson = {
        'importance': importance,
        'subject': subject,
        'body': bodytext,
        'toRecipients': toRecipients,
        'hasAttachments': hasAttachments,
        'receivedDateTime': value['receivedDateTime']
    }
    if hasAttachments:
        message_id = value['id']
        print(message_id)
        vedlegg = []
        attachmentsResponse = requests.get(f'https://graph.microsoft.com/v1.0/users/{postboks}/messages/{message_id}/attachments/', headers=headers)
        print(attachmentsResponse.json()["value"][0]["name"])
        for attachment in attachmentsResponse.json()["value"]:
            vedlegg.append(attachment["name"])
            # convert base64 to pdf
            if attachment["contentType"] == "application/pdf":
                b64 = attachment["contentBytes"]
                b64_decoded = base64.b64decode(b64)
                with open(f"./vedlegg/{attachment["name"]}.pdf", "wb") as file:
                    file.write(b64_decoded)

        innholdjson["attachments"] = vedlegg
    else:
        innholdjson["attachments"] = []
    innhold.append(innholdjson)

# Skriver de behandlede epostene til en fil
with open('epostdata.json', 'w') as file:
    json.dump(innhold, file, indent=4)









