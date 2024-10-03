from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, DirectoryLoader
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from datetime import datetime
import os
import argparse
import nest_asyncio
import pathlib

nest_asyncio.apply()

load_dotenv()

def parse_text(file):
   '''
   parse pdf text and tables using llamaparse
   '''
   parser = LlamaParse(result_type='markdown')
   document = parser.load_data(file)
   print(f'{file}: 處理完成')
   # extract filename as markdown file
   output_file = ''.join(file.split('/')[-1].split('.')[0])
   # with open(f'parsed_data/text/{output_file}.md', 'w') as f:
   #    f.write(document[0].text)
   return document

def parse_image(file):
   '''
   parse images using pypdf library
   '''
   reader = PdfReader(file)
   for i in range(len(reader.pages)):
      page = reader.pages[i]
      img = page.images
      for i in img:
         print(i.name)
         # 檔名：名稱_頁面
         file_prefix = datetime.now().strftime('%S%f') # random number
         with open('parsed_data/images/' + file_prefix + '_' + i.name, 'wb') as f:
            f.write(i.data)
   print(f'{file}: 圖片擷取完成')

def llamaparse_pdf_from_directory(file_path, output_path):
      '''
      parse pdf text and tables under file directory using llamaparse and save to markdown file

      Args:
         :param file_path: input file path  
         :type file_path: str
         :param output_path: output file path
         :type output_path: str
      '''
      parser = LlamaParse(result_type='markdown')
      try:
         for file in os.listdir(file_path):
            if '.pdf' not in file:
               continue
            
            filename = os.path.join(file_path, file)
            
            document = parser.load_data(filename)
            print(f'處理完成: {filename}')

            output_file = os.path.join(output_path, ''.join(filename.split('/')[-1].split('.')[0]))
            with open(f'{output_file}.md', 'w') as f:
               f.write(document[0].text)
      except Exception as e:
         print(e)

def llamaparse_pdf_from_filepath(file_path, output_path):
   """  
   Load document from single file path and parse to markdown

   Args:
      :param file_path: input file path
      :type file_path: str
      :param output_path: output file path
      :type output_path: str
   """
   pass


def load_documents_from_markdown(file_path="parsed_data/text"):
   """
   Load documents from parsed markdown during Llamaparse process  

   Args:
      :param file_path: file path/directory
      :type file_path: str
   """
   documents = []
   for filepath in pathlib.Path(file_path).glob('**/*'):
      file = str(filepath)
      loader_file = UnstructuredMarkdownLoader(file)
      document_file = loader_file.load()
      documents.append(document_file[0])
   return documents


if __name__ == '__main__':
   # result = load_documents_from_markdown()
   # print(result)
   llamaparse_pdf_from_directory('splits/updates', 'parsed_data/text')
