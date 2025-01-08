# labs_sentralbordet
Et labseksperiment for å se på automagisk kategorisering og videresending av eposter

## Innhold
- [01-Basiseksempler](./01-Basiseksempler/)
- [02-Datauttrekk](./02-Datauttrekk/) (under utvikling) 
- [03-Klassifisering](./03-Klassifisering/) (under utvikling)
...
...

## Bakgrunn
Dette er et labseksperiment for å se på automagisk kategorisering/klassifisering og videresending av eposter. Vi har en felles epostkonto som mottar eposter fra ulike kilder. Vi ønsker å kategorisere disse epostene og videresende de til ulike mottakere basert på innholdet i epostene. Vi ønsker å gjøre dette på en enkel og skalerbar måte.

## 01-Basiseksempler
Dette er en mappe som inneholder noen basiseksempler med ulike funksjoner som:
    - Hente ut eposter med vedlegg fra en epostkonto
    - Strukturere data fra epostene og lagre disse i en JSON-objekter
    - Hente ut vedlegg fra epostene og lagre disse i en mappe
    - Lesing av pdf-filer og chatte med disse
    - Klassifisering av tekst

## 02-Datauttrekk
Denne mappen inneholder skript for å hente ut data fra eposter og lagre disse i en database. Dette er under utvikling.

## 03-Metadata
Denne mappen inneholder skript for å hente ut metadata fra eposter og vedlegg. Dette er under utvikling.

## 04-RAG
Mappe med ulike varianter av RAG-systemer for å bruke LLM'er mot definerte datakilder.

## 05-Transkribering
Mappe med skript for å transkribere lydfiler til tekst ved hjelp av nasjonalbibliotekets modell.