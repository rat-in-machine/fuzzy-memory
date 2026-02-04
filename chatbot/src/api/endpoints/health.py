from fastapi import APIRouter
from ..core import HealthResponse
from config.settings import settings

router = APIRouter()

database_status = "operational"  # Puedes mejorar esto con lógica real

@router.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    return {
        "status": "operational",
        "version": "0.1.0",
        "components": {
            "api": "operational",
            "retriever": "pending (awaiting FAISS + MongoDB)",
            "llm": "pending (awaiting OpenAI integration)",
            "database": database_status
        }
    }

@router.get("/test", tags=["Debug"])
async def test_endpoint():
    return {"message": "Server is working"}
