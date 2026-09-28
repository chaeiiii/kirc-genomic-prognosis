# TCGA-KIRC Patient-level PFI Prognosis

A survival analysis project for predicting **Progression-Free Interval (PFI)** in TCGA Kidney Renal Clear Cell Carcinoma (KIRC) patients using clinical and RNA-seq data.

The project compares clinical and molecular prognostic models and extends the final Clinical+RNA model with patient-level interpretation, molecular similarity search, and training-cohort support assessment.

---

## 1. Project Overview

The goal of this project is to investigate whether RNA-seq information provides additional prognostic value beyond routinely available clinical variables for patient-level PFI prediction in TCGA-KIRC.

Four survival models were developed and compared:

- RNA-only
- Clinical-only
- Clinical + RNA
- Clinical + Hallmark

The project additionally implements:

- Global and patient-level model interpretation
- Molecular Twin retrieval using RNA-expression similarity
- Molecular Support assessment relative to the training cohort
- An integrated patient-level inference pipeline
- Reproducibility and consistency checks

The primary endpoint is **Progression-Free Interval (PFI)**.

---

## 2. Dataset

Data were obtained from **The Cancer Genome Atlas Kidney Renal Clear Cell Carcinoma (TCGA-KIRC)** cohort.

Two main data modalities were used:

### Clinical data

Clinical variables used for modeling include:

- Age
- Gender
- Pathologic stage
- Histologic grade

PFI event status and PFI time were used as survival outcomes.

### RNA-seq data

RNA expression data were derived from GDC STAR Counts files.

The RNA processing workflow included:

- TPM-based expression values
- Protein-coding genes only
- Train-derived low-expression filtering
- `log2(TPM + 1)` transformation
- Train-derived feature selection

---

## 3. Modeling Cohort

After clinical-RNA matching and survival-data quality control, the final modeling cohort contained:

| Cohort | N | PFI Events | Event Rate |
|---|---:|---:|---:|
| Total | 529 | 159 | 30.1% |
| Train | 370 | 111 | 30.0% |
| Validation | 79 | 24 | 30.4% |
| Test | 80 | 24 | 30.0% |

A fixed random seed (`seed=42`) and event-stratified splitting were used.

All train-dependent preprocessing and feature selection procedures were fitted using training data only.

---

## 4. Analysis Pipeline

```text
TCGA-KIRC
   │
   ├── Clinical data
   │
   └── RNA-seq data
          │
          ▼
Patient-level matching
          │
          ▼
Survival-data QC
          │
          ▼
529-patient modeling cohort
          │
          ▼
Train / Validation / Test split
          │
          ▼
Train-derived preprocessing
          │
          ▼
Survival model development
          │
          ├── RNA-only
          ├── Clinical-only
          ├── Clinical + RNA
          └── Clinical + Hallmark
          │
          ▼
Test-set evaluation
          │
          ├── Harrell C-index
          ├── Time-dependent AUC
          └── Integrated Brier Score
          │
          ▼
Clinical + RNA interpretation
          │
          ├── Global XAI
          └── Patient-level XAI
          │
          ▼
Molecular Twin + Molecular Support
          │
          ▼
Patient-level inference pipeline
```

---

## 5. Survival Models

Regularized Cox proportional hazards models (**CoxNet**) were used for high-dimensional survival modeling.

### RNA-only

Uses RNA-expression features selected from the training cohort.

### Clinical-only

Uses encoded clinical variables:

- Age
- Gender
- Stage
- Grade

### Clinical + RNA

Combines:

- 10 encoded clinical features
- 500 RNA-expression features

for a total of **510 model inputs**.

At the selected regularization parameter, **24 features had non-zero coefficients**:

- 3 clinical features
- 21 RNA features

### Clinical + Hallmark

Combines clinical variables with pathway-level Hallmark molecular features.

---

## 6. Model Performance

Final Test-set performance:

| Model | Harrell C-index | 1-year AUC | 3-year AUC | IBS (1–3 years) |
|---|---:|---:|---:|---:|
| RNA-only | 0.715 | 0.708 | 0.723 | 0.148 |
| Clinical-only | 0.887 | 0.888 | 0.911 | **0.092** |
| Clinical + RNA | **0.892** | 0.880 | **0.944** | 0.099 |
| Clinical + Hallmark | 0.886 | **0.901** | 0.895 | 0.093 |

Higher C-index and AUC indicate better discrimination, while lower IBS indicates better prediction error performance over the evaluated time interval.

The models showed different strengths across evaluation metrics rather than one model uniformly outperforming the others.

---

## 7. Incremental Value of RNA

The Clinical+RNA model achieved a slightly higher Test Harrell C-index than the Clinical-only model:

```text
Clinical-only : 0.887
Clinical+RNA  : 0.892
```

A paired bootstrap comparison was therefore performed.

```text
ΔC (Clinical+RNA − Clinical-only) = +0.0051

95% bootstrap CI:
-0.0243 to +0.0440
```

Because the confidence interval includes zero, the Test-set analysis does **not provide clear evidence that RNA features improve discrimination beyond the Clinical-only model** in this cohort.

Therefore, the molecular component is not interpreted as demonstrating a statistically clear incremental discrimination benefit.

---

## 8. Model Interpretation

The Clinical+RNA CoxNet model was interpreted at both global and patient levels.

### Global interpretation

Non-zero CoxNet coefficients were examined to identify features contributing to the model's linear risk score.

### Patient-level interpretation

For patient \(i\) and feature \(j\), the local contribution was calculated as:

\[
\text{Contribution}_{ij} = x_{ij}\beta_j
\]

where:

- \(x_{ij}\) is the transformed and standardized feature value
- \(\beta_j\) is the corresponding CoxNet coefficient

The patient-specific Cox linear predictor is therefore:

\[
\text{Risk Score}_i = \sum_j x_{ij}\beta_j
\]

The implementation was numerically verified by confirming that the sum of feature contributions reproduces the model risk score.

These contributions describe the fitted model's prediction mechanism and should **not** be interpreted as causal biological effects.

---

## 9. Molecular Twin

To provide molecular reference cases for individual patients, a Molecular Twin module was developed.

For each Test patient, the **five most similar Train patients** were retrieved using RNA-expression similarity.

Importantly, similarity search does **not** use:

- Clinical variables
- PFI event status
- PFI time

### Molecular Twin preprocessing

```text
19,962 protein-coding genes
        ↓
Train-derived low-expression filtering
        ↓
14,220 genes
        ↓
log2(TPM + 1)
        ↓
Train MAD ranking
        ↓
Top 500 genes
        ↓
Train-fitted StandardScaler
        ↓
Cosine similarity
        ↓
Top-5 Train patients
```

Across 80 Test patients:

- 400 patient-twin pairs were generated
- 202 unique Train patients appeared as twins
- Mean similarity: 0.5083
- Median similarity: 0.4939
- Similarity range: 0.2374–0.9636

PFI outcomes of retrieved Train patients are appended only after similarity search for retrospective context.

They are **not predictions of the query patient's outcome**.

---

## 10. Molecular Support

A Molecular Support indicator was developed to identify Test patients whose RNA-expression profiles have relatively weak representation in the training cohort.

For each Train patient, the nearest other Train patient was identified.

The support threshold was defined using the **5th percentile of Train nearest-neighbor similarity**:

```text
Molecular Support threshold = 0.3810
```

A Test patient is flagged as low molecular support when:

\[
\max(\text{similarity to Train}) < 0.3810
\]

Results:

```text
Low-support Test patients: 4 / 80
Low-support rate: 5%
```

This indicator represents **low molecular similarity to the training cohort**.

It should not be interpreted as a formal out-of-distribution (OOD) detector.

---

## 11. Patient-level Inference

The final patient-level pipeline integrates the Clinical+RNA model with interpretation and molecular-reference information.

```text
Patient
   │
   ├── Clinical features
   └── RNA expression
          │
          ▼
Frozen preprocessing
          │
          ▼
Clinical + RNA CoxNet
          │
          ├── Relative risk score
          ├── Patient-level feature contributions
          ├── Top-5 Molecular Twins
          └── Molecular Support
          │
          ▼
Integrated Patient Report
```

The generated report includes:

- Patient clinical information
- CoxNet relative risk score
- Major patient-level feature contributions
- Top-5 molecularly similar Train patients
- Molecular Support information

The CoxNet output is a **relative prognostic score (linear predictor)** and is not an absolute probability of progression or recurrence.

---

## 12. Reproducibility QC

The reconstructed patient-level inference pipeline was tested across all **80 Test patients**.

Results:

```text
Patients checked: 80

Maximum batch vs. single-patient risk difference:
4.44 × 10^-16

Maximum risk score vs. XAI contribution-sum difference:
4.44 × 10^-16

Batch vs. single-patient risk agreement:
80 / 80

Risk score vs. XAI contribution-sum agreement:
80 / 80
```

The observed differences are within floating-point numerical precision, supporting internal consistency of the reconstructed inference pipeline.

---

## 13. Data Leakage Prevention

Special attention was given to preventing information leakage.

Train-dependent procedures were fitted using the **Train cohort only**, including:

- Low-expression filtering
- RNA feature ranking and selection
- Feature scaling
- Clinical preprocessing
- Molecular Twin feature construction
- Molecular Support threshold construction

Validation and Test data were transformed using parameters derived from the Train cohort.

PFI outcomes were not used in Molecular Twin similarity search.

---

## 14. Repository Structure

```text
kirc-genomic-prognosis/
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── manifests/
│
├── models/
│   └── frozen model and preprocessing artifacts
│
├── notebooks/
│   ├── 00_clinical_data_audit.ipynb
│   ├── 01_rna_data_audit.ipynb
│   ├── 02_split_preprocessing.ipynb
│   ├── 03_results_visualization.ipynb
│   ├── 04_xai_interpretation.ipynb
│   ├── 05_molecular_twin_ood.ipynb
│   ├── 06_patient_inference.ipynb
│   └── 07_final_results_summary.ipynb
│
├── results/
│   ├── final_model_comparison.csv
│   ├── final_model_specifications.csv
│   ├── final_performance_summary.csv
│   ├── test_predictions.csv
│   ├── test_discrimination_metrics.csv
│   ├── test_brier_ibs_metrics.csv
│   ├── test_grouped_calibration.csv
│   ├── test_harrell_c_bootstrap_ci.csv
│   ├── test_harrell_c_difference_ci.csv
│   ├── molecular_twin_results.csv
│   ├── molecular_twin_features.csv
│   ├── molecular_twin_train_reference.parquet
│   ├── molecular_support_config.csv
│   ├── patient_molecular_support_summary.csv
│   ├── ood_results.csv
│   └── patient_inference_qc.csv
│
├── reports/
│   ├── figures/
│   ├── progress_log.md
│   └── project_plan.md
│
├── src/
│   └── patient_inference.py
│
├── app.py
├── requirements.txt
└── README.md

---

## 15. Notebook Workflow

The notebooks follow the project workflow:

| Notebook | Purpose |
|---|---|
| `00_clinical_data_audit.ipynb` | Clinical/PFI data inspection and QC |
| `01_rna_data_audit.ipynb` | RNA-seq inspection and preprocessing |
| `02_split_preprocessing.ipynb` | Cohort split, preprocessing, feature selection, and survival modeling |
| `03_results_visualization.ipynb` | Model performance evaluation and visualization |
| `04_xai_interpretation.ipynb` | Global and patient-level model interpretation |
| `05_molecular_twin_ood.ipynb` | Molecular Twin and Molecular Support analysis |
| `06_patient_inference.ipynb` | Integrated patient-level inference and QC |
| `07_final_results_summary.ipynb` | Final project results summary |

---

## 16. Limitations

This project has several important limitations.

1. The analysis uses a single TCGA-KIRC cohort and has no independent external validation.

2. The Test cohort contains only 80 patients and 24 PFI events, which introduces uncertainty into performance estimates and model comparisons.

3. Generalizability to other hospitals, sequencing pipelines, and patient populations has not been established.

4. CoxNet outputs are relative prognostic scores rather than calibrated absolute probabilities.

5. Model coefficients and patient-level contributions describe associations within the fitted prediction model and should not be interpreted as causal effects.

6. Molecular Twin outcomes are retrospective reference examples rather than predictions for an individual patient.

7. Molecular Support is a training-cohort similarity heuristic rather than a formal OOD detection method.

---

## 17. Streamlit Demo and New Patient Inference

An interactive Streamlit application was implemented to demonstrate the
patient-level inference workflow.

```bash
streamlit run app.py
```

The application provides two inference modes:

### Existing TCGA Test Patient

A patient from the held-out TCGA-KIRC Test cohort can be selected to inspect:

- Clinical information
- Clinical + RNA CoxNet relative risk score
- Patient-level feature contributions
- Molecular Support
- Top-5 Molecular Twins

This mode provides a reproducible demonstration using patients already included
in the project Test cohort.

### New Patient

The application also supports inference for a new patient who was not
preloaded into the application.

The required clinical variables are:

- Age
- Gender
- Pathologic stage
- Histologic grade

Supported categorical values are:

```text
Gender:
FEMALE
MALE

Stage:
Stage I
Stage II
Stage III
Stage IV
Unknown

Grade:
G1
G2
G3
G4
Unknown
```

RNA expression is uploaded as a CSV containing gene identifiers and TPM values:

```csv
gene_id,tpm
ENSGXXXXXXXXXXX,12.34
ENSGXXXXXXXXXXX,0.52
ENSGXXXXXXXXXXX,7.81
```

The uploaded RNA profile must contain the genes required by the frozen
Clinical+RNA model and Molecular Twin pipeline.

For a new patient, the application performs:

```text
Clinical input + RNA TPM
          │
          ▼
Frozen Train-derived preprocessing
          │
          ▼
Frozen Clinical + RNA CoxNet
          │
          ├── Relative prognostic risk score
          ├── Patient-level feature contributions
          │
          ▼
RNA-based Molecular Twin search
          │
          ├── Top-5 similar Train patients
          └── Train-derived Molecular Support assessment
```

No preprocessing parameters, feature-selection rules, scalers, model
coefficients, or Molecular Support thresholds are refitted using the new
patient.

### New-patient parity QC

The new-patient inference path was validated by submitting an existing Test
patient (`TCGA-BP-5169`) through the new-patient interface using the patient's
raw clinical variables and TPM profile.

Results:

```text
Existing pipeline risk score : 0.8775333495883141
New-patient pipeline         : 0.8775333629488457
Absolute difference          : 1.34 × 10^-8

Existing maximum similarity  : 0.65425265
New-patient maximum similarity:
0.6542525913044144

Nearest Train patient:
TCGA-BP-4799

Low molecular support:
False
```

The new-patient pathway reproduced the reference prediction with a negligible
numerical difference in the risk score (1.34 × 10^-8), while the Molecular
Twin and Molecular Support results were also reproduced.

The same patient was then evaluated through the complete Streamlit upload
workflow, including a TPM CSV containing 19,962 genes. The application
reproduced the expected risk score, nearest Train patient, molecular
similarity, and support status.

This provides an end-to-end consistency check across:

**CSV input → frozen preprocessing → CoxNet inference → patient-level XAI →
Molecular Twin → Molecular Support → Streamlit output.**

The application is intended exclusively as a research and portfolio
demonstration and is not a clinical decision-support system.

---

## 18. Main Conclusion

Clinical variables provided strong prognostic discrimination in this TCGA-KIRC cohort.

Adding RNA expression produced a small observed increase in Test Harrell C-index (`0.887 → 0.892`) and a higher 3-year AUC, but the paired bootstrap confidence interval for the C-index difference included zero.

Therefore, the current data do not provide clear evidence of an incremental discrimination benefit from RNA over the Clinical-only model.

Beyond model discrimination, the project demonstrates an end-to-end patient-level workflow combining:

**survival modeling → model interpretation → molecular similarity retrieval → training-cohort support assessment → reproducible patient-level inference.**