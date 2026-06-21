import base64

def base64_to_bytes(image):
    if "," in image:
        image = image.split(",")[1]

    image = image.strip()
    image_bytes = base64.b64decode(image)
    return image_bytes