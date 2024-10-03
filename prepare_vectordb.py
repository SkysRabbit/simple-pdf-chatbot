from langchain_community.vectorstores.chroma import Chroma
from parse_embedding import get_embedding_function
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, DirectoryLoader
import os
import shutil
import argparse
import pathlib

# because the source pdf is relatively large, consider to split manually to multiple pdfs
# then extract documents

CHROMA_PATH = "db/chroma"
DATA_PATH = "data"

def main():
   # check if the database should be cleared (using the --clear flag)
   parser = argparse.ArgumentParser()
   parser.add_argument("--reset", action="store_true", help="Reset the database.")
   args = parser.parse_args()
   if args.reset:
      print("✨ Clearing Database")
      clear_chroma_db()
   
   # Create or update the data store, for small documents for now
   # will also support for larger documents
   # document = load_small_documents()
   document = load_documents_from_markdown() # llamaparse
   chunks = splits_documents(document)
   add_to_chroma(chunks)


def load_small_documents(data_path):
   """
   Load documents from data_path directory  
      Args:  
         :param data_path: document directory
         :type data_path: str
   """
   document_loader = PyPDFDirectoryLoader(data_path)
   print(document_loader.load())
   return document_loader.load()

def load_documents_from_markdown(file_path="parsed_data/text"):
   """
   Load documents from parsed markdown during Llamaparse process  

   Args:
      file_path(str): file path/directory
   """
   documents = []
   for filepath in pathlib.Path(file_path).glob('**/*'):
      file = str(filepath)
      loader_file = UnstructuredMarkdownLoader(file)
      document_file = loader_file.load()
      documents.append(document_file[0])
   return documents

def splits_documents(documents: list[Document]):
   text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=800,
      chunk_overlap=80,
      length_function=len,
      is_separator_regex=False,
   )
   return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
   db = Chroma(
      persist_directory=CHROMA_PATH,
      embedding_function=get_embedding_function()
   )

   # Calculate page IDs
   chunks_with_ids = calculate_chunk_ids(chunks)
   
   # Add or update the documents
   existing_itmes = db.get(include=[])
   existing_ids = set(existing_itmes["ids"])
   print(f"Number of existing documens in DB: {len(existing_ids)}")

   # Only add documents that don't exist in the DB
   new_chunks = []
   for chunk in chunks_with_ids:
      if chunk.metadata["id"] not in existing_ids:
         new_chunks.append(chunk)
   
   if len(new_chunks):
      print(f"Adding new documents: {len(new_chunks)}")
      new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
      db.add_documents(new_chunks, ids=new_chunk_ids)
      db.persist()
   else:
      print("✅ No new documents to add")
  

def calculate_chunk_ids(chunks):
   """
   This will create unique identified IDs like "data/pdf name:6:2",
   For larger pdf also applys
   Page source:Page number:chunk index
   """

   last_page_id = None
   current_chunk_index = 0

   for chunk in chunks:
      source = chunk.metadata.get("source")
      page = chunk.metadata.get("page")
      # there is no page attribute in markdown file
      if 'page' not in chunk.metadata:
         page = 1
      current_page_id = f"{source}:{page}"

      # If the page ID is the same as the last one, increment the index
      if current_page_id == last_page_id:
         current_chunk_index += 1
      else:
         current_chunk_index = 0

      chunk_id = f"{current_page_id}:{current_chunk_index}"
      last_page_id = current_page_id

      chunk.metadata["id"] = chunk_id
   
   return chunks


def clear_chroma_db():
   if os.path.exists(CHROMA_PATH):
      shutil.rmtree(CHROMA_PATH)
      print('清除資料庫完成')

if __name__ == "__main__":
   main()