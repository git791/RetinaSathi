from app.config import settings
from app.schemas import ExplanationRequest, ExplanationResponse
from google import genai
import logging

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = '''You are a downstream explanation assistant for an AI retinal screening prototype.

You do not perform the medical diagnosis.
You do not determine the DR grade.
You do not modify the model prediction.
You do not infer or invent retinal lesions that were not explicitly detected by a validated module.
You do not treat Grad-CAM as proof of a lesion.
You only explain the supplied AI result and the supplied model-attention visualization.
If evidence is insufficient, say so.
Use cautious language.
The final clinical decision belongs to a qualified healthcare professional.

Do NOT say things like 'The patient definitely has...', 'The highlighted region proves...', 'This is definitely a hemorrhage.', 'This confirms proliferative DR.', 'The patient does not need a doctor.'
Instead say: 'The model classified the image as...', 'The highlighted regions indicate areas that contributed to the model's prediction.'

Structure the response logically:
1. AI Screening Result
2. Why the AI produced this result
3. What the Grad-CAM shows (if applicable)
4. Referral meaning
5. Important limitation

Keep the explanation concise, around 100-180 words.
'''

class ExplanationService:
    def __init__(self):
        self.enabled = settings.gemini_explanation_enabled
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        
        self.client = None
        if self.enabled and self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def explain(self, request: ExplanationRequest) -> ExplanationResponse:
        if not self.enabled:
            return ExplanationResponse(
                success=True,
                explanation="[Development Mode] The model evaluated the image and provided a confidence score. Grad-CAM highlights attention. Consult a clinician.",
                model="mock-explanation"
            )

        if not self.client:
            return ExplanationResponse(
                success=False,
                error="AI explanation service unavailable"
            )
            
        if request.quality.status == 'UNGRADABLE' or not request.aiResult:
            return ExplanationResponse(
                success=True,
                explanation="The image was determined to be ungradable. The AI could not produce a reliable screening result. Please recapture the image.",
                model=self.model_name
            )

        prompt = f'''
Please explain this AI screening result:
Quality: {request.quality.status}
Predicted Level: {request.aiResult.predictedLevel}
Predicted Class: {request.aiResult.predictedClass}
Confidence: {request.aiResult.confidence:.2f}
Referable: {request.aiResult.referable}
Grad-CAM Available: {'Yes' if request.explainability and request.explainability.image else 'No'}
'''

        import time
        max_retries = 3
        base_delay = 1

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.2
                    )
                )
                
                return ExplanationResponse(
                    success=True,
                    explanation=response.text,
                    model=self.model_name
                )
            except Exception as e:
                logger.error(f"Gemini API Error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return ExplanationResponse(
                        success=False,
                        error="AI explanation service unavailable"
                    )
                time.sleep(base_delay * (2 ** attempt))
