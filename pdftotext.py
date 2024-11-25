import os
import subprocess
import PyPDF2
from io import BytesIO
from typing import List
import txt_reader

def pdf_to_txt_from_bytes(pdf_bytes, pdf_path_file, txt_path_file):
    
    pdf_path_file
    with open(pdf_path_file, 'wb') as f:
        f.write(pdf_bytes)
    
    os.system('pdftotext -enc UTF-8 -layout ' + pdf_path_file + ' ' + txt_path_file)
    
    txtreader = txt_reader.TxtReader()
    txtreader.read(txt_path_file)
    print(txtreader.mongodic1)
    return txtreader.name, txtreader.mongodic1, txtreader.mongodic2