import os
import regex

def remove_quotes_from_meta_tags(html_content):
    # Pattern pentru <meta name="description" content="...">
    pattern1 = regex.compile(r'(<meta name="description" content=")(.*?)(">)', regex.DOTALL)

    # Pattern pentru <meta property="og:description" content="...">
    pattern2 = regex.compile(r'(<meta property="og:description" content=")(.*?)(">)', regex.DOTALL)

    # Pattern pentru JSON "description": "..."
    pattern3 = regex.compile(r'("description": ")(.*?)(",)', regex.DOTALL)

    def clean_content(match):
        # Eliminarea ghilimelelor, apostrofurilor și caracterului '|' din conținut
        cleaned_content = (match.group(2)
                         .replace('„', '')
                         .replace('"', '')
                         .replace('"', '')
                         .replace("'", '')
                         .replace("'", '')
                         .replace("'", '')
                         .replace('|', ''))
        return match.group(1) + cleaned_content + match.group(3)

    # Aplicarea tuturor pattern-urilor
    content = pattern1.sub(clean_content, html_content)
    content = pattern2.sub(clean_content, content)
    content = pattern3.sub(clean_content, content)

    return content

def process_html_files(folder_path):
    if not os.path.exists(folder_path):
        print(f'Folderul nu există: {folder_path}')
        return

    files_processed = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.html'):
            file_path = os.path.join(folder_path, filename)

            print(f'Procesare: {file_path}')

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                new_content = remove_quotes_from_meta_tags(content)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)

                files_processed += 1
            except Exception as e:
                print(f'Eroare la procesarea fișierului {file_path}: {e}')

    print(f'Au fost procesate {files_processed} fișiere din folderul: {folder_path}')

def main():
    # Lista cu toate folderele de procesat
    folders = [
        r'e:\Carte\BB\17 - Site Leadership\Principal 2022\en',
        r'e:\Carte\BB\17 - Site Leadership\Principal 2022\ro',
        r'e:\Carte\BB\17 - Site Leadership\Principal\en',
        r'e:\Carte\BB\17 - Site Leadership\Principal\ro'
    ]

    total_folders = len(folders)
    processed_folders = 0

    print(f'Se vor procesa {total_folders} foldere...\n')

    for folder_path in folders:
        print(f'=== Procesare folder: {folder_path} ===')
        process_html_files(folder_path)
        processed_folders += 1
        print(f'Progres: {processed_folders}/{total_folders} foldere complete\n')

    print('Toate folderele au fost procesate cu succes!')

if __name__ == "__main__":
    main()