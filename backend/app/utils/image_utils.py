import base64

SUPPORTED_FORMATS = ['jpeg', 'png', 'jpg']

def validate_image_format(content: bytes) -> bool:
    if len(content) < 8:
        return False
    # Check PNG magic number
    if content.startswith(b'\x89PNG\r\n\x1a\n'):
        return True
    # Check JPEG magic number (FF D8 FF)
    if content.startswith(b'\xff\xd8\xff'):
        return True
    return False

def encode_image_base64(content: bytes, img_format: str = "jpeg") -> str:
    encoded = base64.b64encode(content).decode('utf-8')
    return f"data:image/{img_format};base64,{encoded}"
