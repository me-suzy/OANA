import os
import re
import time
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Deep Translator for Romanian to Amharic translation
translator = GoogleTranslator(source='auto', target='am')

# Folder path containing the original HTML files
folder_path = r"c:\Folder-Oana\extracted"
subfolder_path = r"c:\Folder-Oana\extracted\translated"  # Folder where translated files will be stored

# Minimum file size in kilobytes (1.3 KB)
min_file_size_kb = 1.3

# List of HTML tags to translate
tags_to_translate = [
    r'(<title>)(.*?)(<\/title>)',
    r'(<meta name="description" content=")(.*?)(>)',
    r'(<h1)(.*?)(<\/h1>)',
    r'(<h2)(.*?)(<\/h2>)',
    # Add more regex patterns for other tags you want to translate
]

# Read file with multiple fallback encodings
def read_file_with_fallback_encodings(file_path, encodings=('utf-8', 'ISO-8859-1', 'Windows-1252')):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()  # Try to read the file with the specified encoding
        except UnicodeDecodeError:
            continue  # If decoding fails, try the next encoding
    raise Exception(f"Could not decode the file {file_path} with any of the encodings: {encodings}")

# Translate parts of text handling API request errors
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
                time.sleep(1)  # Sleep for a second before retrying
    return translated

# Ensure the translation subfolder exists
if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)

# Process each file in the directory
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path):
        file_size_kb = os.path.getsize(file_path) / 1024

        if file_size_kb < min_file_size_kb:
            print(f"Deleting file {filename} because it is smaller than 1.3 KB.")
            os.remove(file_path)
            continue

        try:
            html_content = read_file_with_fallback_encodings(file_path)
        except Exception as e:
            print(e)
            continue

        translated_content = ''
        for tag_regex in tags_to_translate:
            matches = re.finditer(tag_regex, html_content, re.DOTALL)
            for match in matches:
                tag_start, tag_content, tag_end = match.groups()
                translated_text = translate_in_parts(tag_content, translator)
                translated_content += f"{tag_start}{translated_text}{tag_end}"

        translated_file_path = os.path.join(subfolder_path, filename)
        with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
            translated_file.write(translated_content)
        print(f"Translated file saved: {translated_file_path}")
