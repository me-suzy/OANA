import os
import re
from collections import defaultdict

def read_file_with_fallback_encoding(file_path, encodings=['utf-8', 'iso-8859-1', 'windows-1252']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.readline().strip(), encoding
        except UnicodeDecodeError:
            continue
    return None, None

def find_max_item_id_and_duplicates(directory):
    max_id = 0
    max_id_file = ''
    id_to_files = defaultdict(list)
    files_with_errors = []

    pattern = re.compile(r'\$item_id\s*=\s*(\d+);')

    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            print(f"Parcurg fișierul: {filename}")  # Afișare în timp real

            first_line, encoding = read_file_with_fallback_encoding(file_path)
            if first_line is None:
                print(f"Nu s-a putut citi fișierul {filename} cu niciuna din codificările încercate.")
                files_with_errors.append(filename)
                continue

            match = pattern.search(first_line)
            if match:
                item_id = int(match.group(1))
                id_to_files[item_id].append(filename)
                if item_id > max_id:
                    max_id = item_id
                    max_id_file = filename
            else:
                print(f"Nu s-a găsit item_id în prima linie a fișierului {filename}")

    return max_id, max_id_file, id_to_files, files_with_errors

# Specificați calea către directorul cu fișierele HTML
directory = r'e:\Carte\BB\17 - Site Leadership\Principal\en'

max_id, max_id_file, id_to_files, files_with_errors = find_max_item_id_and_duplicates(directory)

print("\nRezultate:")
if max_id > 0:
    print(f"Cel mai mare item_id găsit este {max_id} în fișierul {max_id_file}")
else:
    print("Nu s-a găsit niciun item_id valid în fișierele HTML din director.")

print("\nNumere duplicate găsite:")
for item_id, files in id_to_files.items():
    if len(files) > 1:
        print(f"item_id {item_id} se repetă în următoarele fișiere:")
        for file in files:
            print(f"  - {file}")

print("\nStatistici:")
print(f"Număr total de fișiere HTML parcurse: {sum(len(files) for files in id_to_files.values())}")
print(f"Număr de item_id-uri unice: {len(id_to_files)}")
print(f"Număr de item_id-uri duplicate: {sum(1 for files in id_to_files.values() if len(files) > 1)}")

if files_with_errors:
    print("\nFișiere care nu au putut fi citite:")
    for file in files_with_errors:
        print(f"  - {file}")