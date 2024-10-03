from unstructured.partition.pdf import partition_pdf
import pathlib
import os

def parse_image_unstructured(file_path, output_path):
   """
   Extract images using unstructured library  

   Args:
      :param file_path: pdf file path
      :type file_path: str
      :param output_path: path to store extracted images
      :type output_path: str
   """
   # filename = "data/竹東SOP.pdf"
   # output_path = 'parsed_data/images'
   try:
      for filepath in pathlib.Path(file_path).glob("**/*"):
         filename = str(filepath)

         # parse images for each pdf
         elements = partition_pdf(
            filename=filename,
            extract_image_block_output_dir=output_path,
            strategy='hi_res',
            extract_images_in_pdf=True,
            infer_table_structure=True,
         )

         element_dict = [ele.to_dict() for ele in elements]
         unique_type = set()
         for item in element_dict:
            unique_type.add(item)

         print(f'解析結果：{unique_type}')

      print('擷取圖片完成')
   except Exception as e:
      print('Error: ', e)
      raise e

