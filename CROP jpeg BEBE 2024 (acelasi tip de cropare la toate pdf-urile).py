import os
import cv2
import PyPDF2
import numpy as np

def crop_image(image, output_path, crop_coords):
    print(output_path, "Dimensiuni:", image.shape)  # Folosim output_path pentru a identifica imaginea
    cropped_image = image[crop_coords[0]:crop_coords[1], crop_coords[2]:crop_coords[3]]
    cv2.imwrite(output_path, cropped_image)
    print(f"Imaginea croită a fost salvată în: {output_path}")


def extract_and_crop_images_from_pdf(pdf_path, output_dir, crop_coords):
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            images = page["/Resources"]["/XObject"].keys()

            for img_num, img_name in enumerate(images):
                img = page["/Resources"]["/XObject"][img_name]
                if img["/Subtype"] == "/Image":
                    # Actualizare pentru a folosi get_data în loc de getData
                    img_data = img.get_data()  # Aceasta este linia actualizată
                    img_array = np.frombuffer(img_data, dtype=np.uint8)
                    img_cv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    print(os.path.join(output_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{page_num+1}_{img_num+1}_cropped.jpg"), "Dimensiuni:", img_cv.shape)  # Afișează dimensiunile aici
                    img_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{page_num+1}_{img_num+1}_cropped.jpg"
                    img_file_path = os.path.join(output_dir, img_filename)
                    crop_image(img_cv, img_file_path, crop_coords)


# Coordonatele de croire (y_start, y_end, x_start, x_end)
crop_coords = (100, 2800, 500, 2600)  # 100 partea de sus, 2800 este partea de jos, 500 este partea laterala stanga, 2600 este laterala dreapta,
# crop_coords = (0, 4000, 120, 2800)
#crop_coords = (0, 1890, 230, 1261)

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
    image = cv2.imread(image_path)
    output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(image_path))[0] + '_cropped.jpg')
    crop_image(image, output_path, crop_coords)

# Procesarea fișierelor PDF
pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
for file in pdf_files:
    pdf_path = os.path.join(input_dir, file)
    extract_and_crop_images_from_pdf(pdf_path, output_dir, crop_coords)
