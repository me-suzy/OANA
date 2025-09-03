import os
import re
import regex
from unidecode import unidecode


# Folder path containing the HTML files
folder_path = r"c:\Folder-Oana\extracted\translated"

####################################################################################

# Funcția pentru eliminarea tagurilor <title> cu conținut pe două linii
def remove_multiline_title_tags(html_content):
    # Expresia regulată pentru a găsi tagurile <title> cu conținut pe două linii
    pattern = r'<title>[\s\S]*?</title>'

    # Înlocuiește tagurile <title> care au conținut pe două linii cu un șir gol
    cleaned_html = re.sub(pattern, '', html_content)

    return cleaned_html

# Funcția pentru efectuarea înlocuirilor suplimentare cu expresii regulate
def apply_additional_regex(html_content):
    # Eliminarea caracterelor speciale
    html_content = re.sub(r'\[|\]|【|】', '', html_content)
    # Înlocuirea caracterului chinezesc „” cu ghilimele obișnuite
    html_content = re.sub(r'”>', '">', html_content)
    # Eliminarea ghilimelelor chinezești „”
    html_content = re.sub(r'„|”', '', html_content)
    # Eliminarea conținutului din tagurile <script>
    html_content = re.sub(r'<script>[\s\S]*?</script>', '', html_content)
        # Apply various replacements
    html_content = re.sub(r'\[|\]|【|】', '', html_content)
    html_content = re.sub(r'”>', '">', html_content)
    html_content = re.sub(r'„|”', '', html_content)
    html_content = re.sub(r'<script>[\s\S]*?</script>', '', html_content)
    html_content = re.sub(r'<title>.*?\s*\n.*?</title>', '', html_content)
    html_content = re.sub(r'^\s*', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'<li>|</li>|<strong>|</strong>', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'<p style=.*?>', '<p>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^<p>$', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^<p></p>$', '', html_content, flags=re.MULTILINE)

    return html_content

# Iterați prin toate fișierele HTML din directorul specificat
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)

        # Citiți conținutul fișierului HTML
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Aplicați funcția pentru eliminarea tagurilor <title> cu conținut pe două linii
        cleaned_html = remove_multiline_title_tags(html_content)

        # Aplicați funcția pentru efectuarea înlocuirilor suplimentare cu expresii regulate
        cleaned_html = apply_additional_regex(cleaned_html)

        # Rescrieți fișierul cu conținutul curățat
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_html)

print("Procesul de eliminare a tagurilor <title> cu conținut pe două linii și aplicarea înlocuirilor suplimentare a fost finalizat.")



#########################################################################################################
# Pune "> care inchide toate tagurile <meta name="description" content="  care nu au la final ">

def fix_meta_description(html_content):
    # Regex pattern to find meta tags with name="description" that don't end with ">
    pattern = r'<meta name="description" content="([^"]*?)(?<!">)$'

    # Function to replace the matched tags with the fixed ones
    def replace_tags(match):
        return f'<meta name="description" content="{match.group(1)}">'

    # Use re.sub() to fix the meta description tags
    html_content = re.sub(pattern, replace_tags, html_content, flags=re.MULTILINE)

    return html_content

# Iterate through all HTML files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)

        # Read the HTML file content
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Fix the meta description tags
        html_content = fix_meta_description(html_content)

        # Rescrieți fișierul cu conținutul actualizat
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

print("Procesul a fost finalizat.")
#########################################################################################################




def format_canonical_text(text):
    # Convertiți textul la forma sa ASCII prin eliminarea diacriticelor
    text = unidecode(text)
    # Eliminați caracterele speciale și înlocuiți spațiile cu "-"
    formatted_text = re.sub(r"[^a-zA-Z0-9\s]", " ", text).strip().replace(" ", "-")
    formatted_text = re.sub(r"-+", "-", formatted_text)  # Eliminați spațiile multiple
    return formatted_text.lower()  # Convertește la litere mici

def adjust_meta_description_tags(html_content):
    # Regex pentru a identifica și elimina ghilimelele din atributul 'content'
    remove_quotes_pattern = regex.compile(r'(<meta name="description" content=")(.*?)(">)', regex.DOTALL)
    add_quotes_pattern = regex.compile(r'(<meta name="description" content="[^">]+)(>)')

    def replace_quotes(match):
        # Eliminarea ghilimelelor din conținutul atributului content
        content_without_quotes = match.group(2).replace('"', '')
        return match.group(1) + content_without_quotes + match.group(3)

    def add_missing_quote(match):
        # Adăugarea ghilimelei lipsă înainte de '>'
        return match.group(1) + '"' + match.group(2)

    # Înlocuirea ghilimelelor în toate tagurile meta potrivite și adăugarea ghilimelei lipsă dacă este cazul
    html_content = remove_quotes_pattern.sub(replace_quotes, html_content)
    html_content = add_quotes_pattern.sub(add_missing_quote, html_content)

    return html_content

# Iterate through all HTML files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)

        # Read the HTML file content
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()



        # Remove double quotes from meta description tags
        html_content = adjust_meta_description_tags(html_content)

        # Verificați dacă fișierul conține deja un tag <title> și un tag <link rel="canonical>
        title_exists = bool(re.search(r"<title>.*?</title>", html_content))
        canonical_exists = bool(re.search(r'<link rel="canonical" href=".*?" />', html_content))

        if not title_exists and not canonical_exists:
            # Cazul 1: Nu este nici linie cu tagul <title> nici linie cu tagul <canonical>
            # Extrageți conținutul din tagul <meta name="description">
            match = re.search(r'<meta name="description" content="([^"]+)"\s*>|<meta name="description" content="(.*?)">', html_content)
            if match:
                description_content = match.group(1) or match.group(2)
                # Luați primele 13 cuvinte din descriere
                description_words = description_content.split()[:13]
                # Creează tagul <title> cu primele 13 cuvinte din descriere
                title_text = " ".join(description_words)
                title_text = unidecode(title_text)

                title_tag = f'<title>{title_text}</title>'
                # Adaugă tagul <title> la începutul fișierului
                html_content = f"{title_tag}\n{html_content}"
                print(f"Cazul 1: Adăugat tagul <title> în fișierul: {filename}")

        # Verificați din nou dacă fișierul conține tagul <title> și tagul <link rel="canonical>
        title_exists = bool(re.search(r"<title>.*?</title>", html_content))
        canonical_exists = bool(re.search(r'<link rel="canonical" href=".*?" />', html_content))

        if canonical_exists and not title_exists:
            # Cazul 3: Există tagul <canonical> dar nu există tagul <title>
            # Ștergeți linia cu tagul <canonical>
            html_content = re.sub(r'<link rel="canonical" href=".*?" />', '', html_content)
            # Extrageți conținutul din tagul <meta name="description">
            match = re.search(r'<meta name="description" content="([^"]+)"\s*>|<meta name="description" content="(.*?)">', html_content)
            if match:
                description_content = match.group(1) or match.group(2)
                # Luați primele 13 cuvinte din descriere
                description_words = description_content.split()[:13]
                # Creează tagul <title> cu primele 13 cuvinte din descriere
                title_text = " ".join(description_words)
                title_text = unidecode(title_text)

                title_tag = f'<title>{title_text}</title>'
                # Adaugă tagul <title> la începutul fișierului
                html_content = f"{title_tag}\n{html_content}"
                print(f"Cazul 3: Șters tagul <canonical> și adăugat tagul <title> în fișierul: {filename}")

        # Verificați dacă fișierul conține tagul <title>
        title_exists = bool(re.search(r"<title>.*?</title>", html_content))

        # Verificați dacă fișierul conține tagul <link rel="canonical">
        canonical_exists = bool(re.search(r'<link rel="canonical" href=".*?" />', html_content))

        if not canonical_exists and title_exists:
            # Cazul 2: Există tagul <title> dar nu există tagul <canonical>
            # Extrageți conținutul din tagul <title>
            title_match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
            if title_match:
                title_text = title_match.group(1)
                # Construiți valoarea atributului href cu "-" între cuvinte și adăugați ".html"
                canonical_href = format_canonical_text(title_text) + ".html"
                canonical_href = unidecode(canonical_href)  # Conversie fără diacritice
                canonical_href = f'<link rel="canonical" href="{canonical_href}" />'
                # Găsiți linia cu tagul <title>
                title_line_match = re.search(r'<title>.*?</title>', html_content)
                if title_line_match:
                    title_line = title_line_match.group(0)
                    # Adăugați tagul <link rel="canonical"> după linia cu tagul <title>
                    html_content = html_content.replace(title_line, f"{title_line}\n{canonical_href}")
                    print(f"Cazul 2: Adăugat tagul <canonical> după tagul <title> în fișierul: {filename}")

        # Rescrieți fișierul cu modificările
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        if title_exists and canonical_exists:
            # Cazul 4: Nu s-a adăugat niciun tag nou
            print(f"Cazul 4: Nu s-a adăugat niciun tag nou în fișierul: {filename}")

print("Procesul a fost finalizat.")
