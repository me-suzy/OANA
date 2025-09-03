import os

cale_folder_html = r"C:\Folder-Oana\extracted\salvate"
output_file_path = r"D:\fisiere-fara-link.txt"
search_text = "neculaifantanaru.com"

def verifica_link(html_content):
    start_marker = "<!-- ARTICOL START -->"
    end_marker = "<!-- ARTICOL FINAL -->"

    start_index = html_content.find(start_marker)
    end_index = html_content.find(end_marker, start_index + len(start_marker))

    if start_index != -1 and end_index != -1:
        article_content = html_content[start_index + len(start_marker):end_index].lower()
        return search_text not in article_content
    else:
        return False

def read_text_from_file(file_path):
    with open(file_path, encoding='utf8') as f:
        text = f.read()
        return text

def write_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf8') as f:
        f.write(text)

def main():
    with open(output_file_path, 'w', encoding='utf8') as output_file:
        for filename in os.listdir(cale_folder_html):
            if filename.endswith('.html'):
                cale_fisier_html = os.path.join(cale_folder_html, filename)
                html_content = read_text_from_file(cale_fisier_html)
                if verifica_link(html_content):
                    output_file.write(filename + '\n')
                    print(f'{filename} adaugat in fisierul de iesire')

if __name__ == "__main__":
    main()
