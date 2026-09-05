from pydantic import BaseModel
from typing import Optional, Literal

class QualityDetail(BaseModel):
    status: Literal['GOOD', 'BORDERLINE', 'UNGRADABLE']
    score: float = 0.0
    focusScore: float = 0.0
    illuminationScore: float = 0.0
    fovScore: float = 0.0
    fovFraction: float = 0.0
    action: Literal['PROCEED', 'ENHANCE', 'RECAPTURE']
    message: str = ""

class AiResult(BaseModel):
    predictedLevel: int
    predictedClass: str
    confidence: float
    referable: bool
    referralStatus: Literal['REFERABLE', 'NON-REFERABLE']
    recommendation: str

class Explainability(BaseModel):
    type: str = "GRAD_CAM"
    image: str

class ScreeningResponse(BaseModel):
    screeningId: str
    status: Literal['COMPLETED', 'UNGRADABLE', 'ERROR']
    quality: QualityDetail
    processedImage: Optional[str] = None
    aiResult: Optional[AiResult] = None
    explainability: Optional[Explainability] = None
