import os
import re
import unicodedata

cale_folder_html = r"C:\Folder-Oana\extracted\salvate"

def read_text_from_file(file_path):
    with open(file_path, encoding='utf8') as f:
        text = f.read()
        return text

def write_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf8') as f:
        f.write(text)

def remove_diacritics(word):
    return ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn')

print('Going through folder')
amount = 1

# prelucrare continut
dict_simboluri = dict()
dict_simboluri['&#259;'] = 'a'
dict_simboluri['&#226;'] = 'a'
dict_simboluri['&atilde;'] = 'a'
dict_simboluri['&acirc;'] = 'a'
dict_simboluri['&#x103;'] = 'a'
dict_simboluri['&#xE2;'] = 'a'
dict_simboluri['ӑ'] = 'a'
dict_simboluri['ȃ'] = 'a'
dict_simboluri['â'] = 'a'
dict_simboluri['ă'] = 'a'
dict_simboluri['ã'] = 'a'
dict_simboluri['à'] = 'a'
dict_simboluri['á'] = 'a'
dict_simboluri['å'] = 'a'
dict_simboluri['ä'] = 'a'
dict_simboluri['Á'] = 'A'
dict_simboluri['É'] = 'E'
dict_simboluri['ö'] = 'o'
dict_simboluri['ă'] = 'a'
dict_simboluri['ō'] = 'o'
dict_simboluri['ñ'] = 'n'
dict_simboluri['ï'] = 'i'
dict_simboluri['ç'] = 'c'
dict_simboluri['½'] = ''
dict_simboluri[' & '] = ''


dict_simboluri['&hellip;'] = ''
dict_simboluri['&#8230;'] = ''
dict_simboluri['\&quot;'] = ''
dict_simboluri['&#8211;'] = '- '

dict_simboluri['Â '] = ' '
dict_simboluri['Â '] = ' '
dict_simboluri['&#039;'] = '\''
dict_simboluri['„'] = ''
dict_simboluri['”'] = ''
dict_simboluri['['] = ''
dict_simboluri[']'] = ''
dict_simboluri['/'] = ''
dict_simboluri['}'] = ''
dict_simboluri['{'] = ''

dict_simboluri['&icirc;'] = 'i'
dict_simboluri['&#206;'] = 'i'
dict_simboluri['&#238;'] = 'i'
dict_simboluri['&#xEE;'] = 'i'
dict_simboluri['&#xCE;'] = 'i'
dict_simboluri['&#206;'] = 'i'
dict_simboluri['&#xEE;'] = 'i'
dict_simboluri['&#xCE;'] = 'i'
dict_simboluri['ȋ'] = 'i'
dict_simboluri['î'] = 'i'
dict_simboluri['&Icirc;'] = 'I'
dict_simboluri['Ĩ'] = 'I'
dict_simboluri['Ä¨'] = 'I'
dict_simboluri['Ĩ¨'] = 'I'
dict_simboluri['Î'] = 'I'
dict_simboluri['ī'] = 'i'
dict_simboluri['ĭ'] = 'i'
dict_simboluri['í'] = 'i'
dict_simboluri['í'] = 'i'
dict_simboluri['!'] = ' '
dict_simboluri['('] = '-'
dict_simboluri[')'] = ' '
dict_simboluri['  '] = ' '
dict_simboluri[',,'] = ' '
dict_simboluri['Ĩ'] = 'I'
dict_simboluri['é'] = 'e'
dict_simboluri['ê'] = 'e'
dict_simboluri['Ã©'] = 'e'
dict_simboluri['a©'] = 'e'
dict_simboluri['è'] = 'e'
dict_simboluri['ë'] = 'e'
dict_simboluri['Ë'] = 'e'

dict_simboluri['ó'] = 'o'
dict_simboluri['ñ'] = 'n'
dict_simboluri['ú'] = 'u'
dict_simboluri['ü'] = 'u'

dict_simboluri['&#537;'] = 's'
dict_simboluri['&#536;'] = 's'
dict_simboluri['&#350;'] = 's'
dict_simboluri['&#x219;'] = 's'
dict_simboluri['&#351;'] = 's'
dict_simboluri['ş'] = 's'
dict_simboluri['ș'] = 's'
dict_simboluri['Ş'] = 'S'
dict_simboluri['Ș'] = 'S'
dict_simboluri['Ș'] = 'S'
dict_simboluri['š'] = 's'
dict_simboluri['ś'] = 's'
dict_simboluri['ș'] = 's'
dict_simboluri['ṣ'] = 's'

dict_simboluri['&quot;'] = ''
dict_simboluri['&#8217;'] = ''
dict_simboluri['&rdquo;'] = ''
dict_simboluri['&rsquo;'] = ''
dict_simboluri['&bdquo;'] = ''
dict_simboluri['&ldquo;'] = ''
dict_simboluri['&#8222;'] = ''
dict_simboluri['&#8220;'] = ''
dict_simboluri['&#8221;'] = ''
dict_simboluri['&lt;'] = ''
dict_simboluri['&lt;'] = ''
dict_simboluri['«'] = ''
dict_simboluri['»'] = ''
dict_simboluri['“'] = ''
dict_simboluri['”'] = ''
dict_simboluri['"'] = ''
dict_simboluri[':'] = ''
dict_simboluri['\''] = ''
dict_simboluri['&amp;'] = ''

dict_simboluri['&#539;'] = 't'
dict_simboluri['&#355;'] = 't'
dict_simboluri['&#354;'] = 't'
dict_simboluri['&#x21B;'] = 't'
dict_simboluri['ţ'] = 't'
dict_simboluri['ț'] = 't'
dict_simboluri['Ţ'] = 'T'
dict_simboluri['Ț'] = 'T'
dict_simboluri['ť'] = 't'
dict_simboluri['ṭ'] = 't'
dict_simboluri['&nbsp;'] = ' '
# dict_simboluri['.'] = '. '
dict_simboluri['-'] = ' '
dict_simboluri['&gt;'] = ' '
dict_simboluri['" "'] = '"'

for filename in os.listdir(cale_folder_html):
    if filename == 'y_key_e479323ce281e459.html' or filename == 'directory.html':
        continue
    if filename.endswith('.html'):
        cale_fisier_html = os.path.join(cale_folder_html, filename)
        html_content = read_text_from_file(cale_fisier_html)

        # Salvează conținutul actual al tagului meta description
        meta_description_pattern = re.compile(r'<meta name="description" content="(.*?)">', re.DOTALL)
        existing_description = re.search(meta_description_pattern, html_content)
        if existing_description:
            existing_description = existing_description.group(1)

        # Operațiuni de găsire și înlocuire la începutul codului
        html_content = re.sub(r'(<meta name="description" content=")(.*?)(/>)', r'\1\2">', html_content)
        html_content = re.sub(r'""', r'"">', html_content)

        # Prelucrare simboluri în conținutul paragrafului
        para_pattern = re.compile(r'<p.*?>(.*?)</p>', re.DOTALL)
        para = re.findall(para_pattern, html_content)

        if len(para) > 0:
            lista_cuvinte = list()
            for txt in para:
                # Îndepărtează diacriticele și aplică prelucrarea simbolurilor
                txt = remove_diacritics(txt)
                for simbol in dict_simboluri.keys():
                    txt = txt.replace(simbol, dict_simboluri[simbol])
                lista_cuvinte.extend(re.findall(r'[a-zA-Z\-\']+', txt))

            # Construiește noul conținut pentru tagul meta description
            content = (existing_description + " " + " ".join(lista_cuvinte[:80])) if existing_description else " ".join(lista_cuvinte[:80])

            # Înlocuiește conținutul tagului meta description
            html_content = re.sub(meta_description_pattern, r'<meta name="description" content="{}">'.format(content), html_content)

            print(f'{filename} parsed ({amount})')
            amount += 1
            write_to_file(html_content, cale_fisier_html)
        else:
            print("Nu am gasit tag-uri cu text_obisnuit2: ", filename)
    else:
        continue
