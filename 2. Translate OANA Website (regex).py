import os
import re
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Deep Translator Translator for the Romanian language
translator = GoogleTranslator(source='auto', target='ro')

# Words to check
words_to_check = ['whose', 'whois', 'the', 'you', 'which', 'view', 'because', 'here', 'have', 'this', 'two', 'one', 'three', 'four', 'five', 'six', 'seven', 'ten', 'had', 'then', 'see', 'saw', 'also', 'than', 'that', 'must', 'make', 'from', 'else', 'does', 'get', 'will', 'make', 'made', 'yours', 'can', 'your', 'doesn', 'their', 'could', 'from', 'at', 'of', 'my', 'an', 'by', 'with', 'his', 'him', 'she', 'he', 'it', 'may', 'seem', 'and', 'for', 'else', 'while', 'which', 'these', 'let', 'ask', 'has', 'as', 'won', 'keep', 'but', 'everything', 'without', 'thinking', 'about', 'just', 'to', 'doesn', 'if', 'each', 'try', 'I’m', 'them', 'one', 'more', 'much', 'on', 'all', 'even', 'over', 'seems', 'was', 'where', 'were', 'who', 'our', 'most', 'cause', 'be']

# Initialize a counter for the translated tags
translated_tags_count = 0

# Folder path containing the HTML files
folder_path = r"c:\\Folder-Oana\\extracted\\"
translated_folder_path = r"c:\\Folder-Oana\\extracted\\translated\\"

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

        with open(file_path, 'rb') as file:
            try:
                html_content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                # Încercați alte seturi de caractere, cum ar fi 'ISO-8859-1' sau 'latin-1'
                html_content = file.read().decode('ISO-8859-1')

# HTML tags to translate
tags_to_translate = [
    r'(<title>)(.*?)(<\/title>)',
    r'(<meta name="description" content=")(.*?)(>)',
    r'(<div class="sc-jKDlA-D hSgfYV sc-glENfF hIVUeB">)(.*?)(<\/div>)',
    r'(<p>)(.*?)(<\/p>)',
    r'(<h4 class="sc-jMKfon fhunKk">)(.*?)(<\/h4>)',
    r'(<h2">)([\s\S]*?)(<\/h2>)'
    # ... other tags, structured similarly
]

def translate_tags_with_specific_words(file_path, translator, words_to_check):
    global translated_tags_count
    translated_tags_count = 0  # Reset the global counter for each file

    file_name = os.path.basename(file_path)

    if not file_name.endswith('.html'):
        print(f"Ignored file: {file_name}")
        return None

    print(f"Translating tags for file: {file_name}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for tag_regex in tags_to_translate:
        matches = re.finditer(tag_regex, content, re.DOTALL)
        for match in matches:
            tag_content = match.group(2)
            if any(word in tag_content.lower() for word in words_to_check):
                print(f"Translating tag: {match.group(1)}...{match.group(3)}")
                translated_content = translator.translate(tag_content)
                translated_tag = f"{match.group(1)}{translated_content}{match.group(3)}"
                content = content.replace(f"{match.group(1)}{tag_content}{match.group(3)}", translated_tag)
                translated_tags_count += 1

    translated_file_path = os.path.join(translated_folder_path, f"{file_name.rsplit('.', 1)[0]}-ro.html")

    with open(translated_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Translated tags for file: {file_name}")
    return translated_file_path

if __name__ == "__main__":
    folder_path = r"c:\Folder-Oana\extracted"

    ignored_files_list = []
    translated_files_list = []

    html_files_to_translate = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith('.html')]

    for file_path in html_files_to_translate:
        translated_file = translate_tags_with_specific_words(
            file_path,
            translator,
            words_to_check
        )

    print(f"Ignored files: {ignored_files_list}")
    print(f"Translated files: {translated_files_list}")
    print(f"Total translated tags: {translated_tags_count}")
