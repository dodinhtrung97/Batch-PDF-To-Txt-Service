import os
from Constants import DOWNLOAD_DIR, UPLOAD_DIR
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import Object

def pdf_to_text(host, bucket_name, object_name):
    """
    Convert pdf to txt file in Texts/ dir
    pdf_name and txt_name should come with their file extension
    Eg: Testfile.pdf, Testfile.txt
    """
    pdf_name = object_name + ".pdf"
    pdf_path = f"./{DOWNLOAD_DIR}/{pdf_name}"
    txt_name = object_name + ".txt"
    txt_path = f'./{UPLOAD_DIR}/{txt_name}'

    Object.download(host, bucket_name, pdf_name)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(pdf_path, 'rb')
    for page in PDFPage.get_pages(infile):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    text_file = open(txt_path, 'w', encoding="utf-8") # encoding fixes UnicodeDecodeError: 'charmap' codec can't decode...
    text_file.write(text)
    text_file.close()

    Object.upload(host, bucket_name, txt_name)

    #Clean-up
    os.remove(pdf_path)
    os.remove(txt_path)

    return "Success"