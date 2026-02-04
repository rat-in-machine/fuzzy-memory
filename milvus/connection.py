from pymilvus import MilvusClient
from utils.config import MILVUS_CONNECTION, MILVUS_API

# milvus_client = MilvusClient(uri=MILVUS_CONNECTION, token=MILVUS_API)

def get_milvus():
    return MilvusClient(uri=MILVUS_CONNECTION, token=MILVUS_API)
# comprobante = milvus_client.has_collection("Pruebas")

# print(f"Conexion a la milvus {milvus_client} bien hecha, la coleccion de Pruebas está a {comprobante}")