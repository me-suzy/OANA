import os
import regex

def remove_double_quotes_and_pipe_from_meta(html_content):
    # Regex pentru a identifica tagurile meta și pentru a înlocui ghilimelele și caracterul '|' din atributul content
    pattern = regex.compile(r'(<meta name="description" content=")(.*?)(">)', regex.DOTALL)

    def replace_quotes_and_pipe(match):
        # Eliminarea ghilimelelor și caracterului '|' din conținutul atributului content
        content_without_quotes_and_pipe = match.group(2).replace('„', '').replace('”', '').replace('"', '').replace('|', '')
        return match.group(1) + content_without_quotes_and_pipe + match.group(3)

    # Înlocuirea ghilimelelor și caracterului '|' în toate tagurile meta potrivite
    replaced_content = pattern.sub(replace_quotes_and_pipe, html_content)

    return replaced_content

def process_html_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.html'):
            file_path = os.path.join(folder_path, filename)

            print(f'Procesare: {file_path}')

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            new_content = remove_double_quotes_and_pipe_from_meta(content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

    print('Toate fișierele au fost modificate.')

# Calea către folderul cu fișierele HTML
folder_path = r'c:\Folder1\test'

# Procesarea fișierelor
process_html_files(folder_path)
