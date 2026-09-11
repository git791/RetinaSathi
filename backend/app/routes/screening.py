from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas import ScreeningResponse, ExplanationRequest, ExplanationResponse
from app.services.matlab_service import MatlabScreeningService
from app.services.explanation_service import ExplanationService
from app.config import settings
from app.utils.image_utils import validate_image_format

router = APIRouter()
matlab_service = MatlabScreeningService(mode=settings.matlab_mode)
explanation_service = ExplanationService()

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

@router.post("/api/v1/explain", response_model=ExplanationResponse)
def explain_result(request: ExplanationRequest):
    return explanation_service.explain(request)
