import os
import re
from collections import defaultdict

# Calea către directorul cu fișierele HTML
directory_path = r'e:\Carte\BB\17 - Site Leadership\Principal\ro'

# Dicționare pentru a ține evidența titlurilor și descrierilor și fișierelor corespunzătoare
titles_dict = defaultdict(list)
descriptions_dict = defaultdict(list)

# Parcurgem fiecare fișier în directorul specificat
for filename in os.listdir(directory_path):
    if filename.endswith(".html"):  # Verificăm dacă fișierul este un HTML
        filepath = os.path.join(directory_path, filename)
        print(f"Procesez fișierul: {filename}")  # Afișăm fișierul curent procesat
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()

                # Căutăm titlul în conținutul fișierului
                title_match = re.search(r'<title>(.*?)</title>', content)
                if title_match:
                    title = title_match.group(1)
                    titles_dict[title].append(filename)

                # Căutăm descrierea în conținutul fișierului
                description_match = re.search(r'<meta name="description" content="(.*?)">', content)
                if description_match:
                    description = description_match.group(1)
                    descriptions_dict[description].append(filename)

        except UnicodeDecodeError:
            print(f"Nu am putut decoda fișierul {filename} folosind UTF-8, chiar și cu errors='replace'.")

# Verificăm dacă există titluri duplicate în mai multe fișiere
print("Dubluri pentru titluri:")
for title, files in titles_dict.items():
    if len(files) > 1:
        print(f"Titlul '{title}' apare în următoarele fișiere:")
        for index, file in enumerate(files, start=1):
            print(f"{index}. {file}")

print("\nDubluri pentru descrieri:")
# Verificăm dacă există descrieri duplicate în mai multe fișiere
for description, files in descriptions_dict.items():
    if len(files) > 1:
        print(f"\nDescrierea '{description}' apare în următoarele fișiere:")
        for index, file in enumerate(files, start=1):
            print(f"{index}. {file}")
