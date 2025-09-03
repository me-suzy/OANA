import os
import re
import textwrap
import regex as re
import regex
import time
from deep_translator import GoogleTranslator
from deep_translator.exceptions import RequestError  # Import specific exceptions
from langdetect import detect

from dotenv import load_dotenv  # Import the dotenv module


# Load environment variables from .env file
load_dotenv()

# Initialize the Deep Translator Translator
translator = GoogleTranslator(source='auto', target='ro')

# Initialize a counter for the translated files
translated_files_count = 0

import os

# Folder path containing the HTML files
folder_path = r"c:\\Folder-Oana\\extracted\\"









# Dimensiunea minimă a fișierului în kilobytes (1.3 KB)
min_file_size_kb = 1.3

# Parcurgeți toate fișierele din director
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Verificați dacă este un fișier și obțineți dimensiunea sa
    if os.path.isfile(file_path):
        file_size_kb = os.path.getsize(file_path) / 1024  # Dimensiunea fișierului în KB

        # Dacă fișierul este mai mic decât dimensiunea minimă, ștergeți-l
        if file_size_kb < min_file_size_kb:
            print(f"Șterg fișierul {filename} deoarece este mai mic decât 1.3 KB.")
            os.remove(file_path)


# Regexuri inainte de traducerea fisierului
regex = r"<p>(.{0,9})<\/p>"


def add_paragraph_tags(text):
    new_lines = []
    for line in text.split('\n'):
        stripped_line = line.strip()

        # Săriți peste linii care conțin taguri specifice
        if re.search(r'(<title>.*?</title>|<meta name="description" content=".*?"|<link rel="canonical" href=".*?"|<p class="pl-3 pt-3">.*?</a></p>)', stripped_line):
            new_line = line
        elif stripped_line and not stripped_line.startswith('<p>') and not stripped_line.endswith('</p>'):
            new_line = f'<p>{stripped_line}</p>'
        else:
            new_line = line
        new_lines.append(new_line)
    return '\n'.join(new_lines)

# Parcurgeți fiecare fișier HTML și aplicați funcția
for filename in os.listdir(folder_path):
    if filename.endswith((".html", ".htm")):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
        # Aplicați funcția de adăugare a tagurilor <p>
        updated_html_content = add_paragraph_tags(html_content)
        # Rescrieți fișierul cu conținutul actualizat
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(updated_html_content)



# Iterate through all HTML files in the folder
for filename in os.listdir(folder_path):
  if filename.endswith((".html", ".htm")):
    filepath = os.path.join(folder_path, filename)

    # Read the HTML file content with UTF-8 encoding
    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()




    # Remove escaped characters
    html_content = re.sub(r"\\\\.*$", "", html_content)

    # html_content = re.sub(r"^(?!<p>|</p>)(.*)(<\/p>)$", "<p>\1\2", html_content)
    # html_content = re.sub(r"(^(?!<p>))(.*)(</p>)", "\1\2", html_content)
    # html_content = re.sub(r"^(?!<p>)(.*)(<\/p>)$", "<p>\1\2", html_content)



    # Format paragraphs
    html_content = re.sub(r"^(.*?)$", r"<p>\1</p>", html_content, flags=re.MULTILINE)


    # Remove paragraphs with less than 10 words (multi-line)
    html_content = re.sub(r"<p>.{0,9}<\/p>", "", html_content, flags=re.MULTILINE)


    # Remove leading > from the first paragraph
    html_content = re.sub(r"^>", "", html_content)

    # Remove U+200B non-breaking space (hair space)
    html_content = re.sub(r"\x200B", "", html_content)
    html_content = re.sub(r"\u00C2", "", html_content)
    html_content = re.sub(r"\u001C", "", html_content) #  NSBN
    html_content = re.sub(r"<p>\d+</p>", "", html_content)


        # Adaugă o linie nouă după fiecare tag </p>
    html_content = re.sub(r'</p>', '</p>\n', html_content)

        # Adaugă un tag <p> la începutul liniilor care nu încep cu un tag HTML
    # html_content = re.sub(r'(^)((?!<[^>]+>).*$)', r'\1<p>\2</p>', html_content, flags=re.MULTILINE)

    # html_content = re.sub(r'^(?!.*<.*>)(.*)$', r'<p>\1</p>', html_content, flags=re.MULTILINE)

        # Convertește fiecare pereche de taguri <p> adiacente într-un singur tag <p>
    # html_content = re.sub(r'((?<=).*?</p>)(<p>(?=.*))', '\1\n\2', html_content, flags=re.MULTILINE)


    html_content = re.sub(r'^\s', '', html_content, flags=re.MULTILINE)
    # html_content = re.sub(r'</p></p>', '</p>', html_content, flags=re.MULTILINE)



    html_content = re.sub(r'<[^>]*>(?:\s*\w+\s*){1,3}\s*<\/[^>]*>', '', html_content) # sterge tagurile care contin mai putin de 4 cuvinte
    html_content = re.sub(r'<p><title>', '<title>', html_content)
    html_content = re.sub(r'<p></p>', '', html_content)
    html_content = re.sub(r'</title></p>', '</title>', html_content)
    html_content = re.sub(r'<p><meta name=', '<meta name=', html_content)
    html_content = re.sub(r'"/></p>', '"/>', html_content)
    html_content = re.sub(r'<p><p>', '<p>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'</p></p>', '</p>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^</p>$', '', html_content, flags=re.MULTILINE) #sterge orice <p> gol de la inceputul linilor
    html_content = re.sub(r'<p style=".*?">', '<p>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'<font.*?">', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'</font>', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'"\/"', '"', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'<strong>|</strong>', ' ', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'<p>\d+</p>', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'‘|’', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'”|“', '', html_content, flags=re.MULTILINE)




    # html_content = re.sub(r'^(?=(\w+\s*){5,}).*$', '<p>$0</p>', html_content, flags=re.MULTILINE)  # adauga  <p>帮助你定期反馈，同时
    # html_content = re.sub(r'(<p>.*?)(?<!</p>)$', '\1</p>', html_content, flags=re.MULTILINE)

    # Write the modified HTML file content
    # Read the HTML file content with UTF-8 encoding
    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()







# Sortează fișierele alfabetic
sorted_files = sorted(os.listdir(folder_path))

def should_translate(text, target_language):
    try:
        # Detectează limba conținutului textului
        detected_language = detect(text)
        # Verifică dacă limba detectată este aceeași cu limba țintă
        return detected_language != target_language
    except:
        # În cazul unei erori, presupune că traducerea este necesară
        return True


# HTML tags to translate
tags_to_translate = [
    r'(<title>)(.*?)(<\/title>)',
    r'(<meta name="description" content=")(.*?)(>)',
    r'(<div class="sc-jKDlA-D hSgfYV sc-glENfF hIVUeB">)(.*?)(<\/div>)',
    r'(<p>)(.*?)(<\/p>)',
    r'(<h4 class="sc-jMKfon fhunKk">)(.*?)(<\/h4>)',
    r'(<h2">)([\s\S]*?)(<\/h2>)'

    # ... alte tag-uri, structurate similar
]



def translate_in_parts(text, translator, max_length=4800, max_retries=5):
    """Traduce textul în fragmente pentru a evita limita de caractere a API-ului."""
    translated = ''
    while text:
        # Luăm un fragment de text pentru a rămâne sub limita de 5000 de caractere
        part = text[:max_length]
        text = text[max_length:]

        attempt = 0
        while attempt < max_retries:
            try:
                translated_part = translator.translate(part)
                translated += translated_part
                break  # Break the loop if translation is successful
            except RequestError:  # Use the imported exception
                attempt += 1
                time.sleep(1)  # Așteaptă un pic înainte de a reîncerca
                print(f"Reîncercarea {attempt} pentru fragmentul: {part[:30]}...")
    return translated

translated_tags_count = 0  # Inițializează contorul pentru tagurile traduse





import unidecode

def format_title_for_canonical(title):
    # Elimină tot ce este după primul semn "-" și formatează pentru tag-ul canonical
    title = re.split(r' - ', title, maxsplit=1)[0]
    title = title.lower()
    title = unidecode.unidecode(title)
    title = re.sub(r'\s+', '-', title)
    return title

def format_title_for_title_tag(title):
    # Elimină tot ce este după primul semn "-" pentru tag-ul <title>
    title = re.split(r' - ', title, maxsplit=1)[0]
    return title



for filename in sorted_files:
    if filename.endswith((".html", ".htm")):
        print(f"Procesez fișierul: {filename}")
        file_path = os.path.join(folder_path, filename)

        file_size_kb = os.path.getsize(file_path) / 1024
        if file_size_kb < min_file_size_kb:
            print(f"Șterg fișierul {filename} deoarece este mai mic decât 1.3 KB.")
            os.remove(file_path)
            continue

        with open(file_path, 'rb') as file:
            try:
                html_content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                # Încercați alte seturi de caractere, cum ar fi 'ISO-8859-1' sau 'latin-1'
                html_content = file.read().decode('ISO-8859-1')


        try:
            title_match = re.search(r'<title>(.*?)<\/title>', html_content)
            if title_match:
                title_content = title_match.group(1)
                formatted_title_for_title_tag = format_title_for_title_tag(title_content)
                formatted_title_for_canonical = format_title_for_canonical(title_content)

                # Înlocuirea sigură a tagurilor
                html_content = html_content.replace(title_match.group(0), f'<title>{formatted_title_for_title_tag}</title>')
                canonical_tag = f'<link rel="canonical" href="{formatted_title_for_canonical}.html" />'
                html_content = re.sub(r'<link rel="canonical" href=".*?" \/>', canonical_tag, html_content)
        except Exception as e:
            print(f"Eroare la procesarea fișierului {filename}: {e}")
            continue





                          # Elimină caracterele ZWSP
            html_content = remove_zwsp(html_content)


            html_content = re.sub(r'<p></p>', '', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'<p>\d+</p>', '', html_content, flags=re.MULTILINE)



            '''
            def add_paragraph_tags(text):
                return regex.sub(r'^(?=(\w+\s*){5,}).*$', '<p>$0</p>', text, flags=regex.MULTILINE)

            # Aplicați funcția la conținutul HTML
            html_content = add_paragraph_tags(html_content)
            '''




        for tag in tags_to_translate:
            matches = re.finditer(tag, html_content, re.DOTALL)

            for match in matches:
                full_match = match.group(0)
                tag_start = match.group(1)
                tag_content = match.group(2)
                tag_end = match.group(3)

                # Verifică dacă trebuie tradus
                if should_translate(tag_content, 'ro'):
                    # Procedează cu traducerea
                    translated_content = translate_in_parts(tag_content, translator)
                    translated_tag = f"{tag_start}{translated_content}{tag_end}"
                    html_content = html_content.replace(full_match, translated_tag)
                    translated_tags_count += 1




        new_filename = f"{filename.split('.')[0]}_ro.html"
        translated_folder_path = os.path.join(folder_path, 'translated')

        if not os.path.exists(translated_folder_path):
            os.mkdir(translated_folder_path)

        with open(os.path.join(translated_folder_path, new_filename), 'w', encoding='utf-8') as file:
            file.write(html_content)

        translated_files_count += 1
        print(f"Fișierul a fost tradus și salvat: {new_filename}")

print("Toate fișierele au fost traduse.")
