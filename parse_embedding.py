# parse and embedding
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings

def get_embedding_function():
   """  
   Get embedding models
   """
   #embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
   embeddings = OllamaEmbeddings(model="nomic-embed-text")
   return embeddings