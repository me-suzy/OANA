import re

def extract_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        html_content = file.read()
    # Extrage conținutul între comentariile specificate
    pattern_section = re.compile(r'<!-- ARTICOL CATEGORIE START -->(.*?)<!-- ARTICOL CATEGORIE FINAL -->', re.DOTALL)
    section_matches = pattern_section.findall(html_content)
    all_links = []
    for section_content in section_matches:
        # Caută link-urile în secțiunea extrasă
        pattern_links = re.compile(r'<span class="den_articol"><a href="https://neculaifantanaru\.com/(.*?)"')
        links = pattern_links.findall(section_content)
        # Elimină prefixul "en/" din link-uri
        links = [link.replace('en/', '', 1) for link in links]
        all_links.extend(links)
    return all_links

# Calea către fișierul specific
file_path = r"e:\Carte\BB\17 - Site Leadership\Principal\ro\python-scripts-examples.html"

# Extrage link-urile din fișier
links = extract_links_from_file(file_path)

# Afișează link-urile găsite, separate prin punct și virgulă
if links:
    print("Link-uri găsite în python-scripts-examples.html:\n\n")
    print(";*".join(links) + ";")
else:
    print("Nu s-au găsit link-uri în secțiunile specificate din fișier.")