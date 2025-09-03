import os
import re
import shutil

folder_path = "c:\\Folder-Oana\\extracted\\"
subfolder_path = "c:\\Folder-Oana\\extracted\\1\\"

# Parcurge fișierele din folderul principal
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Verifică dacă este un fișier și nu un director
    if os.path.isfile(file_path):
        # Citirea conținutului fișierului
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Identificarea conținutului specific
        match = re.search(r'<link rel="canonical" href="(.*?)" />', content)
        if match:
            canonical_link = match.group(0)  # Obține întregul tag canonical

            # Construiește calea către fișierul corespunzător din subfolder
            subfolder_file_path = os.path.join(subfolder_path, filename)

            # Deschide fișierul din subfolder pentru scriere
            with open(subfolder_file_path, 'r+', encoding='utf-8') as subfolder_file:
                subfolder_content = subfolder_file.read()

                # Găsește tagul canonical în fișierul din subfolder și înlocuiește-l cu cel din fișierul principal
                subfolder_content = re.sub(r'<link rel="canonical" href=".*?" />', canonical_link, subfolder_content)

                # Întoarce cursorul la începutul fișierului și rescrie conținutul actualizat
                subfolder_file.seek(0)
                subfolder_file.write(subfolder_content)
                subfolder_file.truncate()

            print(f"Tagul canonical din {filename} a fost mutat în {subfolder_file_path}")
