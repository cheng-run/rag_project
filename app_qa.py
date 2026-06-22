#streamlit run rag_project\app_qa.py
import streamlit as st
import time
from rag import RagService
import config_data as config
from dotenv import load_dotenv
import os

load_dotenv()

#标题
st.title("智能客服")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好有什么可以帮助你的？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

#在页面最下方提供用户的输入栏
prompt = st.chat_input()

if prompt:
    #在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    ai_res_list = []

    with st.spinner("思考中..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt},config.session_config)
        res = st.chat_message("assistant").write(res_stream)
        st.session_state["message"].append({"role":"assistant","content":res})