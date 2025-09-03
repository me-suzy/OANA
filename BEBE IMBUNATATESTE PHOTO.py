import os
from PIL import Image
import numpy as np

def adjust_image_contrast(input_path, output_path):
    try:
        # Incarca imaginea
        image = Image.open(input_path)

        # Converteste imaginea in grayscale daca nu este deja
        if image.mode != 'L':
            image = image.convert('L')

        # Obtine valorile pixelilor
        pixels = np.array(image)

        # Calculeaza percentila 2% si 98%
        # p2, p98 = np.percentile(pixels, [2, 98])
        p2, p98 = np.percentile(pixels, [1, 98]) # varianta bebe

        # Normalizeaza valorile pixelilor la intervalul 0-255
        pixels_normalized = np.clip((pixels - p2) * 255 / (p98 - p2), 0, 255).astype(np.uint8)

        # Creeaza o imagine noua din valorile pixelilor ajustati
        adjusted_image = Image.fromarray(pixels_normalized)

        # Salveaza imaginea ajustata
        adjusted_image.save(output_path)
        print(f"Imaginea a fost procesata si salvata la: {output_path}")

    except Exception as e:
        print(f"A aparut o eroare la procesarea imaginii {input_path}: {e}")

# Calea folderului cu imaginile originale si calea folderului de iesire
input_folder = 'd:/De pus pe FTP'
output_folder = 'd:/De pus pe FTP/1'

# Asigura-te ca folderul de iesire exista
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Proceseaza toate imaginile din folderul de intrare
for image_file in os.listdir(input_folder):
    # Verifica daca este un fisier imagine
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)
        adjust_image_contrast(input_path, output_path)
