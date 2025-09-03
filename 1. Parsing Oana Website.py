import os
import re
import regex

def read_text_from_file(file_path):
    """
    Aceasta functie returneaza continutul unui fisier.
    file_path: calea catre fisierul din care vrei sa citesti
    """
    with open(file_path, encoding='utf8') as f:
        text = f.read()
        return text

def write_to_file(text, file_path, encoding='utf8'):
    """
    Aceasta functie scrie un text intr-un fisier.
    text: textul pe care vrei sa il scrii
    file_path: calea catre fisierul in care vrei sa scrii
    """
    with open(file_path, 'wb') as f:
        f.write(text.encode('utf-8', 'ignore'))

# Adăugați funcția pentru citirea fișierelor cu mai multe codificări
def read_file_with_multiple_encodings(file_path, encodings=('utf-8', 'ISO-8859-1', 'windows-1252')):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Failed to decode {file_path} with encodings {encodings}")

# Adauga <p> in fata fiecarei linii goale si </p> la sfarsitul ei
def add_paragraph_tags(match):
    return f"<p>{match.group(0).strip()}</p>"

def process_file(file_path):
    try:
        content = read_file_with_multiple_encodings(file_path)
    except ValueError as e:
        print(e)
        return

    # Regex pentru a găsi liniile cu minim 5 cuvinte
    regex_pattern = r'^(?:\s*\b\w+\b\s*){5,}$'

    # Aplică regex-ul pe fiecare linie și înlocuiește conform condiției
    modified_content = '\n'.join([re.sub(regex_pattern, add_paragraph_tags, line) for line in content.split('\n')])

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

folder_path = r"c:\\Folder-Oana\\"

# Iterează prin toate fișierele HTML din folder
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)
        process_file(file_path)

print("Procesul de adăugare a tag-urilor <p> a fost finalizat.")

###########################################

def fix_meta_description(html_content):
    # Pune tot continutul tagului pe o singura linie
    pattern = r'<meta name="description" content="(.*?)\s*\n(.*?)>'
    replacement = r'<meta name="description" content="\1\2>'

    # Use re.sub() to fix the meta description tags
    html_content = re.sub(pattern, replacement, html_content)

    # AICI REGEX-URI
    html_content = html_content.replace('«', '').replace('»', '')

    return html_content

# Functie pentru eliminarea tag-urilor de redirectare mobile
def remove_mobile_redirect_tags(html_content):
    # Regex-uri pentru tag-urile pe care dorim să le eliminăm
    mobile_redirect_tags = [
        r'<meta name="xhtml" http-equiv="mobile-agent" content="format=xhtml; url=.*?" />',
        r'<meta name="html5" http-equiv="mobile-agent" content="format=html5; url=.*?" />',
        r'if \(/Mobile/i\.test\(navigator\.userAgent\)\) {[\s\S]*?window\.location\.href = "[\s\S]*?\/";',
    ]

    # Elimină tag-urile mobile redirect din conținutul HTML
    for tag_pattern in mobile_redirect_tags:
        html_content = re.sub(tag_pattern, '', html_content)

    return html_content

# Iterează prin toate fișierele HTML din folder
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)

        # Utilizează noua funcție pentru a citi conținutul fișierului HTML
        try:
            html_content = read_file_with_multiple_encodings(file_path)
        except ValueError as e:
            print(e)
            continue

        # Fixează tag-urile meta description
        html_content = fix_meta_description(html_content)

        # Initialize variables
        canonical_link = None

        # Cauta tagul specific pentru link-ul canonical
        for tag_pattern in [
            r'(<meta name="xhtml" http-equiv="mobile-agent" content="format=xhtml; url=(.*?)" />)',
            r'(<meta name="html5" http-equiv="mobile-agent" content="format=html5; url=(.*?)" />)',
            r'(if \(/Mobile/i\.test\(navigator\.userAgent\)\) {[\s\S]*?window\.location\.href = "(.*?)" \/;)',
        ]:
            tag_match = re.search(tag_pattern, html_content)
            if tag_match:
                canonical_link = tag_match.group(2) or tag_match.group(3)
                break





    # Daca am gasit un link, adauga tagul canonical
    if canonical_link:
        canonical_tag = f'<link rel="canonical" href="{canonical_link}">'

        # Verifică dacă tagul canonical există deja în conținut
        if '<link rel="canonical"' in html_content:
            # Dacă există, înlocuiește toate aparițiile cu noul tag
            html_content = re.sub(r'<link rel="canonical" href=".*?">', canonical_tag, html_content)
        else:
            # Dacă nu există, adaugă noul tag la sfârșitul conținutului
            html_content += f'\n{canonical_tag}'

    # Elimina tagurile de redirectare mobile
    html_content = remove_mobile_redirect_tags(html_content)

    # Adaugarea stilului pentru "Source:"
    html_content += f'\n<p class="pl-3 pt-3">* Source: <a href="{canonical_link}" target="_blank">{canonical_link}</a></p>'

    # Rescrie fișierul cu conținutul actualizat
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(html_content)

    print("Procesul a fost finalizat.")





# HTML tags to translate
tags_to_translate = [
    r'<title>(.*?)<\/title>',
    r'<meta name="description" content="([\s\S]*?)>',
    r'<link rel="canonical" href="(.*?)>',  # sau asta:  <link rel="canonical"[^>]*href="([^"]*)"[^>]*>
    r'<div class="col-12" style="font-weight:300" itemprop="description">([\s\S]*?)<div class="col-md-5',
    r'<p>(.*?)<\/p>',
    r'<h4 class="sc-jMKfon fhunKk">(.*?)<\/h4>',
    r'<h2">(.*?)<\/h2>'
]

# Initialize a regex pattern for the tags to translate
pattern = '|'.join(tags_to_translate)
html_pattern = rf'({pattern})'

# Iterate over all HTML files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith((".html", ".htm")):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Find all matches of specified HTML tags and their content
        matches = re.findall(html_pattern, html_content, re.DOTALL)

        # Write tags and content to a new file without translation with .html extension
        new_filename = f"{filename.split('.')[0]}_tags_content.html"
        extracted_folder_path = os.path.join(folder_path, 'extracted')
        if not os.path.exists(extracted_folder_path):
            os.mkdir(extracted_folder_path)
        with open(os.path.join(extracted_folder_path, new_filename), 'w', encoding='utf-8') as file:
            for match in matches:
                file.write(f"{match[0]}{match[1]}\n")

        # Perform Find/Replace to remove any remaining HTML tags
        with open(os.path.join(extracted_folder_path, new_filename), 'r', encoding='utf-8') as file:
            extracted_content = file.read()

        # Remove any empty paragraph tags
        extracted_content = re.sub(r'<p></p>', '', extracted_content, flags=re.MULTILINE)
        extracted_content = re.sub(r'<p>\s</p>', '', extracted_content, flags=re.MULTILINE)

        # Merge the tag and content into a single line
        extracted_content = re.sub(r'(\s+)(</?\w+[^>]*>)', r'\1\2', extracted_content, flags=re.DOTALL)
        extracted_content = re.sub(r'(</title>).*?(?=\n|$)', r'\1', extracted_content, flags=re.DOTALL) # sterge totul dupa </title>
        extracted_content = re.sub(r'<div.*?">|<img.*?>|<h4 class.*?h4|<span.*?>|</span>|</div>|<a href=.*?</a>', r'', extracted_content, flags=re.DOTALL)
        extracted_content = re.sub(r'^>\s*$', '', extracted_content, flags=re.MULTILINE)
        extracted_content = re.sub(r'^<p></p>\s*$', '', extracted_content, flags=re.MULTILINE)
        extracted_content = re.sub(r'(</p>)(<h2>)', lambda m: m.group(1) + '\n' + m.group(2), extracted_content, flags=re.MULTILINE)
        extracted_content = re.sub(r'(</h2>)(<p>)', lambda m: m.group(1) + '\n' + m.group(2), extracted_content, flags=re.MULTILINE)

        extracted_content = re.sub(r'([^<]*)(</p><p>)', r'\1</p>', extracted_content, flags=re.MULTILINE)

        # sterge toate instantele <title> (toate liniile care contin <title> , dar lasa prima instanta
        def remove_last_title_tags(text):
            # Find all instances of the `<title>` tag
            title_tags = regex.findall(r"(?<=^|\n)<title>.*?</title>", text, flags=regex.DOTALL)

            # Replace the last instance of each `<title>` tag with an empty string
            for i in range(len(title_tags) - 1, -1, -1):
                if i == 0:
                    continue
                text = text.replace(title_tags[i], "")

            return text

        extracted_content = remove_last_title_tags(extracted_content)

        # Extragerea valorii href din tag-ul canonical
        canonical_link_match = re.search(r'<link rel="canonical" href="(.*?)>', extracted_content)
        if canonical_link_match:
            canonical_link = canonical_link_match.group(1)
            # Transformarea linkului canonical într-un link clicabil și adăugarea stilului pentru "Source:"
            extracted_content += f'\n<p class="pl-3 pt-3">* Source: <a href="{canonical_link}" target="_blank">{canonical_link}</a></p>'
        else:
            # Dacă nu găsim un tag canonical, adăugăm textul alternativ cu același stil
            extracted_content += '\n<p class="pl-3 pt-3">Source: Canonical link not found</p>'

        # Save the replaced content to the same file
        with open(os.path.join(extracted_folder_path, new_filename), 'w', encoding='utf-8') as file:
            file.write(extracted_content)

        # Print the file name
        print(f"Tagurile specifice din fisierul '{filename}' au fost extrase și salvate în '{new_filename}'")
