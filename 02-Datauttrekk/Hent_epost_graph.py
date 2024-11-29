# Dette scriptet henter e-post fra en bruker i Microsoft Graph og skriver innholdet til en fil
# For å kjøre scriptet må du ha en token.txt fil med et gyldig token for Microsoft Graph
# Scriptet henter de 10 nyeste e-postene fra brukeren og skriver innholdet til en fil
# HTML-innholdet blir parsert med BeautifulSoup før det skrives til fil
# Vedlegg blir lagret i en mappen kalt vedlegg

import requests
import json
from bs4 import BeautifulSoup
import pprint as pp
import base64
import os
from dotenv import load_dotenv

# Laster miljøvariabler fra .env
load_dotenv()

# Globale variabler
postboks = os.getenv("POSTBOKS")
token = os.getenv("TOKEN")
innhold = []
filbane = './uttrekk'
i = 1

# Henter e-post fra brukeren
headers = {
    'Authorization': 'Bearer ' + token
}

params = {
    'top': 200,
    # '$select': 'importance, subject, body, toRecipients, from, hasAttachments, receivedDateTime',
    '$orderby': 'receivedDateTime desc'
}

response = requests.get(f'https://graph.microsoft.com/v1.0/users/{postboks}/messages/', headers=headers, params=params)
# print(response.json())

# For hver epost hent ut innhold. Body må parses med beautifulsoup for å gjøre den lesbar for mennesker.
for value in response.json()['value']:
    # Create subfolder for each email
    if not os.path.exists("./uttrekk"):
        os.mkdir("./uttrekk")
    foldername = 'epost-' + str(i)
    filbane = './uttrekk/' + foldername
    os.mkdir(filbane)

    # Write email content to file
    importance = value['importance']
    subject = value['subject']
    body = value['body']['content']
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
        # print(message_id)
        vedlegg = []
        attachmentsResponse = requests.get(f'https://graph.microsoft.com/v1.0/users/{postboks}/messages/{message_id}/attachments/', headers=headers)
        print(attachmentsResponse.json()["value"][0]["name"])
        for attachment in attachmentsResponse.json()["value"]:
            vedlegg.append(attachment["name"])
            # convert base64 to pdf
            if attachment["contentType"] == "application/pdf" or attachment["contentType"] == "image/png" or attachment["contentType"] == "application/msword":
                b64 = attachment["contentBytes"]
                b64_decoded = base64.b64decode(b64)
                with open(f"{filbane}/{attachment["name"]}", "wb") as file:
                    file.write(b64_decoded)
        innholdjson["attachments"] = vedlegg
    else:
        innholdjson["attachments"] = []
    innhold.append(innholdjson)

    # Skriver de behandlede epostene til en fil
    with open(f'{filbane}/epostdata.json', 'w') as file:
        json.dump(innhold, file, ensure_ascii=False ,indent=4)
    i += 1
    innhold = []
    print("Ferdig med epost " + str(i))









