from pymilvus import MilvusClient
from utils.config import MILVUS_CONNECTION, MILVUS_API


# https://github.com/zilliztech/cloud-vectordb-examples/blob/master/python/hello_zilliz_vectordb.py

def get_milvus():
    return MilvusClient(uri=MILVUS_CONNECTION, token=MILVUS_API)
