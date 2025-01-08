import os

# Definerer kildemappen og destinasjonsmappen
sourcedir = './ferdig_tekst'
destinationdir = './tekst_til_oppsummering'
oppsummering = ""


# Looper gjennom alle filene i kildemappen
for filename in os.listdir(sourcedir):
    print(filename)
    if filename.endswith('.srt'):
        input_file = os.path.join(sourcedir, filename)
        # Setter sammen en oppsummering av alle tekstfilene
        with open(input_file, 'r', encoding='utf-8') as f:
            # Leser inn en og en linje og sjekker om første tegn er " "
            # Hvis det er det, så legger vi til linjen i oppsummeringen
            for line in f:
                if line[0] == " ":
                    oppsummering += line
        print(f'Oppsummering av {input_file} lagret i oppsummering.txt')
        # Skriver oppsummeringen til en fil
        with open(os.path.join(destinationdir, 'oppsummering.txt'), 'w', encoding='utf-8') as f:
            f.write(oppsummering)