import re
import unidecode

def format_title_for_canonical(title):
    title = re.split(r' - ', title, maxsplit=1)[0]
    title = title.lower()
    title = unidecode.unidecode(title)
    title = re.sub(r'\s+', '-', title)
    return title

def format_title_for_title_tag(title):
    title = re.split(r' - ', title, maxsplit=1)[0]
    title = unidecode.unidecode(title)
    return title

def modify_title_and_canonical_tags(content, filename):
    try:
        title_match = re.search(r'<title>(.*?)<\/title>', content)
        canonical_match = re.search(r'<link rel="canonical" href=".*?" \/>', content)

        if title_match:
            title_content = title_match.group(1)

            # Modificarea 1: Înlocuiește diacriticele în tagul <title>
            formatted_title_for_title_tag = format_title_for_title_tag(title_content)
            formatted_title_for_canonical = format_title_for_canonical(title_content)

            # Modificarea 2: Copiază conținutul tagului <title> în tagul <link rel="canonical">
            canonical_tag = f'<link rel="canonical" href="{formatted_title_for_canonical}" />'
            if canonical_match:
                content = content.replace(canonical_match.group(0), canonical_tag)
            else:
                # Dacă nu există tagul <link rel="canonical">, adaugă-l în conținut
                content = content.replace('</title>', f'</title>\n{canonical_tag}')

            # Înlocuirea sigură a tagului <title> cu varianta fără diacritice
            content = re.sub(r'<title>.*?<\/title>', f'<title>{formatted_title_for_title_tag}</title>', content)
    except Exception as e:
        print(f"Eroare la procesarea fișierului {filename}: {e}")

    return content

# Exemplu de utilizare:
content = """<title>Autoevaluare cuprinzătoare pentru absolvenții de facultate - Bebe</title>
<link rel="canonical" href="https://fw.chazidian.com/fanwen2314013/">"""

filename = "exemplu.html"
modified_content = modify_title_and_canonical_tags(content, filename)
print(modified_content)
