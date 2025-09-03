import os
import cv2
import PyPDF2

def crop_image(image_path, output_dir, page_num):
    # Citirea imaginii folosind OpenCV
    image = cv2.imread(image_path)
    # Alegerea setului de coordonate de cropare în funcție de numărul paginii
    if page_num % 2 == 0:  # Pagini pare

        coords = (800, 4000, 100, 1800)  # In prima parte 800:4000 este VERTICAL  in a doua parte 100:1800 este orizontal

    else:  # Pagini impare

        coords = (1000, 4200, 300, 2000)  # In prima parte 800:4000 este VERTICAL  in a doua parte 100:1800 este orizontal

    # Croirea imaginii folosind coordonatele selectate
    cropped_image = image[coords[0]:coords[1], coords[2]:coords[3]]
    # Salvarea imaginii croite
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '_cropped.jpg')
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
    # Extragere numărului paginii din numele fișierului
    # Presupunem că numele fișierului are forma 'paginaX.jpg' unde X este numărul paginii
    # Trebuie să ajustezi acest cod pentru a se potrivi cu formatul numelui fișierelor tale
    page_num = int(''.join(filter(str.isdigit, file)))
    crop_image(image_path, output_dir, page_num)

# Procesarea fișierelor PDF
pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
for file in pdf_files:
    pdf_path = os.path.join(input_dir, file)
    extract_images_from_pdf(pdf_path, output_dir)
