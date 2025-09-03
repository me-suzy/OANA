import os
import re

def modificare_fisiere_html(director):
    # Parcurgem toate fișierele din directorul specificat
    for nume_fisier in os.listdir(director):
        cale_fisier = os.path.join(director, nume_fisier)

        # Verificăm dacă fișierul este HTML
        if os.path.isfile(cale_fisier) and cale_fisier.endswith(".html"):
            with open(cale_fisier, 'r', encoding='utf-8') as fisier:
                continut = fisier.read()

                # Regex 1: Schimba tagul <meta property
                continut = re.sub(r'<meta name="description" content="([\s\S]*?)">', lambda match: '<meta name="description" content="{}">'.format(match.group(1).replace("\n", " ")), continut)

                # Regex 2: Schimba tagul <title>
                continut = re.sub(r'<title>([\s\S]*?)</title>', lambda match: '<title>{}</title>'.format(match.group(1).replace("\n", " ")), continut)

                # Regex 3: Schimba tagul <p>
                continut = re.sub(r'<p>([\s\S]*?)</p>', lambda match: '<p>{}</p>'.format(match.group(1).replace("\n", " ")), continut)

                # Elimină spațiile multiple dintre cuvinte în interiorul tagurilor
                continut = re.sub(r'(<meta name="description" content=".*?">)|(<title>.*?</title>)|(<p>.*?</p>)', lambda match: ' '.join(match.group(0).split()), continut)

                # Salvăm modificările înapoi în fișier
                with open(cale_fisier, 'w', encoding='utf-8') as fisier_modificat:
                    fisier_modificat.write(continut)

                print(f"Fisierul '{nume_fisier}' a fost modificat conform regex-urilor.")

    # Afișăm mesajul final când operația este completă
    print("Modificarea fișierelor HTML a fost finalizată.")

# Apelăm funcția cu directorul specificat
director_cautare = r'c:\Folder-Oana\extracted\translated'
modificare_fisiere_html(director_cautare)
