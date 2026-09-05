from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas import ScreeningResponse
from app.services.matlab_service import MatlabScreeningService
from app.config import settings
from app.utils.image_utils import validate_image_format

router = APIRouter()
matlab_service = MatlabScreeningService(mode=settings.matlab_mode)

@router.post("/api/v1/screenings", response_model=ScreeningResponse)
async def create_screening(
    image: UploadFile = File(...),
    patient_id: str = Form(None),
    eye: str = Form(None)
):
    contents = await image.read()
    
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")
    
    if not validate_image_format(contents):
        raise HTTPException(status_code=400, detail="Unsupported image format. Use JPEG or PNG.")

    try:
        response = matlab_service.screen_image(contents, patient_id)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal screening processing failure.")
