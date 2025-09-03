import os
import re

# Căile către directoare
translated_folder = r"c:\Folder-Oana\extracted\translated"  # aici sunt fisierele din vechiul design
index_folder = r"c:\Folder-Oana\extracted\index"
saved_folder = r"c:\Folder-Oana\extracted\salvate"  # aici sunt salvate fisierele cu noul design

# Citirea șablonului index.html
with open(os.path.join(index_folder, 'index.html'), 'r', encoding='utf-8') as file:
    index_template = file.read()

# Asigură că directorul de salvare există
if not os.path.exists(saved_folder):
    os.makedirs(saved_folder)

files_without_source = []  # Lista pentru a stoca fișierele fără linia specificată

# Procesarea fiecărui fișier din folderul translated
for filename in os.listdir(translated_folder):
    if filename.endswith((".html", ".htm")):
        with open(os.path.join(translated_folder, filename), 'r', encoding='utf-8') as file:
            content = file.read()

        # REGEX-URI INAINTE DE RULAREA CODULUI
        content = re.sub(r'<link rel="canonical" href="(.*?)"/>', r'<link rel="canonical" href="\1" />', content)

        new_content = index_template

        # Verifică dacă există deja un tag <link rel="canonical">
        if '<link rel="canonical" href="' not in content:
            # Extrage conținutul tag-ului <title> din fișierul tradus și creează un tag <link rel="canonical> cu acest conținut
            title_match = re.search(r'<title>(.*?)<\/title>', content)
            if title_match:
                title_content = title_match.group(1)
                canonical_tag = f'<link rel="canonical" href="{title_content}" />'
                content = content.replace('</head>', f'{canonical_tag}\n</head>')

        # Extrage titlul și actualizează <h1> în index_template
        title_match = re.search(r'<title>(.*?)<\/title>', content)
        if title_match:
            title_content = title_match.group(1)
            new_content = re.sub(r'<h1 class="pt-3 font-weight-bold blog_detail-heading">.*?</h1>',
                                 f'<h1 class="pt-3 font-weight-bold blog_detail-heading">{title_content}</h1>',
                                 new_content)

        # Actualizează tag-urile necesare
        for tag in ['<title>.*?</title>', '<link rel="canonical" href=".*?" />', '<meta name="description" content=".*?">']:
            match = re.search(tag, content)
            if match:
                new_content = re.sub(tag, match.group(), new_content)

        # Extrage conținutul articolului și aplică modificările necesare
        canonical_link = re.search(r'<link rel="canonical" href="(.*?)" />', content)
        if canonical_link:
            article_content = content.split(canonical_link.group())[1]
            article_content = re.sub(r'<h2>(.*?)<\/h2>', r'<p class="mt-1">\1</p>', article_content)
            article_content = re.sub(r'<p>(.*?)<\/p>', r'<p class="text_dummy">\1</p>', article_content)
            article_content = re.sub(r'^(?!.*<[^>]+>)(.*\S.*)$', r'<p class="text_dummy">\1</p>', article_content, flags=re.MULTILINE)

            # Găsește indexul de încheiere al comentariului <!-- ARTICOL FINAL -->
            index_articol_final = new_content.find('<!-- ARTICOL FINAL -->')

            # Adaugă linia înainte de comentariul <!-- ARTICOL FINAL -->
            new_content = new_content[:index_articol_final] + article_content + f'<br><br>\n<p class="pl-3 pt-3">* Source: <a href="{canonical_link.group(1)}" class="color-bebe" target="_new">{canonical_link.group(1)}</a></p>\n\n' + new_content[index_articol_final:]

        # Verifică dacă linia specificată lipsește și adaugă numele fișierului în lista files_without_source
        if '<p class="pl-3 pt-3">* Source:' not in new_content:
            files_without_source.append(filename)

        # Salvează fișierul modificat
        with open(os.path.join(saved_folder, filename), 'w', encoding='utf-8') as file:
            file.write(new_content)

# Afișează fișierele care nu au linia specificată
print("Fișiere fără linia '<p class=\"pl-3 pt-3\">* Source:' înainte de procesare:")
for file_name in files_without_source:
    print(file_name)

print("Toate fișierele au fost procesate și salvate.")
