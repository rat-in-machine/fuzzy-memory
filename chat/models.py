from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Pregunta del usuario")
    chat_id: Optional[UUID] = Field(
        default_factory=uuid4,
        description="Identificador opcional de la conversación"
    )

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Respuesta generada por el chatbot")
    chat_id: UUID