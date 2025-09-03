import os
import fnmatch

def find_replace(directory, find, replace):
    for root, dirs, files in os.walk(directory):
        for file in fnmatch.filter(files, '*.html'):
            file_path = os.path.join(root, file)
            print(f'Procesez fișierul: {file_path}')  # Afisează fiecare fișier care este procesat
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                # Elimină spațiile și newline-urile de la începutul și sfârșitul textului de căutat
                cleaned_find_text = find.strip()
                if cleaned_find_text in content:
                    # Înlocuiește textul găsit cu replace_text, care poate fi un string gol sau alt text
                    new_content = content.replace(cleaned_find_text, replace)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f'Am înlocuit textul în: {file_path}')
            except Exception as e:
                print(f'Nu am putut procesa fișierul {file_path} din cauza unei erori: {e}')

# Exemplu de text de căutat
find_text = """
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-1417683-22"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', 'UA-1417683-22');
</script>
"""

# Pentru a șterge textul, setează replace_text la un string gol
# daca vrei sa pui REPLACE cu ALT TEXT, atunci pui:  replace_text = """  """
# daca vrei sa lasi liber si sa stergi textul din FIND_Text, atunci pui:  replace_text = ""

replace_text = ""

# Setează căile către folderele specificate, inclusiv subfolderele
directories = [
    'e:\\Carte\\BB\\17 - Site Leadership\\Principal\\2024 - TRADUCERI\\FACUT 2024\\',
    'e:\\Carte\\BB\\17 - Site Leadership\\Principal 2022\\ens\\'
]

for directory in directories:
    find_replace(directory, find_text, replace_text)

print("Procesul de înlocuire a fost finalizat!")
