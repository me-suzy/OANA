import requests
from bs4 import BeautifulSoup, Comment
from collections import Counter
import re

def normalize_word(word):
    replacements = {
        'ă': 'a', 'â': 'a', 'î': 'i', 'ț': 't', 'ș': 's',
        'Ă': 'A', 'Â': 'A', 'Î': 'I', 'Ț': 'T', 'Ș': 'S',
        'ş': 's', 'Ş': 'S', 'ţ': 't', 'Ţ': 'T'
    }
    for search, replace in replacements.items():
        word = word.replace(search, replace)
    return word

# Lista cuvintelor de legătură normalizate
LISTA_CUVINTE_LEGATURA = [
    'in', 'la', 'unei', 'si', 'sa', 'se', 'de', 'prin', 'unde', 'care', 'a', 'sale', 'eu', 'ele', 'noi', 'insele', 'insisi', 'spre', 'catre', 'mine', 'mea', 'meu', 'atunci', 'cand', 'pe', 'insumi', 'proprie', 'propria', 'propriul', 'propriei', 'propriului', 'printre', 'fiindca', 'deoarece', 'incat', 'avea', 'avea', 'avand', 'vor', 'ar', 'inca',
    'al', 'prea', 'lui', 'din', 'ai', 'unui', 'acei', 'un', 'doar', 'tine', 'mult', 'putin', 'deci', 'al', 'primul', 'doilea', 'precum', 'fel', 'deoarece', 'pentru', 'asa', 'tot', 'cu', 'ale', 'sau', 'dintre', 'intre', 'cu', 'ce', 'va', 'fi', 'este', 'cand', 'o',
    'cine', 'aceasta', 'ca', 'dar', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
    'to', 'was', 'your', 'you', 'is', 'are', 'iar', 'fara', 'asta', 'pe', 'tu',
    'nu', 'mai', 'ne', 'le', 'intr', 'cum', 'e', 'for', 'she', 'it', 'esti',
	'this', 'that', 'how', 'can', 't', 'must', 'be', 'the', 'and', 'do', 'so', 'or', 'ori',
	'who', 'what', 'if', 'of', 'on', 'i', 'we', 'they', 'them', 'but', 'where', 'by', 'an',
	'mi', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'made', 'my', 'me',
	'vom', 'voi', 'ei', 'cat', 'ar', 'putea', 'poti', 'sunteti', 'inca', 'still', 'noi', 'l',
	'ma', 's', 'dupa', 'after', 'under', 'sub', 'niste', 'some', 'those', 'he', 'no', 'too',
	'fac', 'made', 'make', 'cei', 'most', 'face', 'pentru', 'cat', 'cate', 'much', 'more', 'many',
    'sale', 'tale', 'tau', 'has', 'sunt', 'his', 'yours', 'only', 'as', 'toate', 'all', 'tot', 'incat',
	'which', 'ti', 'asa', 'like', 'these', 'because', 'unor', 'caci', 'ele', 'have', 'haven', 'te',
	'cea', 'else', 'imi', 'iti', 'should', 'could', 'not', 'even', 'chiar', 'when', 'ci', 'ne', 'ni',
	'her', 'our', 'alta', 'another', 'other', 'decat', 'acelasi', 'same', 'au', 'had', 'haven', 'hasn',
	'alte', 'alt', 'others', 'ceea', 'cel', 'cele', 'alte', 'despre', 'about', 'acele', 'acel', 'acea',
	'decit', 'with', '_', 'fata', 'towards', 'against', 'cind', 'dinspre', 'fost', 'been', 'era', 'daca',
	'eu', 'el', 'him', 'ea', 'will', 'am', 'cannot', 'between', 'cause', 'may', 'couldn',
    'IN', 'LA', 'UNEI', 'SI', 'SA', 'SE', 'DE', 'PRIN', 'UNDE', 'CARE', 'A',
    'AL', 'PREA', 'LUI', 'DIN', 'AI', 'UNUI', 'ACEI', 'UN', 'DOAR', 'TINE',
    'ALE', 'SAU', 'DINTRE', 'INTRE', 'CU', 'CE', 'VA', 'FI', 'ESTE', 'CAND', 'O',
    'CINE', 'ACEASTA', 'CA', 'DAR', 'TO', 'WAS', 'YOUR', 'YOU', 'IS', 'ARE', 'IAR', 'FARA', 'ASTA', 'PE', 'TU',
    'NU', 'MAI', 'NE', 'LE', 'INTR', 'CUM', 'E', 'FOR', 'SHE', 'IT', 'ESTI',
	'THIS', 'THAT', 'HOW', 'CAN', 'T', 'MUST', 'BE', 'THE', 'AND', 'DO', 'SO', 'OR', 'ORI',
	'WHO', 'WHAT', 'IF', 'OF', 'ON', 'I', 'WE', 'THEY', 'THEM', 'BUT', 'WHERE', 'BY', 'AN',
	'MI', 'MADE', 'MY', 'ME', 'VOM', 'VOI', 'EI', 'CAT', 'AR', 'PUTEA', 'POTI', 'SUNTETI', 'INCA', 'STILL', 'NOI', 'L',
	'MA', 'S', 'DUPA', 'AFTER', 'UNDER', 'SUB', 'NISTE', 'SOME', 'THOSE', 'HE', 'NO', 'TOO',
	'FAC', 'MADE', 'MAKE', 'CEI', 'MOST', 'FACE', 'PENTRU', 'CAT', 'CATE', 'MUCH', 'MORE', 'MANY',
    'SALE', 'TALE', 'TAU', 'HAS', 'SUNT', 'HIS', 'YOURS', 'ONLY', 'AS', 'TOATE', 'ALL', 'TOT', 'INCAT',
	'WHICH', 'TI', 'ASA', 'LIKE', 'THESE', 'BECAUSE', 'UNOR', 'CACI', 'ELE', 'HAVE', 'HAVEN', 'TE',
	'CEA', 'ELSE', 'IMI', 'ITI', 'SHOULD', 'COULD', 'NOT', 'EVEN', 'CHIAR', 'WHEN', 'CI', 'NE', 'NI',
	'HER', 'OUR', 'ALTA', 'ANOTHER', 'OTHER', 'DECAT', 'ACELASI', 'SAME', 'AU', 'HAD', 'HAVEN', 'HASN',
	'ALTE', 'ALT', 'OTHERS', 'CEEA', 'CEL', 'CELE', 'ALTE', 'DESPRE', 'ABOUT', 'ACELE', 'ACEL', 'ACEA',
	'DECIT', 'WITH', '_', 'FATA', 'TOWARDS', 'AGAINST', 'CIND', 'DINSPRE', 'FOST', 'BEEN', 'ERA', 'DACA',
	'EU', 'EL', 'HIM', 'EA', 'WILL', 'AM', 'CANNOT', 'BETWEEN', 'CAUSE', 'MAY', 'COULDN',
    'In', 'La', 'Unei', 'Si', 'Sa', 'Se', 'De', 'Prin', 'Unde', 'Care', 'Al', 'Prea', 'Lui', 'Din', 'Ai', 'Unui',
    'Acei', 'Un', 'Doar', 'Tine', 'Ale', 'Sau', 'Dintre', 'Intre', 'Cu', 'Ce', 'Va', 'Fi', 'Este', 'Cand', 'Cine', 'Aceasta', 'Ca',
    'Dar', 'Ii', 'Iii', 'Iv', 'V', 'Vi', 'Vii', 'Viii', 'To', 'Was', 'Your', 'You', 'Is', 'Are', 'Iar', 'Fara', 'Asta', 'Pe', 'Tu',
    'Nu', 'Mai', 'Ne', 'Le', 'Intr', 'Cum', 'For', 'She', 'It', 'Esti',
	'This', 'That', 'How', 'Can', 'Must', 'Be', 'The', 'And', 'Do', 'So', 'Or', 'Ori',
	'Who', 'What', 'If', 'Of', 'On', 'We', 'They', 'Them', 'But', 'Where', 'By', 'An',
	'Mi', 'Made', 'My', 'Me', 'Vom', 'Voi', 'Ei', 'Cat', 'Ar', 'Putea', 'Poti', 'Sunteti', 'Inca', 'Still', 'Noi',
	'Ma', 'Dupa', 'After', 'Under', 'Sub', 'Niste', 'Some', 'Those', 'He', 'No', 'Too',
	'Fac', 'Made', 'Make', 'Cei', 'Most', 'Face', 'Pentru', 'Cat', 'Cate', 'Much', 'More', 'Many',
    'Sale', 'Tale', 'Tau', 'Has', 'Sunt', 'His', 'Yours', 'Only', 'As', 'Toate', 'All', 'Tot', 'Incat',
	'Which', 'Ti', 'Asa', 'Like', 'These', 'Because', 'Unor', 'Caci', 'Ele', 'Have', 'Haven', 'Te',
	'Cea', 'Else', 'Imi', 'Iti', 'Should', 'Could', 'Not', 'Even', 'Chiar', 'When', 'Ci', 'Ne', 'Ni',
	'Her', 'Our', 'Alta', 'Another', 'Other', 'Decat', 'Acelasi', 'Same', 'Au', 'Had', 'Haven', 'Hasn',
	'Alte', 'Alt', 'Others', 'Ceea', 'Cel', 'Cele', 'Alte', 'Despre', 'About', 'Acele', 'Acel', 'Acea',
	'Decit', 'With', 'Fata', 'Towards', 'Against', 'Cind', 'Dinspre', 'Fost', 'Been', 'Era', 'Daca',
	'Eu', 'El', 'Him', 'Ea', 'Will', 'Am', 'Cannot', 'Between', 'Cause', 'May', 'Couldn', 'destul', 'enough',
    'Destul', 'Enough', 'from', 'FROM', 'From', 'ia', 'Ia', 'IA', 'n', 'N', 'm', 'M'
]

LISTA_CUVINTE_LEGATURA = [normalize_word(word) for word in LISTA_CUVINTE_LEGATURA]

url = 'https://neculaifantanaru.com/foarte-rar-remarcam-ceea-ce-trebuie-cu-adevarat-sa-vedem.html'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extragem și analizăm metadatele
    title = soup.find('title').text if soup.find('title') else 'Titlu lipsă'
    meta_description = soup.find('meta', attrs={'name': 'description'})
    description = meta_description['content'] if meta_description else 'Descriere lipsă'

    # Procesarea conținutului articolului
    content = ''
    article_started = False

    for element in soup.descendants:
        if isinstance(element, Comment) and 'ARTICOL START' in element:
            article_started = True
        elif isinstance(element, Comment) and 'ARTICOL FINAL' in element:
            break
        elif article_started and element.name == 'p':
            content += ' ' + element.get_text()

    # Analiza conținutului
    words = re.findall(r'\w+', content.lower())
    words = [normalize_word(word) for word in words if word.isalpha()]
    filtered_words = [word for word in words if word not in LISTA_CUVINTE_LEGATURA]
    word_counts = Counter(filtered_words)

    most_common_words = word_counts.most_common(20)

    # Salvăm rezultatele într-un fișier
    with open(r'C:\Bebe\bebe.txt', 'w', encoding='utf-8') as file:
        file.write(f'Titlu: {title}\n\n')
        if len(title) < 30 or len(title) > 60:
            file.write('Sugestie: Lungimea titlului ar trebui să fie între 30 și 60 de caractere pentru optimizare SEO.\n--------\n\n')
        
        file.write(f'Descriere: {description}\n\n')
        if len(description) < 50 or len(description) > 160:
            file.write('Sugestie: Lungimea descrierii ar trebui să fie între 50 și 160 de caractere pentru optimizare SEO.\n--------\n')
        
        file.write('\nCele mai frecvente 10 cuvinte (excluzând cuvintele de legătură):\n\n')
        for word, count in most_common_words:
            file.write(f'{word}: {count}\n')

    print('Analiza a fost completată și salvată în fișierul bebe.txt.')
else:
    print('Nu am putut accesa URL-ul.')
