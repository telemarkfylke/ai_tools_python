# Program for å transkribere lydfiler til tekstfiler
# Skriptet bruker Nasjonalbibliotekets modell for gjenkjenning av tale
# Les mer om modellen her: https://huggingface.co/NbAiLab/nb-whisper-large
# Lydfilene må være i MP3-format og lagres i en mappe kalt: lyd
# Tekstfilene lagres i en ny mappe kalt: ferdig_tekst
# Laget av Tom Jarle Christiansen // Telemark fylkeskommune // 2024
# Lisenstype: CC BY-SA 4.0

from transformers import pipeline
import json, os
from datetime import datetime
from datetime import timedelta

# Definerer kildemappen og destinasjonsmappen
sourcedir = './lyd'
destinationdir = './ferdig_tekst'

# Looper gjennom alle filene i kildemappen
for filename in os.listdir(sourcedir):
    # Sjekker om filen er en lydfil
    if filename.endswith('.mp3'):
         # Definerer input- og output-filene
        input_file = os.path.join(sourcedir, filename)
        output_file = os.path.join(destinationdir , filename.replace('.mp3', '.srt'))
        # Last inn KI-modellen fra Huggingface (Kjøres lokalt på egen maskin)
        print("Nå skal vi gnage litt på: ", input_file)
        asr = pipeline("automatic-speech-recognition", "NbAiLab/nb-whisper-medium", device='cpu')

        # Transkriberer lydfilen til tekst i JSON-format
        print(f'Transkriberer {input_file} til {output_file} - Vær tålmodig, dette kan ta litt tid')
        json_tekst = asr(input_file, chunk_length_s=28, return_timestamps=True, generate_kwargs={'num_beams': 5, 'task': 'transcribe', 'language': 'no'})

        # Laster inn JSON-dataen
        data = json_tekst
        # Gjør klar til å lagre dataen som SRT-fil
        srt_data = []

        # Looper over JSON-rådataen og formaterer den til SRT-format
        for i, item in enumerate(data["chunks"], start=1):
            # Konverterer timestampene til datetime-objekter
            start_time = datetime.fromtimestamp(item['timestamp'][0]) - timedelta(hours=1)
            if item['timestamp'][1] is not None:
                end_time = datetime.fromtimestamp(item['timestamp'][1]) - timedelta(hours=1)
            else:
                end_time = datetime.fromtimestamp(item['timestamp'][0]) - timedelta(hours=1)

            # Formaterer timestampene til SRT-format
            start_time_str = start_time.strftime('%H:%M:%S,%f')[:-3]
            end_time_str = end_time.strftime('%H:%M:%S,%f')[:-3]

            # Lager SRT-strengen og legger den til i listen
            srt_string = f"{i}\n{start_time_str} --> {end_time_str}\n{item['text']}\n"
            srt_data.append(srt_string)

            # Skriver til fil
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(srt_data))
            with open('raw.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

        print(f'Transkripsjonen er lagret i {output_file} hilsen Tom Jarle')

