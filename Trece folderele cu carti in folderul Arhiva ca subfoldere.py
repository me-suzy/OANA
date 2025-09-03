import os
import shutil

# Calea către directorul de lucru
working_dir = r"d:/doc"

# Parcurgem toate fișierele și directoarele din directorul de lucru
for item in os.listdir(working_dir):
    item_path = os.path.join(working_dir, item)
    
    # Verificăm dacă este un director
    if os.path.isdir(item_path):
        
        # Verificăm dacă numele directorului conține virgulă
        if ',' in item:
            # Dacă da, înseamnă că este un director format din 2 sau 3 cuvinte
            first_letter = item.split(',')[0][0].upper()
            
            # Calea către directorul destinație
            dest_dir = os.path.join(working_dir, first_letter)
            
            # Verificăm dacă directorul destinație există, altfel îl creăm
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            # Mutăm directorul în directorul destinație
            shutil.move(item_path, os.path.join(dest_dir, item))
            print(f"Directorul {item} a fost mutat în {dest_dir}")