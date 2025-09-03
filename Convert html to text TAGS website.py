import os
import re
import html

def extrage_text_html(director_sursa, director_destinatie, fisier_final):
    if not os.path.exists(director_destinatie):
        os.makedirs(director_destinatie)

    for fisier in os.listdir(director_sursa):
        if fisier.endswith(".html"):
            cale_fisier = os.path.join(director_sursa, fisier)
            with open(cale_fisier, 'r', encoding='utf-8') as f:
                continut = f.read()

            # Verifică dacă fișierul conține linia specificată pentru a fi ignorat
            if "<div class=\"blog-box heading-space-half\">" in continut:
                print(f"Fișierul {fisier} conține linia specificată și va fi ignorat.")
                continue  # Sari peste acest fișier

            print(f"Procesez fișierul: {fisier}")

            # Decodifică entitățile HTML
            continut = html.unescape(continut)

            # Extrage textul din h1 folosind expresii regulate
            h1_match = re.search(r'<h1 class="custom-h1" itemprop="name">(.*?)</h1>', continut)
            h1_text = h1_match.group(1) if h1_match else 'Titlu lipsă'

            # Extrage textul din secțiunea articol
            articol_match = re.search(r'<!-- ARTICOL START -->([\s\S]*?)<!-- ARTICOL FINAL -->', continut)
            articol_text = articol_match.group(1) if articol_match else 'Conținut articol lipsă'
            articol_text = re.sub(r'<[^>]+>', '', articol_text)  # Elimină toate tagurile HTML

            continut_final = f"{h1_text}\n\n{articol_text}"

            nume_fisier_destinatie = os.path.splitext(fisier)[0] + '.txt'
            with open(os.path.join(director_destinatie, nume_fisier_destinatie), 'w', encoding='utf-8') as f_dest:
                f_dest.write(continut_final)
            print(f"Fișierul {fisier} a fost procesat și salvat ca {nume_fisier_destinatie}.")

    # Unește toate fișierele txt
    print("Unesc toate fișierele txt într-un singur fișier...")
    with open(os.path.join(director_destinatie, fisier_final), 'w', encoding='utf-8') as f_final:
        for fisier in sorted(os.listdir(director_destinatie)):
            if fisier.endswith(".txt"):
                with open(os.path.join(director_destinatie, fisier), 'r', encoding='utf-8') as f:
                    f_final.write(f.read() + '\n\n')
    print(f"Conversia tuturor fișierelor în {fisier_final} a fost finalizată cu succes.")

# Apelează funcția cu calea către directorul sursă și destinatie
extrage_text_html('e:\\Carte\\BB\\17 - Site Leadership\\Principal 2022\\ro\\', 'D:\\Test-Fisier', 'fisier_final.txt')
