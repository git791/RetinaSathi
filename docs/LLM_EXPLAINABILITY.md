# LLM Explainability Module

## Overview
NetraMitra incorporates an optional LLM-based explanation module designed to translate the authoritative DR classification result and model attention (Grad-CAM) into patient-friendly, human-readable language.

**CRITICAL MEDICAL SAFETY:**
The LLM is strictly a downstream explanation assistant. It is NOT the classification engine. The current MVP does not perform explicit lesion segmentation for microaneurysms, exudates, hemorrhages, or neovascularization. Grad-CAM represents model attention and should not be interpreted as lesion segmentation.

## Architecture
- **Model:** gemini-2.5-flash-lite (Google Gemini 2.5 Flash-Lite)
- **SDK:** google-genai (Official Google GenAI Python SDK)
- **API Endpoint:** POST /api/v1/explain (FastAPI Backend)

## Why Gemini 2.5 Flash-Lite?
Gemini 2.5 Flash-Lite provides exceptionally fast, low-latency reasoning suitable for translating clinical metrics into conversational language. It is cost-effective and highly steerable with strict system instructions, making it ideal for downstream explanation without overriding the primary model.

## Safety Boundaries
The LLM operates under strict boundaries defined in the SYSTEM_INSTRUCTION:
1. It does NOT perform medical diagnosis.
2. It does NOT modify the underlying ResNet-50 prediction.
3. It does NOT invent specific retinal lesions based on Grad-CAM.
4. It only explains the supplied result and quality metrics.

## API Endpoint
**POST /api/v1/explain**

*Request:*
Accepts the existing screening result (predictedLevel, confidence, eferable) and quality status. Patient identifying information (PII) is intentionally omitted from the request schema.

*Response:*
`json
{
  "success": true,
  "explanation": "Human-readable explanation...",
  "model": "gemini-2.5-flash-lite",
  "disclaimer": "This explanation is generated from the AI screening output..."
}
`

## Environment Variables
Located in ackend/.env:

- GEMINI_API_KEY: (Required in production) The API key for Gemini. Never expose this to the frontend.
- GEMINI_MODEL: (Default: gemini-2.5-flash-lite)
- GEMINI_EXPLANATION_ENABLED: (Default: 	rue) Set to alse to use a deterministic mock explanation during development.

## Failure Behavior
If the Gemini API fails, times out, or the API key is missing, the core screening workflow continues uninterrupted. The frontend gracefully displays an unavailability message instead of the explanation, ensuring the clinical screening pipeline remains perfectly resilient.

## Production Setup (AWS)
Do NOT commit GEMINI_API_KEY or place it in the Dockerfile. It should be injected securely into the ECS Task Definition environment variables at runtime.

## Privacy Considerations
All patient data is stripped before the LLM request. The backend strictly constructs the prompt using deterministic variables (DR level, confidence, quality). No user-entered text, images, or metadata are forwarded to the LLM.
