# ask PDF questions through command line!
import argparse
import time
import os
from dotenv import load_dotenv
from langchain_community.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

from parse_embedding import get_embedding_function

load_dotenv()

CHROMA_PATH = "db/chroma"

PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks.
You will answer in Chinese and your target user is people speak Tradition Chinese in Taiwan.
Use the following piece of retrieved context to answer the question. If you don't know the answer, just say '我不知道這個內容是什麼' 
Keep the answer concise

{context}

---

Answer the question in Chinese based on the above context: {question}
"""

def main():
   # Create CLI
   parser = argparse.ArgumentParser()
   parser.add_argument("query_text", type=str, help="The query text you want to ask about PDF.")
   args = parser.parse_args()
   query_text = args.query_text
   query_rag(query_text)


def query_rag(query_text: str):
   """
   Ask PDF and get response via LLM RAG\n
   But pay attention, there are many ways to construct RAG
   """
   embedding = get_embedding_function()
   db = Chroma(
      persist_directory=CHROMA_PATH,
      embedding_function=embedding
   )

   # Search the DB
   results = db.similarity_search_with_score(query=query_text, k=5)
   # retriever = db.as_retriever(k=5)

   context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
   prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
   prompt = prompt_template.format(context=context_text, question=query_text)
   print(prompt)

   model = Ollama(model="llama3:8b")
   # for chunk in model.stream(prompt):
   #    print(chunk, end="", flush=True)
   # chain = (
   #    {"context": retriever, "question": RunnablePassthrough()}
   #    | prompt
   #    | model
   #    | StrOutputParser()
   # )
   # response_text = chain.invoke(query_text)
   response_text = model.invoke(prompt)

   sources = [doc.metadata.get("id", None) for doc, _score in results]
   formated_response = f"Response: {response_text}\n Sources: {sources}"
   print(formated_response)
   # #for streaming
   # for word in response_text.split():
   #    yield word + " "
   #    time.sleep(0.05)
   return response_text

if __name__ == "__main__":
   main()
