import os
import re
from bs4 import BeautifulSoup
import unicodedata

# Directorul cu fișierele HTML și HTM
folder_path = "c:\\Folder-Oana\\extracted\\salvate\\"

# Funcție pentru înlocuirea </[> cu </p>
def replace_tags(html_content):
    return re.sub(r'</\[>', '</p>', html_content)

# Funcție pentru adăugarea newline înainte de <link rel="canonical" href=".*"/>
def add_newline_before_canonical_tag(html_content):
    return re.sub(r'(<link rel="canonical" href=".*"/>)', r'\n\1', html_content)

# Funcție pentru extragerea primelor 80 de cuvinte din tagurile <p>
def extract_first_80_words(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    p_tags = soup.find_all('p')
    p_text = ' '.join([p.get_text() for p in p_tags])
    words = p_text.split()[:80]
    return ' '.join(words)

# Funcție pentru eliminarea diacriticelor din meta descriere
def remove_diacritics_from_meta_description(meta_description):
    return ''.join((c for c in unicodedata.normalize('NFD', meta_description) if unicodedata.category(c) != 'Mn'))

# Parcurgem toate fișierele din directorul specificat, fără subfoldere
for file_name in os.listdir(folder_path):
    if file_name.lower().endswith((".html", ".htm")):
        file_path = os.path.join(folder_path, file_name)

        print(f"Procesare fișier: {file_path}")  # Afișăm fișierul procesat

        # Citim conținutul fișierului
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Extragem conținutul din tagul <meta name="description" content=".*">
        description_tag = re.search(r'<meta name="description" content="(.*?)">', html_content)

        if description_tag:
            # Verificăm dacă există cel puțin 80 de cuvinte în tagurile <p>
            if len(html_content.split()) >= 80:
                # Ștergem conținutul existent din tagul <meta name="description" content="">
                html_content = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="">', html_content)

                # Aplicăm eliminarea diacriticelor din meta descriere
                meta_description = description_tag.group(1)
                meta_description_no_diacritics = remove_diacritics_from_meta_description(meta_description)

                # Înlocuim vechiul conținut al tagului <meta name="description" content=""> cu cel nou
                html_content = re.sub(r'<meta name="description" content="">', f'<meta name="description" content="{meta_description_no_diacritics}">', html_content)

                # Aplicăm adăugarea newline înainte de <link rel="canonical" href=".*"/>
                html_content = add_newline_before_canonical_tag(html_content)

                # Aplicăm înlocuirea </[> cu </p>
                html_content = replace_tags(html_content)

                # Extragem primele 80 de cuvinte din tagurile <p> și le adăugăm la descriere
                description = extract_first_80_words(html_content)

                # Înlocuim vechiul conținut al tagului <meta name="description" content=""> cu cel nou
                html_content = re.sub(r'<meta name="description" content="">', f'<meta name="description" content="{description}">', html_content)

                # Scriem fișierul HTML actualizat
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(html_content)
            else:
                # Dacă nu există cel puțin 80 de cuvinte, ștergem fișierul
                os.remove(file_path)
                print(f"Fișierul {file_name} a fost șters deoarece nu conținea cel puțin 80 de cuvinte în tagurile <p>.")

print("Actualizare și ștergere efectuate cu succes în toate fișierele HTML și HTM din folderul specificat!")
