import os
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

# Directorul unde se află fișierele PDF
directory = "g:/ARHIVA/BCU PDF/Cucuianu, Mircea"

# Lista fișierelor PDF corupte sau care nu se deschid
corrupted_files = []

# Parcurge fiecare director și subfolder în mod recursiv
for root, _, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".pdf"):
            # Calea completă a fișierului PDF
            file_path = os.path.join(root, filename)

            try:
                # Încearcă să deschizi fișierul PDF
                reader = PdfReader(file_path)
                # Verifică dacă documentul are pagini
                if len(reader.pages) == 0:
                    corrupted_files.append(file_path)
            except (PdfReadError, ValueError, FileNotFoundError):
                # Dacă apare o eroare la deschiderea fișierului PDF, adaugă-l în lista fișierelor corupte
                corrupted_files.append(file_path)

# Afișează lista fișierelor PDF corupte sau care nu se deschid
if corrupted_files:
    print("Următoarele fișiere PDF sunt corupte sau nu se pot deschide:")
    for file_path in corrupted_files:
        print(file_path)
else:
    print("Toate fișierele PDF din directorul specificat s-au deschis fără probleme.")
