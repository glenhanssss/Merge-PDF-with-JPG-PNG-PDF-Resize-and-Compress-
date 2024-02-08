# succes for saving file in memory
# succes for checking file if landscape or not

from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from tkinter import Tk, filedialog

# Resize and Compress for 1 Image 
def resize_and_compress_image(image_path, target_size=(620, 877), quality=85):
    img = Image.open(image_path)

    # Check if the image has an alpha channel (transparency)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Check if the image is landscape
    if img.width > img.height:
        img = img.resize((target_size[1], target_size[0]), Image.LANCZOS)
    else:
        img = img.resize(target_size, Image.LANCZOS)

    # Save the resized and compressed image to BytesIO
    output_buffer = BytesIO()
    img.save(output_buffer, format="JPEG", quality=quality, optimize=True)
    
    return output_buffer

# Converting Image to PDF
def convert_image_to_pdf(image_buffer):
    img = Image.open(image_buffer)

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.setPageSize((img.width, img.height))
    c.drawInlineImage(img, 0, 0, width=img.width, height=img.height)
    c.save()

    return pdf_buffer

# Resize and Compress Image consuming resize_and_compress_image function
def resize_and_compress_images(image_paths, target_size=(620, 877), quality=85):
    converted_pdfs = []

    for image_path in image_paths:
        image_buffer = resize_and_compress_image(image_path, target_size, quality)
        pdf_buffer = convert_image_to_pdf(image_buffer)
        converted_pdfs.append(pdf_buffer)

    return converted_pdfs

# merge pdf
def merge_pdfs(output_path, *pdf_buffers):
    pdf_writer = PdfWriter()

    for pdf_buffer in pdf_buffers:
        pdf_reader = PdfReader(pdf_buffer)
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

    # Separate PDF and image files
    pdf_files = [file for file in files_to_merge if file.lower().endswith(".pdf")]
    image_files = [file for file in files_to_merge if file.lower().endswith((".jpg", ".png"))]

    # Resize and compress images to PDF
    converted_pdfs = resize_and_compress_images(image_files)

    # Determine the output path for the merged PDF
    output_pdf_path = os.path.join(os.path.dirname(files_to_merge[0]), "merged_output.pdf")

    # Merge all PDFs
    merge_pdfs(output_pdf_path, *pdf_files, *converted_pdfs)

    print("PDFs merged successfully!")

# run main script
if __name__ == "__main__":
    main()
