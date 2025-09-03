import os
import re
import chardet

def read_text_from_file(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    try:
        # Încercăm să decodăm ca UTF-8, ignorând erorile
        return raw_data.decode('utf-8', errors='ignore')
    except UnicodeDecodeError:
        pass

    # Dacă UTF-8 eșuează, încercăm detectarea automată a codificării
    encoding = chardet.detect(raw_data)['encoding']
    if encoding is not None:
        try:
            return raw_data.decode(encoding, errors='ignore')
        except UnicodeDecodeError:
            pass

    raise Exception(f"Eroare: Nu s-a putut decodifica fișierul {file_path} nici cu UTF-8, nici cu codificarea detectată.")



def write_to_file(text, file_path, encoding='utf8'):
    """
    Aceasta functie scrie un text intr-un fisier.
    text: textul pe care vrei sa il scrii
    file_path: calea catre fisierul in care vrei sa scrii
    """
    with open(file_path, 'wb') as f:
        f.write(text.encode(encoding, 'ignore'))



def clean_html_files(folder_path):
    allowed_tags_patterns = [
        r'(<p class="pl-3 pt-3">.*?</p>)',
        r'(<title>.*?</title>)',
        r'(<meta name="description" content=".*?>)',
        r'(<a href="https:.*?</a>)',
        r'(<p>.*?</p>)',
        r'(<link rel="canonical" href=".*?"/>)',
        r'(<meta name="xhtml" http-equiv="mobile-agent" content="format=xhtml; url=.*?" />)',
        r'(<meta name="html5" http-equiv="mobile-agent" content="format=html5; url=.*?" />)',
        r'(if \(/Mobile/i\.test\(navigator\.userAgent\)\) {[\s\S]*?window\.location\.href = "[\s\S]*?\/";)',
    ]
    allowed_pattern = '|'.join(allowed_tags_patterns)

    # Taguri de eliminat din interiorul tagurilor <p></p>
    tags_to_remove = [
        r'<iframe.*?iframe>',
        r'<br>|<br\s*/?>',
        # Aici poți adăuga alte taguri pe care dorești să le elimini
    ]

    # Iterează prin toate fișierele din folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            print(f"UPDATE: Procesez fișierul: {filename}")

            # Citirea conținutului fișierului
            content = read_text_from_file(file_path)

            # Elimină tagurile specificate din interiorul tagurilor <p></p>
            for tag_pattern in tags_to_remove:
                content = re.sub(tag_pattern, '', content, flags=re.DOTALL)

            # Extrage conținutul care corespunde tagurilor permise
            matches = re.findall(allowed_pattern, content, re.DOTALL)
            allowed_content = [match for group in matches for match in group if match]

            # Rescrierea fișierului cu doar conținutul permis
            write_to_file('\n'.join(allowed_content), file_path)

    print("UPDATE: Curățarea fișierelor HTML a fost finalizată.")

# Calea către folderul specificat
folder_path = r"c:\Folder-Oana"

# Apelarea funcției
clean_html_files(folder_path)
