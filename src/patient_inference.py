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

# ============================================================
# 13. Load real-time Molecular Twin artifacts
# ============================================================

from sklearn.metrics.pairwise import cosine_similarity


twin_features = pd.read_csv(
    RESULTS_DIR / "molecular_twin_features.csv"
)

twin_train_reference = pd.read_parquet(
    RESULTS_DIR / "molecular_twin_train_reference.parquet"
)

support_config = pd.read_csv(
    RESULTS_DIR / "molecular_support_config.csv"
)

twin_genes = twin_features["gene_id"].astype(str).tolist()

twin_mean = twin_features["train_mean"].to_numpy(dtype=float)
twin_scale = twin_features["train_scale"].to_numpy(dtype=float)

support_threshold = float(
    support_config.iloc[0]["threshold"]
)


# ============================================================
# 14. New-patient preprocessing
# ============================================================

def preprocess_new_patient(
    clinical_data,
    rna_data
):
    """
    Apply the frozen Clinical + RNA preprocessing to a new patient.

    Parameters
    ----------
    clinical_data : dict
        Clinical feature values for one new patient.

    rna_data : pandas.Series
        TPM expression values indexed by gene ID.

    Returns
    -------
    X_scaled : ndarray, shape (1, n_model_features)
        Frozen Clinical + RNA model input.

    rna_log : pandas.Series
        log2(TPM + 1) RNA values for the supplied genes.
    """

    clinical_df = pd.DataFrame(
        [clinical_data]
    )

    # Ensure every required clinical feature exists
    missing_clinical = [
        feature
        for feature in clinical_features
        if feature not in clinical_df.columns
    ]

    if missing_clinical:
        raise ValueError(
            "Missing clinical features: "
            + ", ".join(missing_clinical)
        )

    # Clinical preprocessing using frozen Train-fitted transformer
    X_clin = clinical_preprocessor.transform(
        clinical_df[clinical_features]
    )

    # Validate RNA
    rna_data = rna_data.copy()
    rna_data.index = rna_data.index.astype(str)

    required_genes = set(selected_rna_genes)

    missing_genes = sorted(
        required_genes.difference(rna_data.index)
    )

    if missing_genes:
        raise ValueError(
            f"RNA input is missing {len(missing_genes)} "
            "genes required by the frozen model."
        )

    selected_tpm = (
        rna_data
        .loc[selected_rna_genes]
        .astype(float)
    )

    if selected_tpm.isna().any():
        raise ValueError(
            "RNA input contains missing TPM values."
        )

    if (selected_tpm < 0).any():
        raise ValueError(
            "TPM values must be non-negative."
        )

    # Same RNA transformation used during model development
    selected_log = np.log2(
        selected_tpm.to_numpy() + 1
    ).reshape(1, -1)

    X_raw = np.hstack([
        X_clin,
        selected_log
    ])

    # Frozen Train-fitted combined scaler
    X_scaled = combined_scaler.transform(
        X_raw
    )

    # Keep log-transformed RNA for Twin calculation
    rna_log = np.log2(
        rna_data.astype(float) + 1
    )

    return X_scaled, rna_log


# ============================================================
# 15. New-patient Molecular Twin / Support
# ============================================================

def calculate_new_patient_twins(
    rna_log,
    top_n=5
):
    """
    Calculate Molecular Twins for a new patient using the
    frozen Train-defined Top-500 RNA space.
    """

    missing_twin_genes = [
        gene
        for gene in twin_genes
        if gene not in rna_log.index
    ]

    if missing_twin_genes:
        raise ValueError(
            f"RNA input is missing {len(missing_twin_genes)} "
            "genes required for Molecular Twin analysis."
        )

    query_log = (
        rna_log
        .loc[twin_genes]
        .to_numpy(dtype=float)
    )

    # Reproduce frozen Train-fitted StandardScaler.transform()
    query_scaled = (
        query_log - twin_mean
    ) / twin_scale

    query_scaled = query_scaled.reshape(1, -1)

    # Safety check
    if query_scaled.shape[1] != twin_train_reference.shape[1]:
        raise ValueError(
            "New-patient Twin feature dimension does not match "
            "the frozen Train reference."
        )

    similarities = cosine_similarity(
        query_scaled,
        twin_train_reference.to_numpy()
    )[0]

    twin_result = pd.DataFrame({
        "twin_patient_id":
            twin_train_reference.index.astype(str),
        "similarity": similarities,
    })

    twin_result = (
        twin_result
        .sort_values(
            "similarity",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    max_similarity = float(
        twin_result.iloc[0]["similarity"]
    )

    nearest_patient = str(
        twin_result.iloc[0]["twin_patient_id"]
    )

    support = {
        "nearest_train_patient": nearest_patient,
        "max_similarity": max_similarity,
        "support_threshold": support_threshold,
        "low_support": bool(
            max_similarity < support_threshold
        ),
    }

    # Add retrospective clinical / PFI information
    # AFTER RNA-based similarity search.
    # These variables are NOT used to calculate similarity.
    twin_metadata = cohort[
        [
            "patient_id",
            "age",
            "gender",
            "stage",
            "grade",
            "pfi_event",
            "pfi_time",
        ]
    ].copy()

    twin_metadata["patient_id"] = twin_metadata["patient_id"].astype(str)

    twin_result = twin_result.merge(
        twin_metadata,
        left_on="twin_patient_id",
        right_on="patient_id",
        how="left",
    )

    twin_result = twin_result.drop(columns=["patient_id"])

    return twin_result, support

# ============================================================
# 16. New-patient integrated inference
# ============================================================

def predict_new_patient(
    clinical_data,
    rna_data,
    top_xai=10,
    top_twins=5
):
    """
    Integrated inference for a genuinely new patient.

    No model fitting or parameter estimation is performed here.
    All preprocessing/model parameters come from Train-fitted
    frozen artifacts.
    """

    X_scaled, rna_log = preprocess_new_patient(
        clinical_data,
        rna_data
    )

    # Risk
    risk_score = clinical_rna_model.predict(
        X_scaled,
        alpha=model_alpha
    )[0]

    # Local XAI
    contribution_values = X_scaled[0] * beta

    contributions = pd.DataFrame({
        "feature": feature_names,
        "contribution": contribution_values,
    })

    contributions["abs_contribution"] = (
        contributions["contribution"].abs()
    )

    contributions = (
        contributions
        .sort_values(
            "abs_contribution",
            ascending=False
        )
        .head(top_xai)
        .reset_index(drop=True)
    )

    # Molecular Twin + support
    twins, support = calculate_new_patient_twins(
        rna_log,
        top_n=top_twins
    )

    return {
        "clinical": clinical_data,
        "risk_score": float(risk_score),
        "molecular_support": support,
        "top_contributions": contributions,
        "molecular_twins": twins,
    }