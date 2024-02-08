from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
from reportlab.pdfgen import canvas
import os
from tkinter import Tk, filedialog

# Resize and Compress for 1 Image 
def resize_and_compress_image(image_path, resized_path, target_size=(620, 877), quality=85):
    img = Image.open(image_path)
    img = img.resize(target_size, Image.LANCZOS)

    # Check if the image has an alpha channel (transparency)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Save the resized and compressed image
    img.save(resized_path, quality=quality, optimize=True)

# Converting Image to PDF
def convert_image_to_pdf(image_path, resized_path=None):
    if resized_path:
        img = Image.open(resized_path)
    else:
        img = Image.open(image_path)

    pdf_path = os.path.splitext(image_path)[0] + ".pdf"

    with open(pdf_path, "wb") as pdf_file:
        c = canvas.Canvas(pdf_file)
        c.setPageSize((img.width, img.height))
        c.drawInlineImage(img, 0, 0, width=img.width, height=img.height)
        c.save()

    return pdf_path

# Resize and Compress Image consuming resize_and_compress_image function
def resize_and_compress_images(image_paths, output_folder, target_size=(620, 877), quality=85):
    converted_pdfs = []

    for image_path in image_paths:
        base_name = os.path.basename(image_path)
        resized_path = os.path.join(output_folder, "resized_" + base_name)

        resize_and_compress_image(image_path, resized_path, target_size, quality)
        converted_pdfs.append(convert_image_to_pdf(image_path, resized_path))

    return converted_pdfs

# merge pdf
def merge_pdfs(output_path, *pdf_paths):
    pdf_writer = PdfWriter()

    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

# local files input
def browse_files():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select Files")
    root.destroy()  # Close the Tk() window after file selection
    return file_paths

# main script
def main():
    # Ask the user to browse and select files
    files_to_merge = browse_files()

    if not files_to_merge:
        print("No files selected. Exiting.")
        return

    # Determine the output folder for both resized images and merged PDF
    output_folder = os.path.dirname(files_to_merge[0])
    resized_images_folder = os.path.join(output_folder, "resized_images")

    # Create the resized images folder
    os.makedirs(resized_images_folder, exist_ok=True)

    # Separate PDF and image files
    pdf_files = [file for file in files_to_merge if file.lower().endswith(".pdf")]
    image_files = [file for file in files_to_merge if file.lower().endswith((".jpg", ".png"))]

    # Resize and compress images to PDF
    converted_pdfs = resize_and_compress_images(image_files, resized_images_folder)

    # Determine the output path for the merged PDF
    output_pdf_path = os.path.join(output_folder, "merged_output.pdf")

    # Merge all PDFs
    merge_pdfs(output_pdf_path, *pdf_files, *converted_pdfs)

    print("PDFs merged successfully!")

# run main script
if __name__ == "__main__":
    main()
