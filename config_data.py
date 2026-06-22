import os
from dotenv import load_dotenv

load_dotenv()

md5_path = "./md5.text"

#chroma
collection_name = "rag"

persist_directory = "./chroma_db"

#spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n","\n","?",".",",","!","#","？","！","。","，"," ",""]
max_split_char_number = 1000        #文本分割的阈值

#
similarity_threshold = 1  #检索返回的结果数量

#
embedding_model_name = "text-embedding-v4"
chat_model_name = "deepseek-v4-flash"
api_key=os.getenv("api_key")
base_url="https://api.deepseek.com"

session_config = {
    "configurable":{
        "session_id":"user_001",
    }
}