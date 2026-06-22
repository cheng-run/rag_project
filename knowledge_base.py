import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

#检查传入的md5字符串是否已经存在
def check_md5(md5_str:str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip()     #处理字符串前后的空格和回车
            if line == md5_str:
                return True     #已经处理过
            
        return False

#将传入的md5字符串记录到文件内保存
def save_md5(md5_str:str):
    with open(config.md5_path,'a',encoding='utf-8') as f:
        f.write(md5_str + '\n')

#将字符串转化为md5
def get_string_md5(input_str:str,encoding= 'utf-8'):
    #将字符串转换为MD5字符串
    str_bytes = input_str.encode(encoding=encoding)
    md5_obj = hashlib.md5()     #得到md5对象
    md5_obj.update(str_bytes)   #更新内容
    md5_hex = md5_obj.hexdigest()   #得到md5的十六进制字符串

    return md5_hex

class KnowledgeBaseService(object):

    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,     #数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,     #数据库本地存储文件夹
        )     #向量存储的实例chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,     #分割后的文本段的最大长度
            chunk_overlap = config.chunk_overlap,       #连续文本段之间的字段重叠数量
            separators=config.separators,       #自然段落的划分符号
            length_function=len,        #用python自带的len函数来做长度的统计依据
        )    #文本分割器的对象

    #将传入的字符串进行向量化，存入向量数据库中
    def upload_by_str(self,data:str,filename):
        #先拿到传入字符串的md5值
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "跳过，内容已经存在知识库中"
        
        if len(data) > config.max_split_char_number:
            knowledge_chunks:list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"Runnnnnnn"
        }

        #内容加载到向量库中
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)

        return "成功，内容已经载入向量库"

#if __name__=='__main__':
