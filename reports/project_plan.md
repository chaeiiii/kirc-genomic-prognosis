# TCGA-KIRC Project Plan

## Target
- Project completion target: **2026-09-28**
- Daily work budget: **approximately 5 hours**
- Current baseline: Train / Validation / Test split completed and QC passed
- Current next stage: **Train-only leakage-safe RNA preprocessing**

## Final Scope by 2026-09-28

The project is planned to include all of the following components.

### Core survival modeling
1. Clinical-only survival model
2. RNA-only survival model
3. Clinical + RNA survival model
4. Clinical + Hallmark pathway survival model

### Evaluation
- C-index
- 1-year and 3-year time-dependent AUC
- Integrated Brier Score (IBS)
- Risk-group visualization such as Kaplan-Meier curves when appropriate

### Interpretation
- Patient-level risk score
- Important clinical / molecular features
- Hallmark pathway-level interpretation

### Molecular Twin
- Query patient → top-k similar patients
- Similarity computed in a predefined standardized molecular/pathway feature space
- Display similarity, PFI/event, and selected clinical characteristics
- MVP implementation only; no deep representation learning required

### OOD detection
- Train-distribution-based distance score
- Warning for patients far from the training distribution
- Threshold determined without using the final Test set
- MVP distance-based implementation only

### Streamlit demo
- Patient selection / input
- Predicted risk score and risk group
- Important features/pathways
- Molecular Twin results
- OOD warning
- Simple survival/risk visualization

## Scientific Rules

- Patient-level analysis
- Primary endpoint: PFI
- Fixed primary modeling cohort: 529 patients
- Fixed split:
  - Train: 370
  - Validation: 79
  - Test: 80
- Stratification: pfi_event
- Random seed: 42
- The same split must be used for all four model families
- Train data only for:
  - low-expression filtering
  - scaling fit
  - feature selection
  - hyperparameter tuning
  - OOD reference distribution / threshold construction
- Validation is used for model/hyperparameter selection
- Test is reserved for final evaluation after the pipeline is frozen
- Unknown values and results must never be guessed
- QC issues take priority over the calendar

## Schedule

### 2026-09-22 — RNA preprocessing + Clinical preprocessing
**5 hours**

1. 0.5 h — Verify local Git/data synchronization and load fixed split
2. 1.0 h — Split RNA matrix by existing `splits.csv` and QC patient alignment
3. 1.5 h — Train-only low-expression filtering
   - Criterion: TPM >= 1 in at least 20% of Train patients
   - Apply Train-derived gene list unchanged to Validation/Test
4. 1.0 h — `log2(TPM + 1)` transform and QC
5. 1.0 h — Clinical feature QC / encoding plan and preprocessing setup

**Completion criteria**
- RNA Train/Validation/Test matrices aligned to 370/79/80 patients
- Final retained gene list recorded
- No NaN/Inf introduced by transformation
- Clinical preprocessing rules documented and ready for modeling

### 2026-09-23 — Clinical CoxNet + RNA CoxNet
**5 hours**

1. 1.0 h — Complete Clinical preprocessing
2. 1.5 h — Clinical CoxNet baseline with Train/CV
3. 2.0 h — RNA CoxNet pipeline and first tuning pass
4. 0.5 h — Validation comparison table

**Completion criteria**
- Clinical model runs end-to-end
- RNA model runs end-to-end
- Validation C-index available for both
- Preprocessing remains leakage-safe

### 2026-09-24 — Combined model + Hallmark model
**5 hours**

1. 1.5 h — Clinical + RNA CoxNet
2. 1.0 h — Ensembl/gene symbol mapping for Hallmark analysis
3. 1.0 h — Hallmark pathway score matrix generation
4. 1.5 h — Clinical + Hallmark CoxNet

**Completion criteria**
- All four core model families run successfully
- Patient × Hallmark matrix available
- Validation predictions available for all models

### 2026-09-25 — Model selection and freeze
**5 hours**

1. 1.5 h — Validation-based hyperparameter tuning / cleanup
2. 1.0 h — C-index + 1y/3y td-AUC + IBS on Train/Validation as appropriate
3. 1.0 h — Compare four models
4. 1.0 h — Define patient-level risk score / risk-group procedure
5. 0.5 h — Freeze preprocessing + model configuration before Test evaluation

**Completion criteria**
- Final model settings chosen without Test-set optimization
- Four-model validation comparison table complete
- Risk score generation works at patient level

### 2026-09-26 — Molecular Twin + OOD
**5 hours**

1. 1.5 h — Implement Molecular Twin top-k retrieval
2. 1.0 h — Add similarity, clinical variables, PFI/event output
3. 1.5 h — Implement Train-distribution distance-based OOD score
4. 0.5 h — Set/check OOD threshold using Train/Validation only
5. 0.5 h — Wrap both features as reusable functions

**Completion criteria**
- One patient can retrieve top-k similar Train patients
- OOD score and warning can be produced for a patient
- Neither feature uses Test data to define thresholds/settings

### 2026-09-27 — Streamlit MVP
**5 hours**

1. 1.0 h — App skeleton and model/data loading
2. 1.0 h — Patient selection + risk score
3. 1.0 h — Feature/pathway explanation
4. 1.0 h — Molecular Twin display
5. 0.5 h — OOD warning
6. 0.5 h — Survival/risk visualization and basic UI cleanup

**Completion criteria**
- Streamlit runs end-to-end locally
- A selected patient shows prediction, explanation, twins, and OOD status
- Demo flow can be completed without notebook interaction

### 2026-09-28 — Final Test evaluation + packaging
**5 hours**

1. 1.0 h — Confirm pipeline/model freeze and run final Test evaluation once
2. 1.0 h — Final model comparison table and figures
3. 1.0 h — End-to-end Streamlit test and bug fixes
4. 1.0 h — README / reproducibility / project structure cleanup
5. 0.5 h — Demo scenario rehearsal
6. 0.5 h — Final file/path/Git checks

**Completion criteria**
- Final Test C-index / td-AUC / IBS recorded
- Final comparison figures/tables available
- Streamlit demo works
- README explains data, methods, results, and demo usage
- Repository is presentation-ready

## Priority if Schedule Slips

Do not drop:
1. Leakage-safe preprocessing
2. Four core model comparison
3. Validation-based model selection
4. Final Test evaluation
5. Hallmark interpretation

Reduce complexity in this order if needed:
1. UI styling
2. Extra plots
3. OOD sophistication
4. Molecular Twin sophistication

Molecular Twin, OOD, and Streamlit remain in the **target scope**, but must stay MVP-level so the scientific core is not compromised.

## Final Deliverable

By 2026-09-28 the intended deliverable is:

**TCGA-KIRC Clinical/RNA PFI prediction → four-model comparison → patient risk score → Hallmark interpretation → Molecular Twin → OOD warning → Streamlit demo**
