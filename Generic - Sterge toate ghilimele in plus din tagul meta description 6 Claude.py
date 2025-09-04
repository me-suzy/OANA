import os
import regex

def remove_quotes_from_meta_description(html_content):
    """Curăță meta name="description" - VERSIUNEA SIMPLĂ ȘI FUNCȚIONALĂ"""
    pattern = regex.compile(r'(<meta name="description" content=")(.*?)(">)', regex.DOTALL)

    def replace_quotes(match):
        content_clean = (match.group(2)
                        .replace('„', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('|', ''))
        return match.group(1) + content_clean + match.group(3)

    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_og_description(html_content):
    """Curăță meta property="og:description" """
    pattern = regex.compile(r'(<meta property="og:description" content=")(.*?)("\s*/>)', regex.DOTALL)

    def replace_quotes(match):
        content_clean = (match.group(2)
                        .replace('„', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('|', ''))
        return match.group(1) + content_clean + match.group(3)

    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_json_description(html_content):
    """Curăță JSON descriptions"""
    # Pattern 1: cu spații
    pattern1 = regex.compile(r'("description":\s*")(.*?)(",)', regex.DOTALL)

    def replace_quotes(match):
        content_clean = (match.group(2)
                        .replace('„', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('|', ''))
        return match.group(1) + content_clean + match.group(3)

    html_content = pattern1.sub(replace_quotes, html_content)

    # Pattern 2: fără spații
    pattern2 = regex.compile(r'("description":")(.*?)(",)', regex.DOTALL)
    html_content = pattern2.sub(replace_quotes, html_content)

    return html_content

def process_html_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            print(f'Procesare: {filename}')

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            original_length = len(content)

            # Aplică curățările simple și funcționale
            content = remove_quotes_from_meta_description(content)
            content = remove_quotes_from_og_description(content)
            content = remove_quotes_from_json_description(content)

            new_length = len(content)
            chars_removed = original_length - new_length

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f'   - Caractere eliminate: {chars_removed}')

    print('Toate fișierele au fost procesate corect.')

# Folosim abordarea simplă care funcționează
folder_path = r'c:\Folder1\test'
if os.path.exists(folder_path):
    print('Revin la metoda simplă și funcțională...')
    process_html_files(folder_path)