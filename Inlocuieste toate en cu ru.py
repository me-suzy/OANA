import os
import re

folder_path = r'e:\Carte\BB\17 - Site Leadership\Principal\2024 - TRADUCERI\si'  # schimba toate /si/ si toate "si"
file_count = 0  # Inițializăm contorul de fișiere

# Iterăm prin fiecare fișier din folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Verificăm dacă fișierul este de tip HTML
    if filename.endswith('.html'):
        print(f'Procesez fișierul: {filename}')  # Afișăm numele fișierului procesat
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Găsim toate potențialele match-uri care trebuie înlocuite în interiorul etichetei <div class="categories-name">
        div_pattern1 = re.compile(r'<div class="categories-name">(.*?)</div>', re.DOTALL)
        matches1 = div_pattern1.finditer(content)
        for match in matches1:
            div_content = match.group(1)
            if '<li>' not in div_content:
                div_content = div_content.replace('https://neculaifantanaru.com/en/', 'https://neculaifantanaru.com/si/')
            content = content.replace(match.group(1), div_content)

        # Găsim toate potențialele match-uri care trebuie înlocuite în interiorul etichetei <div class="single-post mx-1">
        div_pattern2 = re.compile(r'<div class="single-post mx-1">(.*?)</div>', re.DOTALL)
        matches2 = div_pattern2.finditer(content)
        for match in matches2:
            div_content = match.group(1)
            if 'href="https://neculaifantanaru.com/en/' in div_content:
                div_content = div_content.replace('https://neculaifantanaru.com/en/', 'https://neculaifantanaru.com/si/')
            content = content.replace(match.group(1), div_content)

        # Găsim toate potențialele match-uri care trebuie înlocuite în interiorul tag-urilor <link>
        link_pattern = re.compile(r'<link [^>]*href="https://neculaifantanaru\.com/en/([^"]+)"[^>]*>')
        matches3 = link_pattern.finditer(content)
        for match in matches3:
            content = content.replace(match.group(0), f'<link rel="canonical" href="https://neculaifantanaru.com/si/{match.group(1)}" />')

        # Găsim toate potențialele match-uri pentru link-uri între <ul class="sidebar-submenu"> și </ul>
        ul_pattern = re.compile(r'(<ul class="sidebar-submenu">.*?</ul>)', re.DOTALL)
        matches_ul = ul_pattern.finditer(content)
        for match in matches_ul:
            ul_content = match.group(1)
            updated_ul_content = ul_content.replace('https://neculaifantanaru.com/en/', 'https://neculaifantanaru.com/si/')
            content = content.replace(ul_content, updated_ul_content)

        # Găsim și înlocuim link-uri între <!--STARTDATES--> și <!--FINNISHDATES-->
        dates_pattern = re.compile(r'(<!--STARTDATES-->.*?<!--FINNISHDATES-->)', re.DOTALL)
        matches_dates = dates_pattern.finditer(content)
        for match in matches_dates:
            dates_content = match.group(1)
            updated_dates_content = dates_content.replace('https://neculaifantanaru.com/en/', 'https://neculaifantanaru.com/si/')
            content = content.replace(dates_content, updated_dates_content)

        # REGEX FIND AND REPLACE LA FINAL
        content = re.sub(r'<html lang="en">', '<html lang="si">', content)
        content = re.sub(r'<meta http-equiv="Content-Language" content="en"/>', '<meta http-equiv="Content-Language" content="si"/>', content)
        content = re.sub(r'https://neculaifantanaru\.com/en/about\.html', 'https://neculaifantanaru.com/si/about.html', content)
        content = re.sub(r' \.</title>', '</title>', content)
        content = re.sub(r'<h3class=', '<h3 class=', content)
        content = re.sub(r'<meta property="og:locale" content="en" />', '<meta property="og:locale" content="si" />', content)
        content = re.sub(r'< /а>', '</а>', content)





        # Suprascriem fișierul cu conținutul modificat
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        file_count += 1  # Incrementăm contorul după fiecare fișier procesat
        print(f'Fișierul {filename} a fost procesat. Total fișiere procesate: {file_count}')  # Afișăm numărul de fișiere procesate

print('Procesul de înlocuire a fost finalizat.')
