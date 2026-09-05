from app.schemas import ScreeningResponse, QualityDetail, AiResult, Explainability
from app.utils.image_utils import encode_image_base64
from fastapi import HTTPException
import uuid
import io
import base64
from PIL import Image
import numpy as np

def array_to_base64(arr):
    if arr is None:
        return None
    try:
        # Attempt to convert whatever is passed (NumPy or MATLAB array) to standard NumPy
        arr = np.array(arr)
        
        # Squeeze in case of weird dimensions
        if arr.ndim > 3:
            arr = np.squeeze(arr)
            
        # Ensure uint8 for image saving
        if arr.dtype != np.uint8:
            if arr.max() <= 1.0:
                arr = (arr * 255).astype(np.uint8)
            else:
                arr = arr.astype(np.uint8)
                
        img = Image.fromarray(arr)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        encoded = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Error encoding array to base64: {e}")
        return None

class MatlabScreeningService:
    def __init__(self, mode: str):
        self.mode = mode
        self.pkg = None
        
        if self.mode == "compiled":
            try:
                import retinasathimodel
                print("Initializing MATLAB Compiler SDK package: retinasathimodel...")
                self.pkg = retinasathimodel.initialize()
                print("MATLAB Runtime initialized successfully.")
            except ImportError:
                raise RuntimeError("retinasathimodel is not installed. Did you `pip install` the compiled package?")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize MATLAB Runtime: {e}")

    def __del__(self):
        if self.pkg is not None:
            try:
                self.pkg.terminate()
            except Exception:
                pass

    def screen_image(self, image_bytes: bytes, patient_id: str = None) -> ScreeningResponse:
        """
        Executes the screening pipeline.
        In mock mode, returns deterministic mock output.
        In compiled mode, calls the MATLAB Python package.
        """
        if self.mode == "mock":
            # In mock mode, return a dummy structure so backend can be tested independently.
            return ScreeningResponse(
                screeningId=f"SCR-PY-{uuid.uuid4().hex[:6].upper()}",
                status="COMPLETED",
                quality=QualityDetail(
                    status="GOOD",
                    action="PROCEED",
                    message="Image quality is sufficient.",
                    score=1.0,
                    focusScore=1.0,
                    illuminationScore=1.0,
                    fovScore=1.0,
                    fovFraction=0.6
                ),
                processedImage=f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}",
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
                    image=f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                )
            )

        if self.mode == "compiled":
            if self.pkg is None:
                raise HTTPException(status_code=503, detail="MATLAB Runtime not initialized.")
            
            try:
                # Load image into numpy array
                img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                img_array = np.array(img)
                
                # Execute MATLAB compiled function
                result = self.pkg.retinaSathiScreen(img_array)
                
                # Handle return types securely based on Python dictionary or object mapping
                is_dict = isinstance(result, dict)
                
                def get_val(obj, key, default=None):
                    if is_dict:
                        return obj.get(key, default)
                    return getattr(obj, key, default)

                status = str(get_val(result, 'status', 'ERROR'))
                scr_id = str(get_val(result, 'screeningId', str(uuid.uuid4())))
                
                # If error, raise it
                if status == "ERROR":
                    errors = get_val(result, 'errors', [])
                    err_msg = ", ".join([str(e) for e in errors]) if isinstance(errors, list) else str(errors)
                    raise HTTPException(status_code=500, detail=f"MATLAB Screening Error: {err_msg}")
                
                # Parse Quality
                q_obj = get_val(result, 'quality')
                if not q_obj:
                    raise HTTPException(status_code=500, detail="Missing quality object in MATLAB result")
                
                quality = QualityDetail(
                    status=str(get_val(q_obj, 'status', 'UNGRADABLE')),
                    score=float(get_val(q_obj, 'score', 0.0)),
                    focusScore=float(get_val(q_obj, 'focusScore', 0.0)),
                    illuminationScore=float(get_val(q_obj, 'illuminationScore', 0.0)),
                    fovScore=float(get_val(q_obj, 'fovScore', 0.0)),
                    fovFraction=float(get_val(q_obj, 'fovFraction', 0.0)),
                    action=str(get_val(q_obj, 'action', 'RECAPTURE')),
                    message=str(get_val(q_obj, 'message', ''))
                )
                
                response = ScreeningResponse(
                    screeningId=scr_id,
                    status=status,
                    quality=quality
                )
                
                # UNGRADABLE checks
                if status == "UNGRADABLE":
                    # Do not attach AI results
                    return response
                    
                # Parse AI Result
                ai_obj = get_val(result, 'aiResult')
                if ai_obj:
                    response.aiResult = AiResult(
                        predictedLevel=int(get_val(ai_obj, 'predictedLevel', 0)),
                        predictedClass=str(get_val(ai_obj, 'predictedClass', '')),
                        confidence=float(get_val(ai_obj, 'confidence', 0.0)),
                        referable=bool(get_val(ai_obj, 'referable', False)),
                        referralStatus=str(get_val(ai_obj, 'referralStatus', 'NON-REFERABLE')),
                        recommendation=str(get_val(ai_obj, 'recommendation', ''))
                    )
                
                # Parse Processed Image
                processed = get_val(result, 'processedImage')
                if processed is not None:
                    response.processedImage = array_to_base64(processed)
                    
                # Parse Explainability
                exp_obj = get_val(result, 'explainability')
                if exp_obj:
                    exp_type = str(get_val(exp_obj, 'type', 'GRAD_CAM'))
                    exp_img = get_val(exp_obj, 'image')
                    if exp_img is not None:
                        response.explainability = Explainability(
                            type=exp_type,
                            image=array_to_base64(exp_img)
                        )
                
                return response
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"MATLAB Execution Failed: {str(e)}")
        
        # Fallback safeguard
        raise HTTPException(status_code=501, detail=f"Unsupported MATLAB_MODE: {self.mode}")
