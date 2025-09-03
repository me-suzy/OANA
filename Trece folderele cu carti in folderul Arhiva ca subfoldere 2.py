import os
import shutil

folder_path = r"G:\De pus pe FTP 2"

# Parcurge fiecare fișier din director
for file_name in os.listdir(folder_path):
    if file_name.endswith(".pdf"):
        # Înlocuiește ambele variante de separatori cu unul standard, " - "
        file_name_standardized = file_name.replace(" – ", " - ").replace(" - ", " - ")

        # Verifică dacă fișierul corespunde formatului dorit
        if " - " in file_name_standardized:
            # Extrage numele de fișier până la " - "
            folder_name = file_name_standardized.split(" - ")[0].strip()

            # Calea completă pentru fișier și folder
            file_path = os.path.join(folder_path, file_name)
            folder_path_new = os.path.join(folder_path, folder_name) # Păstrează spațiile în numele folderului

            # Crează folderul dacă nu există deja
            if not os.path.exists(folder_path_new):
                os.mkdir(folder_path_new)

            # Mută fișierul în noul folder
            shutil.move(file_path, os.path.join(folder_path_new, file_name))
        else:
            # Mută fișierul în folderul principal
            try:
                print(f"Nu s-a putut crea folder pentru: {file_name}".encode('cp1252', 'replace').decode('cp1252'))
                print(f"Verificare: Separatorul ' - ' nu este prezent în numele fișierului: {file_name}".encode('cp1252', 'replace').decode('cp1252'))
            except UnicodeEncodeError:
                print("Eroare de codificare la afișarea numelui fișierului.")
            shutil.move(os.path.join(folder_path, file_name), os.path.join(folder_path, file_name))
            try:
                print(f"Fișierul {file_name} a fost mutat în folderul principal.".encode('cp1252', 'replace').decode('cp1252'))
            except UnicodeEncodeError:
                print("Eroare de codificare la afișarea numelui fișierului.")

print("Procesul a fost finalizat.")
