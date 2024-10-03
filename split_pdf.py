from llama_index.core import VectorStoreIndex
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from PyPDF2 import PdfReader, PdfWriter
import os

# split large PDFs and store in output path
def split_pdfs(pdf_path, page_extract, output_dir):
   """
   Split large PDF into smaller PDFs
   """
   with open(pdf_path, 'rb') as f:
      reader = PdfReader(f)
      if not os.path.exists(output_dir):
         os.makedirs(output_dir)
      
      for title, (start, end) in page_extract.items():
         writer = PdfWriter()
         
         for page in range(start - 1, end):
            writer.add_page(reader.pages[page])
         
         # save split PDF
         output_path = os.path.join(output_dir, f'{title}.pdf')
         with open(output_path, 'wb') as output_file:
            writer.write(output_file)
         
         print(f'已創建完成: {output_path}')
         

if __name__ == '__main__':
   # page_extract = {
   #    '竹東SOP_chapter1': [7, 12], 
   #    '竹東SOP_chapter2': [13, 22],
   #    '竹東SOP_chapter3': [23, 131],
   #    '竹東SOP_chapter4': [132, 151],
   #    '竹東SOP_附錄': [152, 162]
   # }
   # output_dir = 'splits'
   # pdf_path = 'data/竹東SOP.pdf'
   # split_pdfs(pdf_path, page_extract, output_dir)

   page_extract = {
      '竹東SMP_part1': [1, 7],
      '竹東SMP_part2': [8, 28],
      '竹東SMP_part3': [29, 50],
      '竹東SMP_part4': [51, 159],
      '竹東SMP_part5': [160, 217]
   }
   output_dir = 'splits'
   pdf_path = 'data/竹東SMP.pdf'
   split_pdfs(pdf_path, page_extract, output_dir)
