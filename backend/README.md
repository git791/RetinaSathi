# RetinaSathi Backend

Python FastAPI backend serving as a bridge to the MATLAB screening engine.

## Setup

1. **Python Version**: Python 3.9+ recommended.
2. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Copy `.env.example` to `.env` and adjust variables.
   - `MATLAB_MODE=mock` (Currently only mock is supported as a placeholder)

## Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /health` - Health check status.
- `POST /api/v1/screenings` - Accepts multipart/form-data with an `image` field.

## MATLAB Integration Placeholder
Currently, `MATLAB_MODE` handles mock inferences. When configured for production compilation, the `MatlabScreeningService` will raise a controlled `503 MATLAB_NOT_CONNECTED` error until the MATLAB Compiler SDK package is integrated.
