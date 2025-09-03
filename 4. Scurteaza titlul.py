import os
import re

folder_path = r'c:\Folder-Oana\extracted\translated'

def limit_title_words(html_content, max_words=12):
    # Regex pentru a găsi tagul <title> și a captura conținutul său
    title_pattern = re.compile(r'<title>(.*?)</title>', re.DOTALL)

    def truncate_title(match):
        title_content = match.group(1)
        # Limitarea la primele 8 cuvinte
        limited_title = ' '.join(title_content.split()[:max_words])
        return f'<title>{limited_title}</title>'

    # Înlocuirea titlului în conținutul HTML
    html_content = title_pattern.sub(truncate_title, html_content)

    # Regex pentru a înlocui .html> cu .html" />
    html_content = re.sub(r'\.html>', r'.html" />', html_content)

    return html_content

# Parcurgerea tuturor fișierelor HTML din folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith('.html'):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Salvează conținutul original pentru a verifica schimbările ulterior
        original_content = html_content

        # Aplicăm modificările
        html_content = limit_title_words(html_content)

        # Verificăm dacă s-au produs schimbări
        if html_content != original_content:
            print(f"Fișierul '{filename}' a fost modificat.")

        # Salvează conținutul modificat înapoi în fișier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

print("Procesarea fișierelor a fost finalizată.")
