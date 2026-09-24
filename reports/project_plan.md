# TCGA-KIRC Project Plan

## Target
- Project completion target: **2026-09-28**
- Daily work budget: **approximately 5 hours**
- Current status (2026-09-24): core modeling, frozen Test evaluation, and Clinical+RNA Global/Local XAI completed
- Current next stage: **remaining XAI → reusable inference pipeline → Molecular Twin/OOD → Streamlit**

## Final Scope by 2026-09-28

### Core survival modeling — completed
1. Clinical-only CoxNet
2. RNA-only CoxNet
3. Clinical + RNA CoxNet
4. Clinical + Hallmark CoxNet

### Evaluation — completed
- Harrell C-index
- Uno C
- 1-year and 3-year time-dependent AUC
- Brier score / Integrated Brier Score
- Calibration diagnostic
- Bootstrap confidence intervals and paired model comparison

### XAI / biological interpretation
- Clinical+RNA Global XAI — completed
- Clinical+RNA patient-level Local XAI — completed
- Clinical-only XAI
- Clinical+Hallmark pathway XAI
- Biological interpretation of selected RNA genes
- Reusable patient-level contribution output for inference/Streamlit

### Reusable patient inference
The final prototype will support **two input modes that share the same frozen inference engine**.

#### Mode A — Demo Patient
- Select a held-out TCGA-KIRC Test patient
- Load that patient's existing Clinical + RNA TPM profile
- Run the frozen inference pipeline
- Display risk, XAI, Molecular Twin, and OOD output
- This is the primary presentation/demo path

#### Mode B — New Patient
- Enter required Clinical variables
- Upload a compatible tumor RNA expression profile in TPM format
- Validate input schema and required genes
- Apply **Train-fitted preprocessing only**
- Run the same frozen Clinical+RNA CoxNet used in Demo Patient mode
- Display risk, XAI, Molecular Twin, and OOD output

The New Patient mode is a **research-prototype inference interface**, not a clinically validated deployment. It does not accept raw FASTQ; RNA input is assumed to have already been quantified to the required TPM/gene-ID schema.

### Molecular Twin
- Query patient → top-k similar **Train** patients
- Similarity computed in a predefined, standardized molecular/pathway representation
- Display similarity plus selected reference information such as PFI/event and clinical characteristics
- Retrieval is explanatory/reference functionality, not a separate prognosis model
- MVP only; no deep representation learning required

### OOD detection
- Train-distribution-based distance score
- Warning when an input is far from the training distribution
- Reference distribution and threshold determined without the final Test set
- OOD means limited similarity to the training distribution; it does not by itself mean the prediction is wrong

### Streamlit demo
Two input tabs/modes:
1. **Demo Patient** — choose a held-out TCGA Test patient
2. **New Patient** — Clinical input + compatible RNA TPM upload

Both modes call the same analysis pipeline:

```
Input
→ validation
→ frozen preprocessing
→ frozen Clinical+RNA CoxNet
→ PFI prognostic risk score / risk group
→ patient-level XAI
→ Molecular Twin
→ OOD warning
→ patient report
```

The app must clearly state that it is a research prototype and is not validated for clinical use.

## Scientific / Engineering Rules

- Patient-level analysis
- Primary endpoint: PFI
- Fixed primary modeling cohort: 529 patients
- Fixed split:
  - Train: 370
  - Validation: 79
  - Test: 80
- Stratification: pfi_event
- Random seed: 42
- Same split for all model families
- Train data only for:
  - low-expression filtering
  - scaling fit
  - feature selection
  - hyperparameter tuning
  - risk-group threshold when applicable
  - Molecular Twin reference construction
  - OOD reference distribution / threshold construction
- Validation used for model/hyperparameter selection where applicable
- Test remains held out from training/tuning
- No refitting preprocessing on a new patient
- New Patient mode must use saved Train-derived gene list, feature order, encoding, scaling, and frozen model parameters
- New Patient input must be validated before inference
- Raw FASTQ processing is outside the application scope
- External hospital TPM data may have platform/pipeline/batch differences; compatibility with the input schema does not constitute external clinical validation
- Unknown values/results must never be guessed
- QC issues take priority over the calendar

## Updated Schedule

### 2026-09-24 — XAI completion + inference preparation
**~5 hours**

1. Clinical-only XAI
2. Clinical+Hallmark pathway XAI
3. Biological interpretation of selected Clinical+RNA genes
4. Audit the exact frozen Clinical+RNA preprocessing sequence
5. Identify/save all Train-derived inference artifacts:
   - clinical encoding rules
   - retained/selected RNA genes
   - feature order
   - Train-fitted scaling parameters
   - frozen model parameters
   - risk-group threshold if used

**Completion criteria**
- Required XAI/biological interpretation is complete
- Exact preprocessing sequence for one-patient inference is documented
- No Test-derived preprocessing parameters are introduced
- Required inference artifacts are identified and reproducible

### 2026-09-25 — New-patient inference pipeline
**~5 hours — ⏳ core engineering day**

1. Define Clinical input schema
2. Define RNA TPM upload schema
3. Implement input validation
4. Implement reusable frozen preprocessing
5. Implement `predict_patient()` / equivalent patient-level inference
6. Connect patient-level XAI
7. Create at least one held-out Test patient as an example input
8. Run an inference parity test:
   - existing frozen Test risk score
   - new one-patient inference risk score
   - values must agree within numerical tolerance

**Completion criteria**
- A single Clinical + RNA TPM patient can be analyzed without notebook-wide batch processing
- Frozen preprocessing is reused rather than refit
- Example held-out Test patient reproduces the existing frozen prediction
- Invalid/missing input is detected before prediction

### 2026-09-26 — Molecular Twin + OOD
**~5 hours**

1. Freeze the representation used for patient similarity
2. Implement top-k Molecular Twin retrieval using Train patients as references
3. Return similarity and selected reference-patient information
4. Build Train-distribution-based OOD score
5. Determine OOD warning threshold without Test-set tuning
6. Wrap Twin and OOD as reusable functions
7. Connect both to the same patient inference output

**Completion criteria**
- Any valid query patient can retrieve top-k Train reference patients
- OOD score/warning is returned
- Test data are not used to define Twin/OOD settings or thresholds
- Demo Patient and New Patient inputs can use the same Twin/OOD functions

### 2026-09-27 — Streamlit MVP with two input modes
**~5 hours — ⏳ integration day**

1. App skeleton and artifact/model loading
2. **Demo Patient tab**
   - choose held-out TCGA Test patient
   - run complete analysis
3. **New Patient tab**
   - enter Clinical variables
   - upload RNA TPM file
   - validate and run complete analysis
4. Display:
   - PFI prognostic risk score / risk group
   - patient-level XAI
   - Molecular Twin results
   - OOD warning
5. Add research-use limitation notice
6. Basic UI/error handling

**Completion criteria**
- Demo Patient mode works end-to-end
- New Patient mode works end-to-end with a valid example file
- Both modes call the same frozen inference engine
- Demo can run without notebook interaction

### 2026-09-28 — Final validation + packaging
**~5 hours**

1. End-to-end regression/parity checks
2. Test invalid/missing RNA and Clinical inputs
3. Confirm model/preprocessing artifacts are frozen and reproducible
4. Final figures/tables and README
5. Add architecture/data-flow diagram
6. Document exact New Patient input format and example
7. Document limitations:
   - TCGA-based research cohort
   - no external clinical validation
   - TPM/pipeline/batch compatibility limitations
   - not for clinical use
8. Rehearse Demo Patient and New Patient presentation flows
9. Final Git/file/path checks

**Completion criteria**
- Both Streamlit modes run locally
- Existing frozen predictions are reproducible through the new inference path
- README explains data, methods, evaluation, XAI, Twin, OOD, input format, and limitations
- Repository is presentation-ready

## Priority if Schedule Slips

Do not drop:
1. Frozen-model scientific integrity / leakage-safe preprocessing
2. Existing four-model evaluation
3. XAI interpretation
4. Reusable one-patient inference pipeline
5. **Demo Patient Streamlit mode**

Reduce complexity in this order if needed:
1. UI styling
2. Extra plots
3. OOD sophistication
4. Molecular Twin sophistication
5. New Patient UI convenience features

The **New Patient inference architecture remains a target**, but if time becomes critical, preserve a working command/function-level New Patient inference path and prioritize a reliable Demo Patient Streamlit presentation.

## Final Deliverable

By 2026-09-28 the intended deliverable is:

**TCGA-KIRC Clinical/RNA PFI modeling and independent evaluation → XAI → frozen one-patient inference → Demo Patient + New Patient inputs → Molecular Twin → OOD warning → Streamlit research prototype**

### Final user flow

```
A. Demo Patient
Held-out TCGA Test patient selection
                 ↓
             Analyze
                 ↓
Risk → XAI → Molecular Twin → OOD

B. New Patient
Clinical input + compatible RNA TPM upload
                 ↓
        Input validation
                 ↓
             Analyze
                 ↓
Risk → XAI → Molecular Twin → OOD
```

Both paths use the **same frozen Clinical+RNA inference pipeline**.
