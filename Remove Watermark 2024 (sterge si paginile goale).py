import os
import fitz  # PyMuPDF

def remove_watermark_and_empty_pages(input_pdf, output_pdf):
    # Deschide fișierul PDF de intrare
    doc = fitz.open(input_pdf)

    # Creați un nou document PDF gol pentru ieșire
    output_doc = fitz.open()

    # Parcurge fiecare pagină a documentului de intrare
    for page_number in range(len(doc)):
        # Încarcă pagina curentă
        page = doc.load_page(page_number)

        # Curăță conținutul paginii pentru a îndepărta elementele grafice
        page.clean_contents()

        # Verifică dacă pagina este goală
        # Dacă pagina conține text sau elemente grafice, o adăugăm în documentul de ieșire
        if page.get_text().strip() or page.search_for_images(full=True):
            output_doc.insert_pdf(doc, from_page=page_number, to_page=page_number)

    # Salvează documentul PDF modificat în output_pdf
    output_doc.save(output_pdf)

    # Închide documentele PDF
    doc.close()
    output_doc.close()

# Directorul unde se află fișierele PDF
directory = "D:/test"

# Parcurge fiecare fișier PDF din director
for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        # Calea completă a fișierului PDF de intrare
        input_pdf = os.path.join(directory, filename)

        # Calea completă a fișierului PDF de ieșire
        output_pdf = os.path.join(directory, filename.replace(".pdf", "_removed.pdf"))

        # Elimină watermark-ul și paginile goale din fișierul PDF
        remove_watermark_and_empty_pages(input_pdf, output_pdf)

print("Eliminarea watermark-ului și paginilor goale a fost completată pentru toate fișierele PDF din directorul specificat.")
