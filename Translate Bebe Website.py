import os
import re
import time
from deep_translator import GoogleTranslator
from deep_translator.exceptions import RequestError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Deep Translator Translator for Romanian language
translator = GoogleTranslator(source='auto', target='ka')

# Initialize a counter for the translated files
translated_files_count = 0



# Folder path containing the HTML files
folder_path = r"c:\\Folder-Oana\\extracted\\" # calea fisierelor en originale. Nu schimbi nimic aici




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
    r'(<h4)(.*?)(<\/h4>)',
    r'(<h5)(.*?)(<\/h5>)',
    r'(<h6)(.*?)(<\/h6>)',
    r'(<h3)(.*?)(<\/h3)',
    r'(<h1)(.*?)(<\/h1)',
    r'(<h2)(.*?)(<\/h2)',
    r'(<p class="text_obisnuit2">)(.*?)(<\/p>)',
    r'(<p class="text_obisnuit">)(.*?)(<\/p>)',
    r'(<p class="mb-35px)(.*?)(</p>)',
    # Adaugă regex-ul tău pentru <p class="book-description">
    r'(<p class="book-description">)(.*?)(<\/p>)',
    r'(html" class="color-grey">)(.*?)(</a>)'
]

def find_html_files_only_in_folder(folder, subfolder):
    folder_files = set(os.listdir(folder))
    subfolder_files = set(os.listdir(subfolder))

    html_files_only_in_folder = {f for f in folder_files - subfolder_files if f.endswith('.html')}

    return html_files_only_in_folder

def translate_in_parts(text, translator, max_length=4800, max_retries=5):
    translated = ''
    while text:
        part = text[:max_length]
        text = text[max_length:]

        attempt = 0
        while attempt < max_retries:
            try:
                translated_part = translator.translate(part)
                translated += translated_part
                break
            except RequestError:
                attempt += 1
                time.sleep(1)
                print(f"Reîncercarea {attempt} pentru fragmentul: {part[:30]}...")
    return translated

def apply_regex_before_translation(content):
    # Adaugă regex-uri de căutare și înlocuire aici
    # Exemplu: content = re.sub(r'pattern', 'replacement', content)



    content = re.sub(r'”></p>', r'">', content, flags=re.MULTILINE)
    content = re.sub(r'<p><meta', r'<meta', content, flags=re.MULTILINE)

    # Remove paragraphs with less than 10 words (multi-line)
    content = re.sub(r"<p>.{0,9}<\/p>", "", content, flags=re.MULTILINE)

    # Remove leading > from the first paragraph
    content = re.sub(r"^>", "", content)

    # Remove U+200B non-breaking space (hair space)
    content = re.sub(r"\x200B", "", content)
    content = re.sub(r"\u00C2", "", content)
    content = re.sub(r"\u001C", "", content)  # NSBN
    content = re.sub(r"<p>\d+</p>", "", content)

    # Remove escaped characters
    content = re.sub(r"\\\\.*$", "", content)



    content = re.sub(r'^\s', '', content, flags=re.MULTILINE)


    content = re.sub(r'<p><title>', '<title>', content)
    content = re.sub(r'<p></p>', '', content)
    content = re.sub(r'</title></p>', '</title>', content)
    content = re.sub(r'<p><meta name=', '<meta name=', content)
    content = re.sub(r'"/></p>', '"/>', content)
    content = re.sub(r'<p><p>', '<p>', content, flags=re.MULTILINE)
    content = re.sub(r'</p></p>', '</p>', content, flags=re.MULTILINE)
    content = re.sub(r'^</p>$', '', content, flags=re.MULTILINE)  # sterge orice <p> gol de la inceputul linilor
    content = re.sub(r'<p style=".*?">', '<p>', content, flags=re.MULTILINE)
    content = re.sub(r'<font.*?">', '', content, flags=re.MULTILINE)
    content = re.sub(r'</font>', '', content, flags=re.MULTILINE)
    content = re.sub(r'"\/"', '"', content, flags=re.MULTILINE)
    content = re.sub(r'<strong>|</strong>', ' ', content, flags=re.MULTILINE)
    content = re.sub(r'<p>\d+</p>', '', content, flags=re.MULTILINE)
    content = re.sub(r'‘|’', '', content, flags=re.MULTILINE)
    content = re.sub(r'”/></p>', '"/>', content, flags=re.MULTILINE)
    content = re.sub(r'”|“', '', content, flags=re.MULTILINE)

    return content




def translate_html_tags(file_path, translator, subfolder_path, ignored_files, translated_files):
    global translated_tags_count
    translated_tags_count = 0  # Reset the global counter for each file

    file_name = os.path.basename(file_path)

    if not file_name.endswith('.html'):
        ignored_files.append(file_name)
        print(f"Ignored file: {file_name}")
        return None

    print(f"Translating file: {file_name}")  # Print the file being translated

    local_tag_count = 0  # Local counter for tags within this file

    translated_file_path = os.path.join(subfolder_path, file_name.rsplit('.', 1)[0] + '_ka.html')  # schimbi aici sufixul _ de final

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = apply_regex_before_translation(content)

    for tag_regex in tags_to_translate:
        matches = re.finditer(tag_regex, content, re.DOTALL)
        for match in matches:
            local_tag_count += 1  # Increment local tag counter
            tag_start = match.group(1)
            tag_content = match.group(2)
            tag_end = match.group(3)

            print(f"Translating tag {local_tag_count}: {tag_start}...{tag_end}")

            translated_content = translate_in_parts(tag_content, translator)
            translated_tag = f"{tag_start}{translated_content}{tag_end}"

            content = content.replace(f"{tag_start}{tag_content}{tag_end}", translated_tag)
            translated_tags_count += 1




    # Aplică adăugarea de taguri <p> pentru linii de text


    # Aplică regex-uri DUPA TRADUCERE !!!!!!!


    # content = remove_zwsp(content)
    content = re.sub(r'<p></p>', '', content, flags=re.MULTILINE)
    content = re.sub(r'<p>\d+</p>', '', content, flags=re.MULTILINE)
    content = re.sub(r'”/></p>', '"/>', content, flags=re.MULTILINE)
    content = re.sub(r'/></p>', '/>', content, flags=re.MULTILINE)
    content = re.sub(r'»>|»\.>', '">', content, flags=re.MULTILINE)
    content = re.sub(r'<p>                    <p', '<p', content, flags=re.MULTILINE)
    content = re.sub(r'<p>        <p', '<p', content, flags=re.MULTILINE)





    with open(translated_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    translated_files.append(translated_file_path)
    print(f"Translated file: {translated_file_path}")
    return translated_file_path








if __name__ == "__main__":
    folder_path = r"c:\Folder-Oana\extracted"
    subfolder_path = r"c:\Folder-Oana\extracted\translated" # schimbi aici folderul in care vrei sa puna traducerea

    ignored_files_list = []
    translated_files_list = []

    # Asigură-te că subfolderul există
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    html_files_to_translate = find_html_files_only_in_folder(folder_path, subfolder_path)
    for file_name in html_files_to_translate:
        translated_file = translate_html_tags(
            os.path.join(folder_path, file_name),
            translator,
            subfolder_path,
            ignored_files_list,
            translated_files_list
        )

    print(f"Ignored files: {ignored_files_list}")
    print(f"Translated files: {translated_files_list}")
    # print(f"Total translated tags: {translated_tags_count}")
