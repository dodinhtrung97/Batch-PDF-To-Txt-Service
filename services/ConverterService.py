import os
from constant.Constants import DOWNLOAD_DIR, UPLOAD_DIR
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import Object

def pdf_to_text(host, bucket_name, object_name, pages=None):
    """
    Convert pdf to txt file in Texts/ dir
    pdf_name and txt_name should come with their file extension
    Eg: Testfile.pdf, Testfile.txt
    """
    pdf_name = object_name + ".pdf"
    txt_name = object_name + ".txt"

    Object.download(host, bucket_name, pdf_name)

    ## What is pagenums suppose to do?
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(f"./{DOWNLOAD_DIR}/{pdf_name}", 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close

    # create folder if folder does not yet exist
    if not os.path.exists(f'./{UPLOAD_DIR}'):
        os.makedirs(f'./{UPLOAD_DIR}')

    text_file = open(f'./{UPLOAD_DIR}/{txt_name}', 'w', encoding="utf-8") # encoding fixes UnicodeDecodeError: 'charmap' codec can't decode...
    text_file.write(text)
    ## Why remove space?
    #text = re.sub("\s\s+", " ", text)
    #text_file.write("%s" % text)
    text_file.close()

    Object.upload(host, bucket_name, txt_name)

    #Clean-up
    os.remove(f'./{UPLOAD_DIR}/{pdf_name}')
    os.remove(f'./{UPLOAD_DIR}/{txt_name}')

    return "Success"