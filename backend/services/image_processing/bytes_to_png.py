from PIL import Image
import io

def bytes_to_png(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return image