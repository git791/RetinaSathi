# NetraMitra --- Antigravity Product & UI/UX Build Specification

## 1. Project Identity

### Recommended product name

**NetraMitra**

**Meaning:** "Sathi" means companion. The name positions the system as
an AI-assisted screening companion for frontline/rural healthcare
workflows rather than as an autonomous diagnostic authority.

### Recommended local project folder

`NetraMitra`

### Recommended GitHub repository

`netramitra-frontend`

### Recommended application title

**NetraMitra --- Explainable AI Retinal Screening**

### Recommended short tagline

> **Explainable retinal screening, closer to every community.**

### Naming research note

A web search was performed for several candidate names and obvious
project/repository collisions. Some attractive alternatives were
rejected because closely matching projects or organizations already
exist.

Examples: - **RetinaLens** --- already used by an AI
diabetic-retinopathy GitHub project. - **DrishtiAI / Drishti AI** ---
already used by multiple eye-health projects/products. - **DrishtiSetu**
--- already used by other projects. - **NetraSetu** --- already used by
an existing project. - **Netrika** --- already used by an
eye-care/public-health organization and an unrelated consulting company.

`NetraMitra` had no obvious exact-match project collision in the
searches performed and is therefore the recommended working name.

**Important:** this is a practical web-collision check, not a trademark,
company-name, package-name, or domain-name clearance. Before public
commercialization, perform formal trademark/domain/GitHub-owner checks.

------------------------------------------------------------------------

# 2. Product Intent

NetraMitra is an **explainable AI-assisted diabetic-retinopathy
screening platform** designed for resource-constrained and rural
healthcare workflows.

The product must communicate one central idea:

> **AI accelerates screening; humans remain responsible for clinical
> interpretation.**

The interface should therefore feel:

-   clinical
-   trustworthy
-   calm
-   modern
-   accessible
-   fast
-   evidence-oriented
-   human-in-the-loop

It must **not** look like: - a generic AI chatbot - a flashy consumer
health app - a gaming dashboard - a financial analytics dashboard - an
autonomous "AI doctor"

The visual language should make a clinician feel that the system is a
**clinical screening workstation**, not an AI experiment.

------------------------------------------------------------------------

# 3. Design Research → Product Principles

Recent healthcare-dashboard research emphasizes four major design
pillars:

1.  **Approach** --- involve users and design around their actual
    workflow.
2.  **Content** --- prioritize actionable information, data quality, and
    clear presentation.
3.  **Behavior** --- make interaction usable, accessible, and
    appropriate for different levels of digital literacy.
4.  **Adoption** --- integrate with existing workflows and reduce
    additional staff burden.

For NetraMitra, these translate into:

### Principle A --- Decision first

Every screening result page should answer these questions immediately:

1.  Is the image gradable?
2.  What DR level did the model predict?
3.  Is it referable?
4.  How confident is the model?
5.  Why did the model make this prediction?
6.  Does a clinician need to review it?

### Principle B --- Evidence beside the prediction

Do not hide explainability behind a separate page.

The retinal image and Grad-CAM explanation should appear directly beside
the prediction.

### Principle C --- Quality before AI

An unusable retinal image should never silently proceed to
classification.

The workflow should visibly communicate:

`Quality Check → Enhance / Recapture → Analyze`

### Principle D --- Human-in-the-loop

Never present the AI prediction as a final diagnosis.

Use language such as:

-   **AI Screening Result**
-   **Possible signs detected**
-   **Referable screening result**
-   **Requires clinical review**

Avoid:

-   "Diagnosis confirmed"
-   "Patient has DR"
-   "AI doctor"
-   "100% accurate"

### Principle E --- Reduce cognitive load

A clinician should be able to understand a screening result in **under
30 seconds**, matching the intended human-review workflow.

### Principle F --- Accessibility is part of clinical safety

WCAG 2.2 requires sufficient contrast and states that color should not
be the only mechanism used to communicate information.

Therefore: - status badges must include text/icons - red/green must
never be the only distinction - keyboard focus must be visible - text
must remain readable - controls must have clear labels - important
information must not depend on hover alone

------------------------------------------------------------------------

# 4. Target Users

## Primary user --- Screening operator

Examples: - rural health worker - technician - nurse - primary-care
worker

Needs: - very simple upload/acquisition workflow - clear image-quality
feedback - minimal technical terminology - fast result - obvious next
action

## Secondary user --- Ophthalmologist / clinician

Needs: - high-information result view - original and enhanced image -
Grad-CAM explanation - DR grade - confidence - referable/non-referable
classification - review/override capability - audit trail - report
generation

## Tertiary user --- Program administrator

Needs: - screening volume - referable-case counts - review backlog -
quality failure rate - throughput - district/resource utilization -
system performance

------------------------------------------------------------------------

# 5. Core User Workflow

## Workflow 1 --- New screening

``` text
Login
  ↓
Dashboard
  ↓
New Screening
  ↓
Patient / Screening ID
  ↓
Capture or Upload Fundus Image
  ↓
Image Quality Assessment
  ├── GOOD → Continue
  ├── BORDERLINE → Enhance → Continue
  └── UNGRADABLE → Recapture → Stop
  ↓
AI Screening
  ↓
DR Level 0–4
  ↓
Referable Decision
  ↓
Confidence
  ↓
Grad-CAM Explanation
  ↓
Human Review
  ├── Agree
  ├── Override
  └── Needs Specialist Review
  ↓
Screening Report
  ↓
Save / Export / Referral
```

------------------------------------------------------------------------

# 6. Primary Application Architecture

## Frontend

Recommended Antigravity application architecture:

``` text
React / Next.js-style frontend
│
├── App Shell
│   ├── Sidebar
│   ├── Top Navigation
│   ├── Breadcrumbs
│   └── User / System Status
│
├── Dashboard
├── New Screening
├── Screening Result
├── Review Queue
├── Patients
├── Screening History
├── Reports
├── Analytics
├── Simulation
└── Settings
```

## AI / MATLAB integration boundary

The frontend should be designed so that the AI engine can later be
connected through an API.

Conceptually:

``` text
Frontend
   │
   │ image
   ▼
Screening API
   │
   ▼
MATLAB / Compiled AI Pipeline
   │
   ├── Quality Assessment
   ├── Enhancement
   ├── DR Classification
   ├── Referable Decision
   └── Grad-CAM
   │
   ▼
Structured Screening Result
   │
   ▼
Frontend Result View
```

Current MATLAB MVP entry point:

``` matlab
summary = runScreening(image, netTrained);
```

The frontend architecture should therefore expect a structured response
similar to:

``` json
{
  "predictedLevel": 0,
  "predictedClass": "No DR",
  "confidence": 0.9782,
  "referralStatus": "NON-REFERABLE",
  "recommendation": "No immediate referral indicated based on automated screening.",
  "qualityStatus": "BORDERLINE",
  "qualityScore": 0.6149,
  "hasGradCAM": true
}
```

------------------------------------------------------------------------

# 7. Page Architecture

## Page 1 --- Login

### Goal

Fast, professional authentication.

### Layout

Centered authentication card with subtle retinal/medical visual
identity.

### Components

-   NetraMitra logo
-   email / username
-   password
-   sign in
-   remember device
-   system status
-   privacy/security notice

### Visual rule

Do not use a giant marketing hero.

This is a clinical application.

------------------------------------------------------------------------

# Page 2 --- Dashboard

### Goal

Give the clinician/operator an immediate operational overview.

### Top section

Greeting + current role.

Example:

> Good morning, Dr. Sharma\
> **12 screenings require review**

### KPI cards

-   Screenings today
-   Referable cases
-   Pending reviews
-   Ungradable images

### Main content

#### Screening activity

Simple line/bar visualization.

#### Referral distribution

Level 0--4 distribution.

#### Review queue

Show the highest-priority cases.

Each case should show:

``` text
Patient ID
Time
DR level
Confidence
Referral status
Review status
```

### Primary CTA

**+ New Screening**

This must be visually dominant.

------------------------------------------------------------------------

# Page 3 --- New Screening

This is one of the most important screens.

## Layout

Two-column workstation.

### Left

Image acquisition/upload area.

### Right

Screening context.

### Image upload area

Large drag-and-drop/click target:

> Upload retinal image

Secondary action:

> Capture image

Supported format indicators: - JPG - PNG

### Before processing

Show: - image dimensions - file size - image preview - acquisition
status

### Primary CTA

**Assess Image Quality**

Do not show classification controls before quality assessment.

------------------------------------------------------------------------

# Page 4 --- Image Quality Check

This page should visually explain the quality gate.

## Three quality indicators

### Focus

Show: - score - status - simple visual indicator

### Illumination

Show: - score - status

### Field of View

Show: - score - status

### Overall

Example:

``` text
IMAGE QUALITY
BORDERLINE

Enhancement recommended
```

### Actions

For GOOD:

**Continue to Screening**

For BORDERLINE:

**Enhance & Continue**

For UNGRADABLE:

**Recapture Image**

### Recapture guidance

Use practical messages:

-   Move closer to the eye
-   Keep the camera steady
-   Ensure the retina is centered
-   Avoid excessive glare
-   Ensure sufficient illumination

Do not expose raw algorithmic terminology to frontline users unless they
request technical details.

------------------------------------------------------------------------

# Page 5 --- Screening Analysis

Minimal screen.

Show:

``` text
Analyzing retinal image...

✓ Image quality assessed
✓ Image enhancement completed
● DR classification
○ Explainability
```

Use subtle progress states.

Avoid fake percentage progress if the backend cannot provide real
progress.

------------------------------------------------------------------------

# Page 6 --- Screening Result

This is the **hero screen of the entire project**.

The result should be understandable within seconds.

## Top result banner

Example:

``` text
AI SCREENING RESULT

NO DR

Level 0
Non-Referable

Confidence
97.82%
```

For Level 2+:

``` text
REFERABLE DR

Moderate DR
Level 2

Clinical review recommended
```

### Important

The system must visually distinguish:

-   AI prediction
-   referral recommendation
-   clinician decision

They are not the same thing.

------------------------------------------------------------------------

# 8. Result Page Layout

## Left: Retinal image

Large image viewer.

Controls:

-   Original
-   Enhanced
-   Grad-CAM

### Grad-CAM view

Overlay heatmap on the retinal image.

Provide:

**What the model focused on**

with a short explanation.

Example:

> Highlighted regions indicate areas that contributed more strongly to
> the model's prediction. This visualization supports review but is not
> a lesion diagnosis.

------------------------------------------------------------------------

# 9. Right: Clinical Summary

Use stacked cards.

## Card 1 --- DR Grade

``` text
Level 0
No DR
```

## Card 2 --- Confidence

``` text
97.82%
Model confidence
```

Avoid suggesting that confidence equals clinical certainty.

## Card 3 --- Referral

``` text
NON-REFERABLE
```

or

``` text
REFERABLE
Clinical review recommended
```

## Card 4 --- Image Quality

``` text
BORDERLINE
Enhanced before analysis
```

## Card 5 --- Recommendation

Clear next action.

------------------------------------------------------------------------

# 10. Human Review Panel

For clinician users:

``` text
AI Assessment
        ↓
Review
        ↓
[ Agree ] [ Override ] [ Needs Specialist Review ]
```

If override is selected:

Require:

``` text
Clinical assessment
Reason for override
Reviewer
Timestamp
```

This creates an audit trail.

------------------------------------------------------------------------

# 11. Review Queue

The queue should prioritize cases.

## Priority order

1.  Referable + low confidence
2.  Referable + high confidence
3.  Borderline quality
4.  Non-referable
5.  Completed

### Table columns

-   Case
-   Image quality
-   AI grade
-   Confidence
-   Referral
-   Review status
-   Time
-   Action

### Main action

**Review**

Avoid excessive table decoration.

------------------------------------------------------------------------

# 12. Patient / Screening History

## Patient profile

Show only the minimum information necessary for the prototype.

``` text
Patient ID
Screening date
Eye
Previous screening
Current result
Referral status
```

## Timeline

``` text
Previous screening
      ↓
Current screening
      ↓
Referral
      ↓
Review
```

Future versions can add longitudinal disease progression.

------------------------------------------------------------------------

# 13. Reports

Generate a clean clinical-style report.

## Report structure

### Header

NetraMitra

### Screening information

-   Patient ID
-   Screening ID
-   Date/time
-   Eye
-   Operator

### Image quality

-   Overall status
-   Quality score

### AI result

-   DR level
-   Class
-   Confidence
-   Referable status

### Explainability

Original image + Grad-CAM

### Recommendation

### Human review

-   reviewer
-   decision
-   timestamp

### Disclaimer

> AI screening results are intended to support qualified healthcare
> professionals and do not constitute a clinical diagnosis.

------------------------------------------------------------------------

# 14. Analytics

Analytics should be operational, not decorative.

## KPIs

-   total screenings
-   screenings/day
-   referable rate
-   ungradable rate
-   average review time
-   pending reviews

## Charts

Prefer: - simple bars - simple lines - compact distributions

Avoid: - 3D charts - excessive gradients - gauges everywhere -
decorative charts

------------------------------------------------------------------------

# 15. Simulink / Resource Simulation Page

This page connects the software product to the SIH problem statement.

## Purpose

Demonstrate whether a rural/district screening network can support:

**100,000+ patients/year**

## Metrics

-   image acquisition rate
-   network bandwidth
-   processing throughput
-   clinician review capacity
-   queue size
-   average processing time
-   resource utilization

## Visual

A clean system-flow diagram:

``` text
Village Screening Point
        ↓
Image Acquisition
        ↓
Network
        ↓
AI Processing
        ↓
Referable Queue
        ↓
Clinical Review
        ↓
Referral
```

Add simulation controls:

-   patients/day
-   image size
-   bandwidth
-   processing capacity
-   reviewers
-   review time

------------------------------------------------------------------------

# 16. Settings

Sections:

-   Profile
-   Role
-   Notification preferences
-   Model information
-   Screening thresholds
-   Audit log
-   Privacy
-   About NetraMitra

Do not expose dangerous model controls to ordinary operators.

------------------------------------------------------------------------

# 17. Navigation

Use a persistent left sidebar.

Recommended order:

``` text
NetraMitra

Overview
New Screening
Review Queue
Patients
History
Reports
Analytics
Simulation

────────────

Settings
Help
```

The sidebar should collapse on smaller screens.

------------------------------------------------------------------------

# 18. UI/UX Visual Direction

## Chosen direction

### **Clinical Calm + Technical Precision**

Think:

-   modern medical workstation
-   premium health-tech
-   subtle Indian accessibility context
-   clean clinical data visualization
-   trustworthy AI

Avoid a stereotypical hospital interface.

Avoid excessive: - blue gradients - glassmorphism - neon - floating
blobs - cartoon medical illustrations

------------------------------------------------------------------------

# 19. Color System

## Primary palette

### Deep Clinical Navy

`#12304A`

Use for: - primary navigation - headings - major actions - strong
emphasis

### Teal

`#0F766E`

Use for: - primary interactive states - positive/verified states -
active navigation accents - clinical highlights

### Soft Teal

`#CCFBF1`

Use for: - subtle information backgrounds - selected states -
non-critical success panels

### Clinical Sky

`#0EA5E9`

Use sparingly for: - secondary actions - information states - links -
charts

------------------------------------------------------------------------

## Neutral palette

### Background

`#F7FAFC`

### Surface

`#FFFFFF`

### Border

`#D9E2EC`

### Primary text

`#102A43`

### Secondary text

`#52606D`

### Muted text

`#7B8794`

------------------------------------------------------------------------

# 20. Clinical Status Colors

Status colors must always include text and/or an icon.

## Success / Non-referable

`#15803D`

Background:

`#DCFCE7`

## Warning / Borderline

`#B45309`

Background:

`#FEF3C7`

## Critical / Referable

`#B91C1C`

Background:

`#FEE2E2`

## Information

`#0369A1`

Background:

`#E0F2FE`

### Important accessibility rule

Never communicate:

``` text
green = safe
red = dangerous
```

by color alone.

Use:

``` text
✓ NON-REFERABLE
⚠ BORDERLINE
! REFERABLE
```

This follows the WCAG principle that color should not be the sole means
of conveying information.

------------------------------------------------------------------------

# 21. Typography

## Primary font

**Inter**

Use for: - navigation - buttons - KPI values - headings - labels - data
tables

Reason: - highly legible - modern - strong numeric readability - works
well for dense clinical interfaces

## Secondary font

**Source Sans 3**

Use for: - longer explanations - report content - clinical guidance -
supporting text

This creates a subtle distinction between **interface/data** and
**human-readable clinical content**.

## Type scale

``` text
Display: 32–40px
H1: 28–32px
H2: 22–24px
H3: 18–20px
Body: 14–16px
Small: 12–13px
KPI: 28–36px
```

Do not make everything huge.

Clinical dashboards need information density without sacrificing
readability.

------------------------------------------------------------------------

# 22. Spacing & Layout

Use an 8px spacing system.

``` text
4px   micro
8px   small
16px  default
24px  section
32px  major section
48px  page separation
```

Cards should generally use:

``` text
border-radius: 12px
padding: 20–24px
```

Avoid excessive rounded cards.

The application should feel structured rather than playful.

------------------------------------------------------------------------

# 23. Image Viewer Design

The retinal image is the most important visual asset.

Give it priority.

## Viewer

``` text
┌───────────────────────────────┐
│ Original | Enhanced | Grad-CAM│
├───────────────────────────────┤
│                               │
│       RETINAL IMAGE            │
│                               │
└───────────────────────────────┘
```

Controls should remain minimal.

Potential future controls: - zoom - pan - reset - fullscreen

Do not clutter the image with unnecessary controls.

------------------------------------------------------------------------

# 24. Grad-CAM UX

Grad-CAM is a major SIH differentiator.

The UI must explain it honestly.

### Label

**Model Attention**

rather than:

**Disease Location**

because the current Grad-CAM is classification explainability, not
lesion segmentation.

### Explanation

> The heatmap shows retinal regions that contributed more strongly to
> the model's prediction. It is an interpretability aid and should not
> be treated as a definitive lesion map.

This distinction is important because the current MVP uses Grad-CAM and
does not yet provide validated lesion-level segmentation.

------------------------------------------------------------------------

# 25. Confidence UX

Never use confidence as a giant "certainty" meter.

Instead:

``` text
Model confidence
97.82%

High model confidence
```

For lower confidence:

``` text
Model confidence
61.20%

Review recommended
```

Future calibration should replace raw confidence with calibrated
probabilities once implemented.

------------------------------------------------------------------------

# 26. Quality Gate UX

The quality workflow should be extremely clear.

### GOOD

``` text
✓ Image ready
Quality acceptable
```

### BORDERLINE

``` text
⚠ Enhancement applied
Image quality is borderline
```

### UNGRADABLE

``` text
! Image needs recapture
The image is not suitable for automated screening.
```

Do not expose technical scores unless the clinician opens "Technical
details".

------------------------------------------------------------------------

# 27. Responsive Design

The primary target is desktop/laptop because ophthalmologists and
administrators will use the clinical dashboard.

Still support:

-   tablet
-   smaller laptop
-   mobile operator workflow

## Desktop

Two-column clinical workstation.

## Tablet

Stack image and summary vertically.

## Mobile

Prioritize:

1.  patient
2.  quality status
3.  DR result
4.  referral
5.  next action

Hide secondary analytics until requested.

Responsive design must **reallocate attention**, not merely shrink the
desktop UI.

------------------------------------------------------------------------

# 28. Interaction Design

Use restrained animation.

Allowed: - fade - slide - progress transitions - image loading - result
reveal

Avoid: - bouncing cards - spinning decorative elements - excessive
parallax - flashy gradients - animated backgrounds

Medical software should feel stable.

------------------------------------------------------------------------

# 29. Microcopy

Prefer:

**"Analyze Image"**

over:

**"Run AI"**

Prefer:

**"AI Screening Result"**

over:

**"AI Diagnosis"**

Prefer:

**"Clinical review recommended"**

over:

**"Doctor required"**

Prefer:

**"Image needs recapture"**

over:

**"Invalid image"**

Prefer:

**"Possible signs detected"**

over:

**"Disease detected"**

------------------------------------------------------------------------

# 30. Empty States

Every empty state should tell the user what to do next.

Example:

``` text
No pending reviews

All current screening cases have been reviewed.

[View Screening History]
```

------------------------------------------------------------------------

# 31. Loading States

Never show blank screens.

Use skeleton loaders for: - dashboard cards - tables - patient history

For AI processing, use explicit stages:

``` text
Checking image quality
        ✓
Enhancing image
        ✓
Classifying DR
        ●
Preparing explanation
        ○
```

------------------------------------------------------------------------

# 32. Error Handling

Errors must be actionable.

Bad:

> Error 500

Good:

> We couldn't process this image. Please try uploading the image again.

For quality failures:

> The retinal field is not sufficiently visible. Please recapture the
> image with the retina centered in the frame.

------------------------------------------------------------------------

# 33. Trust & Safety UI

Every result page should contain a subtle but visible disclaimer:

> **Clinical support only:** AI screening results do not replace
> evaluation by a qualified healthcare professional.

For referable results, emphasize:

> **Clinical review recommended.**

Never imply autonomous diagnosis.

------------------------------------------------------------------------

# 34. Technical Architecture

Recommended conceptual structure:

``` text
netramitra-frontend/
│
├── app/
│   ├── dashboard/
│   ├── screening/
│   ├── review/
│   ├── patients/
│   ├── history/
│   ├── reports/
│   ├── analytics/
│   ├── simulation/
│   └── settings/
│
├── components/
│   ├── ui/
│   ├── clinical/
│   ├── retinal-viewer/
│   ├── quality/
│   ├── screening/
│   ├── charts/
│   └── layout/
│
├── services/
│   ├── screening-api/
│   ├── patient-api/
│   └── report-api/
│
├── types/
│   ├── screening.ts
│   ├── patient.ts
│   └── report.ts
│
├── mock/
│   └── demo-data/
│
├── public/
│   ├── images/
│   └── icons/
│
└── docs/
    ├── architecture.md
    └── ui-ux-spec.md
```

The exact framework can be selected by Antigravity based on the current
project environment, but the architecture should preserve this
separation.

------------------------------------------------------------------------

# 35. Demo Mode

The SIH demo must work even if the MATLAB backend is not running.

Implement a controlled demo mode.

``` text
Demo Mode
   ↓
Preloaded retinal image
   ↓
Mock / recorded screening response
   ↓
Full result UI
```

The demo should visibly distinguish demonstration data from live
inference.

This prevents a backend/network failure from destroying the
presentation.

------------------------------------------------------------------------

# 36. MVP Scope for Antigravity

## Must work

### 1. Dashboard

-   KPIs
-   recent cases
-   new screening CTA

### 2. New Screening

-   upload image
-   preview
-   quality status

### 3. Screening

-   processing state

### 4. Result

-   retinal image
-   enhanced image
-   Grad-CAM
-   DR Level 0--4
-   confidence
-   referable status
-   recommendation
-   disclaimer

### 5. Review

-   agree
-   override
-   notes

### 6. History

-   previous screening records

### 7. Report

-   structured screening report

------------------------------------------------------------------------

# 37. Advanced Features

Implement after the core experience is stable:

-   lesion segmentation
-   vessel segmentation
-   optic-disc/fovea localization
-   microaneurysm evidence
-   exudate evidence
-   hemorrhage evidence
-   neovascularization
-   probability calibration
-   external validation
-   advanced audit trail
-   Simulink integration
-   district resource simulation
-   offline-first workflow
-   multilingual operator mode

Do not block the first working frontend on these features.

------------------------------------------------------------------------

# 38. SIH Demonstration Flow

The ideal 2--3 minute demo:

``` text
1. Dashboard
      ↓
2. New Screening
      ↓
3. Upload retinal image
      ↓
4. Quality Gate
      ↓
5. Borderline image → Enhancement
      ↓
6. AI classification
      ↓
7. DR Level + confidence
      ↓
8. Referable decision
      ↓
9. Grad-CAM explanation
      ↓
10. Human review
      ↓
11. Generate report
      ↓
12. Show analytics / scale simulation
```

The judges should immediately see:

**Quality → AI → Explainability → Human Review → Referral → Scale**

That is the core story of the product.

------------------------------------------------------------------------

# 39. What Makes NetraMitra Different

The product should not be positioned merely as:

> "AI detects diabetic retinopathy."

Instead:

> **NetraMitra is an explainable, quality-aware, human-in-the-loop
> screening workflow designed to extend retinal screening capacity into
> resource-constrained settings.**

The differentiators are:

1.  Image quality gate
2.  Adaptive enhancement
3.  5-level DR grading
4.  Referable DR decision
5.  Explainability
6.  Human review
7.  Structured report
8.  Rural workflow
9.  Scale/resource simulation

------------------------------------------------------------------------

# 40. Implementation Rules for Antigravity

### Rule 1

Build the **clinical workflow before decorative features**.

### Rule 2

Use reusable components.

### Rule 3

Do not hardcode clinical result logic throughout the UI.

### Rule 4

Keep AI output types strongly structured.

### Rule 5

Separate: - AI prediction - referral recommendation - clinician decision

### Rule 6

Never claim clinical validation that has not been performed.

### Rule 7

Never claim the current model meets the SIH sensitivity target until the
validation work actually demonstrates it.

### Rule 8

Use realistic demo data and label it clearly.

### Rule 9

Maintain accessibility.

### Rule 10

Keep the result screen fast and understandable.

------------------------------------------------------------------------

# 41. Final Design System

``` text
PRODUCT
NetraMitra

TAGLINE
Explainable retinal screening, closer to every community.

STYLE
Clinical Calm + Technical Precision

PRIMARY
#12304A  Deep Clinical Navy
#0F766E  Teal

SECONDARY
#0EA5E9  Clinical Sky
#CCFBF1  Soft Teal

NEUTRALS
#F7FAFC  Background
#FFFFFF  Surface
#D9E2EC  Border
#102A43  Primary Text
#52606D  Secondary Text
#7B8794  Muted Text

STATUS
#15803D  Non-referable / Success
#B45309  Borderline / Warning
#B91C1C  Referable / Critical
#0369A1  Information

FONT
Inter
Source Sans 3

RADIUS
12px cards

SPACING
8px base system

DESIGN LANGUAGE
Clean
Clinical
Accessible
Calm
Evidence-oriented
Human-in-the-loop
```

------------------------------------------------------------------------

# 42. Research Basis

The UI/UX direction is informed by:

-   **J Med Internet Research, 2026 --- Design Practices for Data
    Dashboards in Health Care:** emphasizes user involvement, actionable
    content/data quality, usability/accessibility, and workflow
    integration.
-   **W3C WCAG 2.2:** requires adequate contrast and says color should
    not be the sole method of communicating information.
-   **Healthcare UX trend research, 2026:** highlights
    accessibility-first design and trust/safety as increasingly
    important in healthcare interfaces.
-   **Ophthalmology dashboard research:** supports user-centered
    development with ophthalmologist involvement.
-   Existing diabetic-retinopathy screening interfaces commonly
    emphasize clear risk/result presentation and clinical decision
    support rather than autonomous diagnosis.

------------------------------------------------------------------------

# 43. Build Acceptance Criteria

The Antigravity implementation is considered successful when a
first-time user can:

1.  understand what NetraMitra does within 5 seconds
2.  start a screening within 10 seconds
3.  upload a retinal image
4.  understand image quality status
5.  understand the DR prediction
6.  identify whether referral is recommended
7.  see the Grad-CAM explanation
8.  understand that the result is AI-assisted, not a diagnosis
9.  complete a clinician review
10. generate a screening report

The complete primary workflow should feel like:

> **Upload → Check → Analyze → Explain → Review → Report**

and not:

> **Upload → complicated AI dashboard → hunt for the answer**

------------------------------------------------------------------------

# 44. Antigravity Build Instruction

Use this document as the **product-level source of truth** for the
frontend.

Do not begin by creating every page at once.

Build in this order:

``` text
App Shell
↓
Dashboard
↓
New Screening
↓
Quality Gate
↓
Result / Grad-CAM
↓
Human Review
↓
History
↓
Reports
↓
Analytics
↓
Simulation
```

The first implementation milestone is the **complete screening
journey**, not the complete application.

Once that journey works visually and interactively, expand the
surrounding modules.
