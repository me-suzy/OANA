import os
import cv2
import PyPDF2

def crop_image(image_path, output_dir):
    # Citirea imaginii folosind OpenCV
    image = cv2.imread(image_path)

    # Identificarea textului și determinarea coordonatelor
    # (implementarea OCR poate fi adăugată aici, folosind Tesseract sau alte biblioteci)
    # Presupunând că coordonatele chenarului sunt cunoscute în avans

    # Croirea imaginii


    # In prima parte 800:4000 este VERTICAL
    # in a doua parte 100:1800 este orizontal (cu cat este mai mic numarul dinainte de :, cu atat este mai larga pagina)

    cropped_image = image[510:2800, 520:2800]   # 2800 este partea verticala, dar partea de jos a paginii # 520 partea orizontala din dreapta (aia mare neagra de la imprimanta)
    # cropped_image = image[800:4000, 100:1800]

    # Salvarea imaginii croite
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '_cropped.jpg')  # Specificăm extensia .jpg manual
    cv2.imwrite(output_path, cropped_image)
    print(f"Imaginea croită a fost salvată în: {output_path}")

def extract_images_from_pdf(pdf_path, output_dir):
    # Citirea fișierului PDF folosind PyPDF2
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)

        # Extragerea imaginilor din fiecare pagină și salvarea lor
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]

            images = page["/Resources"]["/XObject"].keys()
            for img_num, img_name in enumerate(images):
                img = page["/Resources"]["/XObject"][img_name]
                if img["/Subtype"] == "/Image":
                    img_data = img._data
                    img_file = open(os.path.join(output_dir, f"{page_num+1}_{img_num+1}.jpg"), "wb")
                    img_file.write(img_data)
                    img_file.close()

# Directorul de intrare și de ieșire
input_dir = r"d:\test"
output_dir = r"d:\test\1"

# Verificăm dacă directorul de ieșire există, altfel îl creăm
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Procesarea fișierelor JPEG
jpeg_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]
for file in jpeg_files:
    image_path = os.path.join(input_dir, file)
    crop_image(image_path, output_dir)

# Procesarea fișierelor PDF
pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
for file in pdf_files:
    pdf_path = os.path.join(input_dir, file)
    extract_images_from_pdf(pdf_path, output_dir)

'''
Sintaxa generală pentru croirea unei imagini este img[y1:y2, x1:x2], unde:

    x1 este coordonata de început pe axa orizontală (de la stânga la dreapta),
    x2 este coordonata de sfârșit pe axa orizontală,
    y1 este coordonata de început pe axa verticală (de sus în jos),
    y2 este coordonata de sfârșit pe axa verticală.

Prin urmare, pentru cropped_image = image[100:2800, 200:2800]:

    100:2800 pe axa verticală (y) înseamnă că se va începe croirea de la pixelul 100 de la partea de sus a imaginii și se va merge până la pixelul 2800, deci practic se extrage o porțiune din imagine care începe de la 100 de pixeli de la partea de sus și se întinde până la pixelul 2800 pe verticală.
    200:2800 pe axa orizontală (x) înseamnă că croirea începe de la pixelul 200 de la marginea stângă a imaginii și se extinde până la pixelul 2800 pe orizontală, deci se extrage o porțiune care începe de la 200 de pixeli de la marginea stângă și merge până la pixelul 2800.

Această operație de croire elimină părțile imaginii care sunt în afara intervalului specificat pentru fiecare axă. În acest exemplu, primele 100 de pixeli de la partea de sus a imaginii și primii 200 de pixeli de la marginea stângă nu vor fi incluși în imaginea croită. Similar, orice parte a imaginii care se află după pixelul 2800 atât pe axa verticală, cât și pe cea orizontală, va fi de asemenea eliminată.

Prin ajustarea acestor coordonate, poți controla cu precizie zona din imaginea originală pe care dorești să o extragi. Este un mod eficient de a elimina părțile nedorite ale unei imagini, cum ar fi marginile, sau de a focusa pe o anumită regiune de interes.
'''

