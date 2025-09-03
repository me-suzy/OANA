import os
import numpy as np
from skimage import exposure, io
from skimage.filters import unsharp_mask
from PIL import Image

# def process_images_in_folder(input_dir, output_dir, gamma_value=0.5, clip_limit_value=0.02, compression_quality=95): #varianta DEFAULT
def process_images_in_folder(input_dir, output_dir, gamma_value=1.00, clip_limit_value=0.001, compression_quality=95):  # varianta BEBE
# def process_images_in_folder(input_dir, output_dir, gamma_value=2.00, clip_limit_value=0.01, compression_quality=95):  # varianta BEBE 2
# def process_images_in_folder(input_dir, output_dir, gamma_value=2.00, clip_limit_value=0.01, compression_quality=95):  # varianta BEBE

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all image files in the input directory
    for file_name in os.listdir(input_dir):
        # Check for image file extensions
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)

            # Read the image
            image = io.imread(input_path, as_gray=True)

            # Apply gamma correction to brighten the image
            gamma_corrected = exposure.adjust_gamma(image, gamma=gamma_value)

            # Apply CLAHE to enhance contrast
            clahe_corrected = exposure.equalize_adapthist(gamma_corrected, clip_limit=clip_limit_value)

            # Apply unsharp masking to enhance edges
            unsharp_corrected = unsharp_mask(clahe_corrected, radius=1, amount=1)

            # Convert the image back to uint8
            final_image = np.clip(unsharp_corrected * 255, 0, 255).astype(np.uint8)

            # Convert to a PIL image for saving
            final_image_pil = Image.fromarray(final_image)

            # Save the final image with specified compression
            final_image_pil.save(output_path, quality=compression_quality)

# Specify the input and output directories
input_dir = 'd:/De pus pe FTP'
output_dir = 'd:/De pus pe FTP/1'

# Call the function to process the images
process_images_in_folder(input_dir, output_dir)
