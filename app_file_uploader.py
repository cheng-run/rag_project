import streamlit as st
from knowledge_base import KnowledgeBaseService
import time


#添加网页的标题
st.title("知识库更新服务")

#文件上传框
uploader_file = st.file_uploader(
    "请上传文件",
    type=['txt'],
    accept_multiple_files=False,    #false表示仅接受一个文件的上传
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    #提取文件信息
    file_name = uploader_file.name,
    file_type = uploader_file.type,
    file_size = uploader_file.size / 1024,

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    text = uploader_file.getvalue().decode("utf-8")
    st.write(text)

    with st.spinner("载入中。。。"):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)
        
