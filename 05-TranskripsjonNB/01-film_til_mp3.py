# Skript for å konvertere M4V-filer til MP3-filer
# Skriptet bruker ffmpeg til å trekke ut lyden fra M4V-filene og lagre den som MP3-filer
# MP3-filene lagres i en ny mappe kalt "Lyd"
# Laget av Tom Jarle Christiansen // Telemark fylkeskommune // 2024
# Lisenstype: CC BY-SA 4.0

import ffmpeg, os

# Definerer kildemappen og destinasjonsmappen
sourcedir = './filmer'
destinationdir = './lyd'

# Looper gjennom alle filene i kildemappen
for filename in os.listdir(sourcedir):
    # Sjekker om filen er en videofil
    print("Filnavn: ", filename)
    if filename.split('.')[-1] == 'm4v':
        print(f'Filen {filename} er en videofil')
        # Define the input og output filer
        input_file = os.path.join(sourcedir, filename)
        output_file = os.path.join(destinationdir, filename.replace('.m4v', '.mp3'))
        print(input_file, output_file)
        # Bruker ffmpeg til å trekke ut lyden fra video-filen og lagrer den som MP3-fil
        ffmpeg.input(input_file).output(output_file, acodec='libmp3lame', format='mp3').run()
        print(f'Hentet ut lyd fra {input_file} og lagret i {output_file}')
