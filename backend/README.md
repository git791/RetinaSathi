# 👁️ NetraMitra Backend

> **Smart India Hackathon (SIH) 2026** — Problem Statement ID 26038 (MathWorks)  
> Python FastAPI backend bridging the MATLAB screening engine, Gemini LLM explainability, and Next.js frontend.

## 👥 Project Team & Contributors

- **BiBi Sufiya Shariff**
- **Mohammed Ayaan Adil Ahmed**
- **Likhitha Devan M**
- **Mohith B S**
- **Sinchana K A**
- **Thilak D G**

---

## ⚡ Setup & Quick Start

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
   Copy `.env.example` to `.env` and set:
   - `MATLAB_MODE=mock` (Safe developer default)
   - `MATLAB_MODE=compiled` (Requires MATLAB Runtime R2026a)
   - `GEMINI_API_KEY=your_gemini_key`

## 🚀 Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

---

## 📖 Comprehensive Documentation

For complete problem statement specifications, deep learning pipeline details, dataset references (APTOS 2019, IDRiD, DRIVE, Messidor-2), frontend setup, and AWS deployment instructions, please view the [Main Project README](../README.md).

---

## 📜 License & Credits
Developed under the **MIT License** for **Smart India Hackathon 2026** (Sponsored by MathWorks).
