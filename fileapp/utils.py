import fitz 
import ebooklib.epub
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import tempfile
import os, textwrap
from PIL import Image


def pdf_epub(uploaded_file):
    reader = PdfReader(uploaded_file)
    epub_path = tempfile.mktemp(suffix='.epub')
    book = ebooklib.epub.EpubBook()
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        content = page.extract_text()
        chapter = ebooklib.epub.EpubHtml(title=f'Page {page_num + 1}', file_name=f'page_{page_num + 1}.xhtml', lang='en')
        chapter.content = f'<h1>Page {page_num + 1}</h1><p>{content}</p>'
        book.add_item(chapter)
    book.spine = ['nav'] + book.items
    ebooklib.epub.write_epub(epub_path, book)
    return epub_path


def pdf_txt(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text_content = ""
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        page_text = page.get_text()
        
        # Clean the text: This is a basic example to remove extra whitespaces
        cleaned_text = ' '.join(page_text.split())
        
        # Append cleaned text for the page to the main content
        text_content += cleaned_text + "\n"
    
    text_file_name = uploaded_file.name.replace('.pdf', '.txt')
    with open(text_file_name, 'w') as text_file:
        text_file.write(text_content)



def pdf_txt(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text_content = ""
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        page_text = page.get_text()
        cleaned_text = ' '.join(page_text.split())
        text_content += cleaned_text + "\n"

    text_file_name = uploaded_file.name.replace('.pdf', '.txt')
    full_path = os.path.join(os.getcwd(), text_file_name)
    with open(full_path, 'w') as text_file:
        text_file.write(text_content)
    return full_path 


def image_pdf(uploaded_file):
    image_file_path = uploaded_file.name
    with open(image_file_path, 'wb+') as image_file:
        for chunk in uploaded_file.chunks():
            image_file.write(chunk)
    image = Image.open(image_file_path)
    pdf_file_path = image_file_path.replace('.png', '.pdf').replace('.jpeg', '.pdf')
    image.convert('RGB').save(pdf_file_path)
    return pdf_file_path


def png_jpeg(uploaded_file):
    image_file_path = uploaded_file.name
    with open(image_file_path, 'wb+') as image_file:
        for chunk in uploaded_file.chunks():
            image_file.write(chunk)
    image = Image.open(image_file_path)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    jpeg_file_path = image_file_path.replace('.png', '.jpg')
    image.save(jpeg_file_path, 'JPEG')
    return jpeg_file_path


def jpeg_png(uploaded_file):
    image_file_path = uploaded_file.name
    with open(image_file_path, 'wb+') as image_file:
        for chunk in uploaded_file.chunks():
            image_file.write(chunk)
    image = Image.open(image_file_path)
    png_file_path = image_file_path.replace('.jpg', '.png')
    image.save(png_file_path, 'PNG')
    return png_file_path
