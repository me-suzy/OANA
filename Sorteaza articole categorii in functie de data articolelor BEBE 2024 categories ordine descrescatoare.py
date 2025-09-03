import os
import re
from datetime import datetime

def extract_date(text):
    """Extract and correct date from text, handling minor typos."""
    date_match = re.search(r'On\s+([A-Za-z]+(?:lie)?\s+\d{1,2},\s+\d{4})', text)
    if date_match:
        raw_date = date_match.group(1)
        # Correct common typos like "Aprlie" to "April"
        corrected_date = raw_date.replace('Aprlie', 'April').replace('Maylie', 'May')
        try:
            return datetime.strptime(corrected_date, '%B %d, %Y')
        except ValueError:
            print(f"Warning: Could not parse date '{raw_date}', using minimum date.")
            return datetime.min
    return datetime.min

def sort_articles(html_content, ascending=True):
    """Sort articles within the ARTICOL CATEGORIE section by date."""
    pattern = re.compile(r'(<!-- ARTICOL CATEGORIE START -->.*?<!-- ARTICOL CATEGORIE FINAL -->)', re.DOTALL)
    match = pattern.search(html_content)

    if match:
        section_to_sort = match.group(1)
        # Extract individual articles
        article_pattern = re.compile(r'(<table width="\d+" border="0">.*?<p class="text_obisnuit"></p>)', re.DOTALL)
        articles = article_pattern.findall(section_to_sort)

        # Sort articles by date
        sorted_articles = sorted(articles, key=lambda x: extract_date(x), reverse=not ascending)

        # Reconstruct sorted section
        sorted_section = '<!-- ARTICOL CATEGORIE START -->\n' + '\n'.join(sorted_articles) + '\n<!-- ARTICOL CATEGORIE FINAL -->'

        # Replace original section with sorted one
        return html_content.replace(section_to_sort, sorted_section)

    return html_content

def process_file(file_path, ascending=True):
    """Process a single HTML file and sort its articles."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            html_content = file.read()

        sorted_html = sort_articles(html_content, ascending)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(sorted_html)

        print(f"Articolele au fost sortate cu succes în {file_path} (ordine {'crescătoare' if ascending else 'descrescătoare'})")
    except Exception as e:
        print(f"Eroare la procesarea fișierului {file_path}: {e}")

if __name__ == "__main__":
    # Directorul care conține fișierele HTML
    directory = r"d:\3\Input"

    # Verifică dacă directorul există
    if not os.path.isdir(directory):
        print(f"Eroare: Directorul '{directory}' nu există.")
    else:
        # Sortează în ordine descrescătoare (cea mai recentă dată la început)
        ascending_order = False
        for filename in os.listdir(directory):
            if filename.endswith('.html'):
                file_path = os.path.join(directory, filename)
                process_file(file_path, ascending_order)
        print("Procesarea tuturor fișierelor HTML a fost finalizată.")