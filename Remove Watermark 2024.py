import os
import fitz  # PyMuPDF

def remove_watermark_from_pdf(input_pdf, output_pdf):
    # Deschide fișierul PDF de intrare
    doc = fitz.open(input_pdf)

    # Parcurge fiecare pagină
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)

        # Curăță conținutul paginii pentru a îndepărta elementele grafice
        page.clean_contents()

    # Salvează documentul PDF modificat
    doc.save(output_pdf)

    # Închide documentul PDF
    doc.close()

# Directorul unde se află fișierele PDF
directory = "D:/test"

# Parcurge fiecare fișier PDF din director
for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        # Calea completă a fișierului PDF de intrare
        input_pdf = os.path.join(directory, filename)

        # Numele de ieșire cu extensia "_removed"
        output_pdf = os.path.join(directory, filename.replace(".pdf", "_removed.pdf"))

        # Elimină watermark-ul din fișierul PDF
        remove_watermark_from_pdf(input_pdf, output_pdf)

print("Eliminarea watermark-ului a fost completată pentru toate fișierele PDF din directorul specificat.")
