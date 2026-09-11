# 👁️ NetraMitra — Explainable AI for Diabetic Retinopathy Screening in Rural India

> **Smart India Hackathon (SIH) 2026**  
> **Problem Statement ID:** 26038 | **Organization:** MathWorks  
> **Category:** Software | **Theme:** MedTech / BioTech / HealthTech  
> **Tagline:** *Explainable retinal screening, closer to every community.*

NetraMitra is a comprehensive, clinically validated, and explainable AI-assisted Diabetic Retinopathy (DR) screening platform engineered specifically for primary healthcare centres and rural telemedicine workflows in India. Powered by a MATLAB deep learning & image analysis pipeline, FastAPI backend services with Google Gemini LLM explainability, a Next.js 15 web application, and scalable AWS ECS cloud deployment.

---

## 👥 Project Team & Contributors

- **BiBi Sufiya Shariff**
- **Mohammed Ayaan Adil Ahmed**
- **Likhitha Devan M**
- **Mohith B S**
- **Sinchana K A**
- **Thilak D G**

---

## 📌 Problem Statement Details (SIH 26038)

### Background
India has over **77 million diabetic adults** — the second highest globally. Diabetic Retinopathy (DR) affects ~18% of this population and is a leading cause of preventable blindness. Early screening can prevent up to **90% of vision loss**, but India faces an acute shortage of eye specialists (~1 ophthalmologist per 100,000 rural population), making mass manual screening infeasible. Existing AI solutions often function as "black boxes", lack clinical validation rigor, and fail under field conditions with variable fundus camera image quality.

### Core Objectives & System Deliverables

#### 1. Image Quality Assessment & Enhancement
- Automatic field of view, focus, and illumination evaluation for incoming fundus photos.
- Adaptive enhancement pipeline utilizing **CLAHE (Contrast Limited Adaptive Histogram Equalization)**, illumination normalization, and denoising.
- Rejection of ungradeable images with real-time recapture feedback for operators.

#### 2. Retinal Structure Segmentation & Feature Extraction
- Sub-pixel localization of Optic Disc and Fovea.
- Retinal blood vessel extraction, microaneurysm detection, exudate segmentation, hemorrhage classification, and neovascularization identification.

#### 3. DR Severity Grading & Performance Benchmarks
- International Clinical DR Severity Scale classification (Levels 0–4):
  - **Level 0**: No DR
  - **Level 1**: Mild NPDR
  - **Level 2**: Moderate NPDR
  - **Level 3**: Severe NPDR
  - **Level 4**: Proliferative DR (PDR)
- Achieves **>90% Sensitivity** and **>85% Specificity** for Referable DR (Level 2+).

#### 4. Clinically Meaningful Explainability
- **Grad-CAM Attention Maps**: Highlighting regions influencing deep learning predictions.
- **Lesion-Level Evidence**: Correlated against clinical diagnostic criteria.
- **LLM Narrative Reports**: Powered by Google Gemini 2.5 Flash-Lite to translate metrics into plain-language summaries, enabling ophthalmologists to validate screenings in **under 30 seconds**.

#### 5. Simulink Telemedicine Workflow Simulation
- Full discrete-event simulation of district-level screening programs serving **100,000+ patients annually**.
- Models image acquisition rates, rural bandwidth constraints, backend processing throughput, and specialist review capacity to optimize healthcare resource allocation.

---

## 🧰 Datasets & MATLAB Toolboxes

### Datasets Integrated & Validated Against
- **APTOS 2019 Blindness Detection** (Kaggle)
- **IDRiD** (Indian Diabetic Retinopathy Image Dataset)
- **DRIVE** (Digital Retinal Images for Vessel Extraction)
- **Messidor-2**

### MATLAB Toolboxes Employed
- Image Processing Toolbox
- Computer Vision Toolbox
- Deep Learning Toolbox
- Medical Imaging Toolbox
- Simulink
- Statistics and Machine Learning Toolbox

---

## 📐 System Architecture & Workflow

```
                                    +-----------------------------------+
                                    |       Next.js 15 Frontend         |
                                    |     (retinasathi-ai Web App)      |
                                    +-----------------+-----------------+
                                                      |
                                                      v HTTP / REST API
                                    +-----------------+-----------------+
                                    |        FastAPI Backend            |
                                    |  (app/main.py & app/routes/*)     |
                                    +--------+------------------+--------+
                                             |                  |
                       +---------------------+                  +----------------------+
                       v                                                               v
         +-------------+-------------+                                   +-------------+-------------+
         |    MATLAB Engine Service  |                                   |  Gemini LLM Explainability|
         |  (Compiled Runtime / Mock)|                                   |  (gemini-2.5-flash-lite)   |
         +---------------------------+                                   +---------------------------+
```

### End-to-End Clinical Flow
1. **Image Acquisition**: Frontline health worker / ASHA technician captures fundus photo with portable camera.
2. **Quality & Preprocessing**: System validates image quality, applies CLAHE contrast enhancement, and extracts green channel.
3. **MATLAB Inference**: Pre-trained deep learning model classifies DR grade (0–4) and generates Grad-CAM heatmap overlay.
4. **LLM Explanation**: Gemini 2.5 Flash-Lite translates findings into clinical risk assessment and patient-friendly guidance.
5. **Review Queue**: Scans requiring confirmation (Referable DR Level 2+) are queued for ophthalmologist sign-off (<30s review).

---

## 💻 Installation & Setup Guide

### Prerequisites
- **Node.js**: v18.0.0+
- **Python**: v3.9+
- **Docker**: Optional
- **MATLAB Runtime**: R2026a (v10.1) — *Optional (Mock mode available for dev)*

---

### 1. Backend Setup

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate | Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Set MATLAB_MODE=mock (or compiled) and GEMINI_API_KEY

# Start backend server
uvicorn app.main:app --reload --port 8000
```
Swagger API docs available at `http://localhost:8000/docs`.

---

### 2. Frontend Setup

```bash
cd retinasathi-ai

# Install packages
npm install

# Start Next.js dev server
npm run dev
```
Access UI at `http://localhost:3000`.

---

### 3. Docker & AWS Cloud Deployment

```bash
# Docker local build
cd backend
docker build -t netramitra-backend .

# AWS ECR Push & ECS Fargate Update
aws ecr get-login-password --region ap-south-1 --profile netramitra | docker login --username AWS --password-stdin 821421641429.dkr.ecr.ap-south-1.amazonaws.com
docker tag netramitra-backend:latest 821421641429.dkr.ecr.ap-south-1.amazonaws.com/netramitra-backend:latest
docker push 821421641429.dkr.ecr.ap-south-1.amazonaws.com/netramitra-backend:latest
aws ecs update-service --cluster netramitra-cluster --service netramitra-backend-service --force-new-deployment --profile netramitra --region ap-south-1
```

---

## 🗺 Application Navigation

| Page | Path | Description |
| :--- | :--- | :--- |
| **Overview** | `/dashboard` | Screening statistics, patient throughput, DR severity distribution |
| **New Screening** | `/screening/new` | Fundus image upload, quality validation, patient metadata |
| **Review Queue** | `/review` | Ophthalmologist verification queue with <30s triage workflow |
| **Patients** | `/patients` | Patient records, historical scans, longitudinal tracking |
| **Reports** | `/reports` | Exportable PDF diagnostic summaries |
| **Simulation** | `/simulation` | Telemedicine bandwidth & capacity planning (Simulink model interface) |
| **Help & Info** | `/help` | SIH Problem 26038 details, team credits, clinical notes |

---

## 📜 License & Credits

### Credits & Acknowledgments
- **Problem Statement Sponsor**: MathWorks (SIH 2026 - Problem Statement 26038)
- **Datasets**: APTOS 2019, IDRiD, DRIVE, Messidor-2
- **Development Team**: BiBi Sufiya Shariff, Mohammed Ayaan Adil Ahmed, Likhitha Devan M, Mohith B S, Sinchana K A, Thilak D G.

### License
This project is licensed under the **MIT License** — free for academic, research, and non-commercial clinical evaluation. See `LICENSE` for details.
