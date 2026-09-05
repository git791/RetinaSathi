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
   - `MATLAB_MODE=mock` (Safe developer default for deterministic output)
   - `MATLAB_MODE=compiled` (Requires `retinasathimodel` package installed)

## Compiled MATLAB Mode Installation

To run in compiled mode, you must install the MATLAB Compiler SDK package generated in Phase 9, and you MUST have MATLAB Runtime R2026a installed on your host OS.

1. Ensure MATLAB Runtime R2026a (v10.1) is installed.
2. Install the compiled package:
   ```bash
   pip install ../deployment/build
   # Or install via the generated .whl directly
   ```
3. Start the server with `MATLAB_MODE=compiled`.

## Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

## Testing

```bash
# Run tests in mock mode
pytest tests/

# Run tests in compiled mode (includes real APTOS image integration test)
# Note: Requires retinasathimodel installed in environment
$env:MATLAB_MODE="compiled"
pytest tests/
```

## Endpoints

- `GET /health` - Health check status.
- `POST /api/v1/screenings` - Accepts multipart/form-data with an `image` field.
