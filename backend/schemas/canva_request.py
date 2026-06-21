from pydantic import BaseModel

class CanvasRequest(BaseModel):
    image: str