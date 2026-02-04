import os

from dotenv import load_dotenv


load_dotenv()

OPENAI_API= os.getenv("OPENAI_API")
OPENAI_MODEL= os.getenv("OPENAI_MODELO")

NEXTAI_API= os.getenv("NEXTAI_API")
NEXTAI_USER= os.getenv("NEXTAI_USER")
NEXTAI_URL = os.getenv("NEXTAI_URL")
NEXTAI_MODEL = os.getenv("NEXTAI_MODELO")

MILVUS_CONNECTION =os.getenv("ZILLIZ_MILVUS_URL")