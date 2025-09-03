import os

# Calea către directorul cu fișiere HTML
directory = "c:/Folder-Oana/extracted/salvate/"

# Listă pentru a stoca numele fișierelor modificate
modified_files = []

# Parcurgeți fiecare fișier în director
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Variabile pentru a identifica tag-urile meta description
        first_meta_index = None
        second_meta_index = None

        # Găsiți indexul celor două tag-uri meta description
        for i, line in enumerate(lines):
            if '<meta name="description"' in line:
                if first_meta_index is None:
                    first_meta_index = i
                else:
                    second_meta_index = i
                    break

        # Verificăm dacă am găsit ambele tag-uri
        if first_meta_index is not None and second_meta_index is not None:
            # Înlocuiți primul tag cu al doilea
            lines[first_meta_index] = lines[second_meta_index]
            del lines[second_meta_index]

            # Rescrieți fișierul cu modificările efectuate
            with open(filepath, 'w', encoding='utf-8') as file_modified:
                file_modified.writelines(lines)

            # Adăugați fișierul la lista de fișiere modificate
            modified_files.append(filename)

# Afișați numele fișierelor modificate și numărul lor
print(f"Fișiere modificate: {modified_files}")
print(f"Număr total de fișiere modificate: {len(modified_files)}")
