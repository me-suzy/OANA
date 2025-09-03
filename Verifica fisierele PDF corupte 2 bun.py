import os
import shutil
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

# Directorul unde se află fișierele PDF
directory = r"g:\1"
# Subfolder pentru fișierele corupte
output_folder = os.path.join(directory, "Output")
# Lista fișierelor PDF corupte sau care nu se deschid
corrupted_files = []
# Variabilă pentru a ține evidența ultimului fișier parcurs
last_processed_file = None
# Contor pentru toate fișierele PDF procesate
total_files_processed = 0

# Creează folderul Output dacă nu există
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    # Parcurge fiecare director și subfolder în mod recursiv
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".pdf"):
                total_files_processed += 1
                # Calea completă a fișierului PDF
                file_path = os.path.join(root, filename)
                # Salvează ultimul fișier parcurs
                last_processed_file = file_path
                # Afișează în timp real fișierul care este parcurs
                print(f"Procesând fișierul: {file_path}")
                try:
                    # Încearcă să deschizi fișierul PDF
                    reader = PdfReader(file_path)
                    # Verifică dacă documentul are pagini
                    if len(reader.pages) == 0:
                        corrupted_files.append(file_path)
                except (PdfReadError, ValueError, FileNotFoundError, PermissionError):
                    # Dacă apare o eroare la deschiderea fișierului PDF, adaugă-l în lista fișierelor corupte
                    corrupted_files.append(file_path)
except Exception as e:
    # În cazul unei excepții, oprește scriptul și afișează mesajul și informațiile dorite
    print(f"\nScriptul a fost oprit din cauza unei excepții: {e}")
    print(f"Ultimul fișier parcurs: {last_processed_file}")
else:
    # Dacă nu a fost oprită de o excepție, afișează fișierele corupte la final
    if corrupted_files:
        print("\nUrmătoarele fișiere PDF sunt corupte sau nu se pot deschide:")
        for file_path in corrupted_files:
            print(file_path)
            # Mută fișierul corupt în folderul Output
            try:
                shutil.move(file_path, os.path.join(output_folder, os.path.basename(file_path)))
                print(f"Fișierul {file_path} a fost mutat în folderul Output.")
            except Exception as move_error:
                print(f"Nu s-a putut muta fișierul {file_path}. Eroare: {move_error}")
    else:
        print("\nToate fișierele PDF din directorul specificat și subfoldere s-au deschis fără probleme.")

print(f"\nTotal fișiere PDF procesate: {total_files_processed}")
print(f"Total fișiere PDF corupte sau care nu se pot deschide: {len(corrupted_files)}")
print(f"Fișierele corupte au fost mutate în: {output_folder}")