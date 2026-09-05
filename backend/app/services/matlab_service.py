from app.schemas import ScreeningResponse, QualityDetail, AiResult, Explainability
from app.utils.image_utils import encode_image_base64
from fastapi import HTTPException
import uuid

class MatlabScreeningService:
    def __init__(self, mode: str):
        self.mode = mode

    def screen_image(self, image_bytes: bytes, patient_id: str = None) -> ScreeningResponse:
        """
        Placeholder adapter for MATLAB screening engine.
        Currently raises an error indicating MATLAB is not connected,
        acting as a controlled seam for future compilation.
        """
        # The prompt requires raising an error if it's the Matlab placeholder 
        # but also to keep it runnable without MATLAB.
        # We'll fail cleanly with MATLAB_NOT_CONNECTED if configured for production.
        if self.mode != "mock":
            raise HTTPException(
                status_code=503, 
                detail="MATLAB_NOT_CONNECTED"
            )
        
        # In mock mode, return a dummy structure so backend can be tested independently.
        return ScreeningResponse(
            screeningId=f"SCR-PY-{uuid.uuid4().hex[:6].upper()}",
            status="COMPLETED",
            quality=QualityDetail(
                status="GOOD",
                action="PROCEED",
                message="Image quality is sufficient."
            ),
            processedImage=encode_image_base64(image_bytes),
            aiResult=AiResult(
                predictedLevel=2,
                predictedClass="Moderate DR",
                confidence=0.85,
                referable=True,
                referralStatus="REFERABLE",
                recommendation="Refer to ophthalmologist"
            ),
            explainability=Explainability(
                type="GRAD_CAM",
                image=encode_image_base64(image_bytes)
            )
        )
