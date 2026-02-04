import os

from dotenv import load_dotenv

from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()

OPENAI_API= os.getenv("OPENAI_API_KEY")
OPENAI_MODEL= os.getenv("OPENAI_MODELO")

NEXTAI_API= os.getenv("NEXTAI_API_KEY")
NEXTAI_USER= os.getenv("NEXTAI_USER")
NEXTAI_URL = os.getenv("NEXTAI_URL")
NEXTAI_MODEL = os.getenv("NEXTAI_MODELO")

MILVUS_CONNECTION =os.getenv("ZILLIZ_MILVUS_URI")
MILVUS_USER= os.getenv("ZILLIZ_MILVUS_USER")
MILVUS_PASSWORD= os.getenv("ZILLIZ_MILVUS_PASSWORD")
MILVUS_API= os.getenv("ZILLIZ_MILVUS_API_KEY")

MODELO_EMBEDDING = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODELO"))