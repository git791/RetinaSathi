import base64

SUPPORTED_FORMATS = ['jpeg', 'png', 'jpg', 'webp']

def validate_image_format(content: bytes) -> bool:
    if len(content) < 12:
        return False
    # Check PNG magic number
    if content.startswith(b'\x89PNG\r\n\x1a\n'):
        return True
    # Check JPEG magic number (FF D8 FF)
    if content.startswith(b'\xff\xd8\xff'):
        return True
    # Check WebP magic number (RIFF ... WEBP)
    if content.startswith(b'RIFF') and content[8:12] == b'WEBP':
        return True
    return False

def encode_image_base64(content: bytes, img_format: str = "jpeg") -> str:
    encoded = base64.b64encode(content).decode('utf-8')
    return f"data:image/{img_format};base64,{encoded}"

