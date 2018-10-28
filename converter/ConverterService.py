import os
from constant import Constants
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re

def pdf_to_text(pdf_name, txt_name):
    """
    pdf_name and txt_name should come with their file extension
    Eg: Testfile.pdf, Testfile.txt
    """
    pages = None
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(pdf_name, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close

    # create folder if folder does not yet exist
    if not os.path.exists(f'./{Constants.UPLOAD_DIR}'):
        os.makedirs(f'./{Constants.UPLOAD_DIR}')

    text_file = open(f'./{Constants.UPLOAD_DIR}/{txt_name}', 'w')
    text = re.sub("\s\s+", " ", text)
    text_file.write("%s" % text)
    text_file.close()

    return os.path.abspath(txt_name)

pdf_to_text("C://Users//Trung//Desktop//java_developer_cv_template.pdf", "Test.txt")