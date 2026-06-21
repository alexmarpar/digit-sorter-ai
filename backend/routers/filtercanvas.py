from fastapi import APIRouter
from schemas.canva_request import CanvasRequest
from services.image_processing.base_64_to_bytes import base64_to_bytes
from services.image_processing.bytes_to_png import bytes_to_png
from services.ai_processing.main import image_processing

router = APIRouter(prefix="/filtercanvas",
                    tags=["aicanvas"],
                    responses={404: {"message": "Not founded"}})


@router.post("/")
async def products(data: CanvasRequest):
    image = data.image
   
    decofied_image = bytes_to_png(base64_to_bytes(image))
    result = image_processing(decofied_image)
    
    return result