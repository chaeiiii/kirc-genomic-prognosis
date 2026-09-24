# ============================================================
# TCGA-KIRC Patient-level Clinical + RNA Inference
# ============================================================

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"
MODEL_DIR = PROJECT_ROOT / "models"


# ------------------------------------------------------------
# 2. Load data
# ------------------------------------------------------------

cohort = pd.read_parquet(
    DATA_DIR / "kirc_modeling_cohort.parquet"
)

rna_tpm = pd.read_parquet(
    DATA_DIR / "rna_tpm_modeling_raw.parquet"
)

# RNA matrix index must be patient_id
rna_tpm.index = rna_tpm.index.astype(str)


# ------------------------------------------------------------
# 3. Load frozen Clinical + RNA artifacts
# ------------------------------------------------------------

clinical_preprocessor = joblib.load(
    MODEL_DIR / "clinical_preprocessor.joblib"
)

combined_scaler = joblib.load(
    MODEL_DIR / "combined_scaler.joblib"
)

clinical_rna_model = joblib.load(
    MODEL_DIR / "clinical_rna_coxnet.joblib"
)

selected_rna_genes = joblib.load(
    MODEL_DIR / "selected_rna_genes.joblib"
)

model_config = joblib.load(
    MODEL_DIR / "clinical_rna_config.joblib"
)

clinical_features = model_config["clinical_features"]
model_alpha = model_config["alpha"]


# ------------------------------------------------------------
# 4. Load Molecular Twin / Support results
# ------------------------------------------------------------

molecular_twins = pd.read_csv(
    RESULTS_DIR / "molecular_twin_results.csv"
)

molecular_support = pd.read_csv(
    RESULTS_DIR / "patient_molecular_support_summary.csv"
)


# ------------------------------------------------------------
# 5. Feature names and Cox coefficients
# ------------------------------------------------------------

clinical_feature_names = (
    clinical_preprocessor
    .get_feature_names_out()
    .tolist()
)

feature_names = (
    clinical_feature_names
    + list(selected_rna_genes)
)

# Selected alpha = index used in the frozen model
alpha_idx = model_config["alpha_idx"]

beta = clinical_rna_model.coef_[:, alpha_idx]

if len(feature_names) != len(beta):
    raise ValueError(
        "Feature names and CoxNet coefficients have different lengths."
    )


# ------------------------------------------------------------
# 6. Patient input preprocessing
# ------------------------------------------------------------

def preprocess_patient(patient_id):
    """
    Reproduce the frozen Clinical + RNA preprocessing
    for one patient.
    """

    patient = cohort.loc[
        cohort["patient_id"] == patient_id
    ].copy()

    if len(patient) != 1:
        raise ValueError(
            f"patient_id '{patient_id}' was not found exactly once."
        )

    if patient_id not in rna_tpm.index:
        raise ValueError(
            f"RNA data for patient_id '{patient_id}' was not found."
        )

    # Clinical preprocessing
    X_clin = clinical_preprocessor.transform(
        patient[clinical_features]
    )

    # RNA preprocessing
    # The selected genes were determined from Train only.
    X_rna = np.log2(
        rna_tpm.loc[
            [patient_id],
            selected_rna_genes
        ] + 1
    ).to_numpy()

    # Combine Clinical + RNA
    X_raw = np.hstack([
        X_clin,
        X_rna
    ])

    # Frozen Train-fitted scaler
    X_scaled = combined_scaler.transform(
        X_raw
    )

    return patient, X_scaled


# ------------------------------------------------------------
# 7. Clinical + RNA risk score
# ------------------------------------------------------------

def predict_clinical_rna_risk(patient_id):
    """
    Return the frozen CoxNet linear predictor.

    This is a relative prognostic risk score,
    not an absolute probability of progression.
    """

    _, X_scaled = preprocess_patient(patient_id)

    risk_score = clinical_rna_model.predict(
        X_scaled,
        alpha=model_alpha
    )[0]

    return float(risk_score)


# ------------------------------------------------------------
# 8. Patient-level XAI
# ------------------------------------------------------------

def explain_patient(patient_id, top_n=10):
    """
    Calculate local feature contributions:

        contribution_j = x_j * beta_j

    The sum of all contributions reproduces
    the Cox linear predictor.
    """

    _, X_scaled = preprocess_patient(patient_id)

    contributions = X_scaled[0] * beta

    explanation = pd.DataFrame({
        "feature": feature_names,
        "contribution": contributions,
    })

    explanation["abs_contribution"] = (
        explanation["contribution"].abs()
    )

    explanation = (
        explanation
        .sort_values(
            "abs_contribution",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    return explanation


# ------------------------------------------------------------
# 9. Molecular Twin lookup
# ------------------------------------------------------------

def get_molecular_twins(patient_id, top_n=5):
    """
    Return previously computed RNA-based Molecular Twins.

    PFI outcomes were NOT used for similarity search.
    They are retrospective information only.
    """

    twins = molecular_twins.loc[
        molecular_twins["query_patient_id"] == patient_id
    ].copy()

    if twins.empty:
        raise ValueError(
            f"No Molecular Twin results found for '{patient_id}'. "
            "The current demo supports patients with precomputed "
            "Test-cohort Twin results."
        )

    twins = (
        twins
        .sort_values(
            "similarity",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    return twins


# ------------------------------------------------------------
# 10. Molecular Support lookup
# ------------------------------------------------------------

def get_molecular_support(patient_id):
    """
    Return the precomputed molecular-support result.

    low_support is a training-cohort similarity heuristic,
    not a formal OOD classification.
    """

    support = molecular_support.loc[
        molecular_support["patient_id"] == patient_id
    ].copy()

    if len(support) != 1:
        raise ValueError(
            f"Molecular Support result for '{patient_id}' "
            "was not found exactly once."
        )

    row = support.iloc[0]

    return {
        "nearest_train_patient": row["nearest_train_patient"],
        "max_similarity": float(row["max_similarity"]),
        "support_threshold": float(row["ood_threshold"]),
        "low_support": bool(row["low_support"]),
    }


# ------------------------------------------------------------
# 11. Available demo patients
# ------------------------------------------------------------

def get_available_patients():
    """
    Return patients for whom precomputed Molecular Twin
    and Molecular Support results are available.
    """

    twin_ids = set(
        molecular_twins["query_patient_id"].astype(str)
    )

    support_ids = set(
        molecular_support["patient_id"].astype(str)
    )

    available_ids = sorted(
        twin_ids.intersection(support_ids)
    )

    return available_ids


# ------------------------------------------------------------
# 12. Unified patient inference
# ------------------------------------------------------------

def predict_patient(
    patient_id,
    top_xai=10,
    top_twins=5
):
    """
    Integrated patient-level inference for the Streamlit demo.
    """

    patient, _ = preprocess_patient(patient_id)

    risk_score = predict_clinical_rna_risk(patient_id)

    contributions = explain_patient(
        patient_id,
        top_n=top_xai
    )

    support = get_molecular_support(patient_id)

    twins = get_molecular_twins(
        patient_id,
        top_n=top_twins
    )

    clinical = {
        "age": patient.iloc[0]["age"],
        "gender": patient.iloc[0]["gender"],
        "stage": patient.iloc[0]["stage"],
        "grade": patient.iloc[0]["grade"],
    }

    return {
        "patient_id": patient_id,
        "clinical": clinical,
        "risk_score": risk_score,
        "molecular_support": support,
        "top_contributions": contributions,
        "molecular_twins": twins,
    }