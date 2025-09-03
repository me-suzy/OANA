import os
import re

def remove_duplicate_lines_from_files(folder_path):
    # Iterează prin toate fișierele HTML și HTM din folder
    for filename in os.listdir(folder_path):
        if filename.endswith((".html", ".htm")):
            file_path = os.path.join(folder_path, filename)
            remove_duplicate_lines(file_path)
            print(f"Liniile duplicate din '{filename}' au fost eliminate.")
            remove_ellipsis(file_path)
            print(f"&hellip; eliminat din '{filename}'.")

def remove_duplicate_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Utilizează un set pentru a ține evidența liniilor unice
    unique_lines = set()

    # Construiește o listă cu liniile unice
    unique_lines_list = []
    for line in lines:
        # Elimină caracterele de la sfârșitul liniei (spații, tab-uri, newline)
        cleaned_line = line.strip()

        # Adaugă linia la set doar dacă nu există deja
        if cleaned_line not in unique_lines:
            unique_lines.add(cleaned_line)
            unique_lines_list.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines_list)

def remove_ellipsis(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Utilizează re.sub pentru a înlocui toate aparițiile "&hellip;" cu un șir gol
    updated_content = re.sub(r'&hellip;', '', content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

# Exemplu de utilizare
folder_path = 'c:\\Folder-Oana\\extracted\\translated\\'
remove_duplicate_lines_from_files(folder_path)
print("Liniile duplicate și &hellip; din toate fișierele HTML și HTM au fost eliminate.")
