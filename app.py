# frontend app 
import streamlit as st
import sys
from langchain_community.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from query_data import query_rag

st.set_page_config(
   page_title='對話機器人for上水',
   page_icon="🦈",
   layout='centered',
   initial_sidebar_state = 'expanded',
   menu_items = {
      'About': ''':rainbow[對話機器人解決工作人員的疑問]'''
   }
)

st.title('🤖上水對話機器人')
st.caption('對話機器人使用Llama🦙')

if 'messages' not in st.session_state:
   st.session_state['messages'] = [{'role': 'assistant', 'content': '你好，有什麼可以為你回答的？'}]

for msg in st.session_state['messages']:
   if msg['role'] == 'assistant':
      st.chat_message('assistant', avatar='🦙').write(msg['content'])
   else:
      st.chat_message('user', avatar='🧸').write(msg['content'])

if prompt := st.chat_input():
   try:
      st.session_state['messages'].append({'role': 'user', 'content': prompt})
      st.chat_message('user', avatar='🧸').write(prompt)
      response = query_rag(prompt)
      # #for streaming in frontend
      # with st.chat_message('assistant', avatar='🦙'):
      #    response = st.write_stream(query_rag(prompt))
      st.chat_message('assistant', avatar='🦙').markdown(response)
      st.session_state['messages'].append({'role': 'assistant', 'content': response})
   except:
      st.error(sys.exc_info[:])