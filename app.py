import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.patient_inference import (
    get_available_patients,
    predict_patient,
    predict_new_patient,
)


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="TCGA-KIRC Prognosis Explorer",
    page_icon="🧬",
    layout="wide",
)


# ============================================================
# Helper functions
# ============================================================

def show_results(
    clinical,
    risk_score,
    support,
    contributions,
    twins,
    patient_label,
):
    # --------------------------------------------------------
    # Patient information
    # --------------------------------------------------------
    st.header("1. Patient Information")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Age", clinical["age"])
    col2.metric("Gender", clinical["gender"])
    col3.metric("Stage", clinical["stage"])
    col4.metric("Grade", clinical["grade"])

    st.caption(f"Patient: {patient_label}")

    # --------------------------------------------------------
    # Risk score
    # --------------------------------------------------------
    st.header("2. PFI Prognostic Risk")

    risk_col1, risk_col2 = st.columns([1, 2])

    with risk_col1:
        st.metric(
            "Clinical + RNA CoxNet Risk Score",
            f"{risk_score:.3f}",
        )

    with risk_col2:
        st.write(
            """
            The displayed value is the Cox model's **linear predictor**.
            Higher values indicate higher model-predicted relative
            prognostic risk within this model.

            It is **not** a calibrated probability of progression
            or recurrence.
            """
        )

    # --------------------------------------------------------
    # Patient-level XAI
    # --------------------------------------------------------
    st.header("3. Why This Prediction?")

    st.write(
        """
        The chart shows the features with the largest absolute
        contributions to this patient's Cox linear predictor.

        **Contribution = transformed feature value × Cox coefficient**
        """
    )

    xai_plot = contributions.copy()
    xai_plot = xai_plot.sort_values(
        "contribution",
        ascending=True,
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        xai_plot["feature"],
        xai_plot["contribution"],
    )

    ax.axvline(
        0,
        linewidth=1,
    )

    ax.set_xlabel("Contribution to predicted log-risk")
    ax.set_ylabel("")
    ax.set_title("Top Patient-level Contributions")

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    with st.expander("View contribution values"):
        st.dataframe(
            contributions[
                ["feature", "contribution"]
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "Positive and negative contributions describe the fitted "
        "model's prediction mechanism and should not be interpreted "
        "as causal effects."
    )

    # --------------------------------------------------------
    # Molecular Support
    # --------------------------------------------------------
    st.header("4. Molecular Support")

    support_col1, support_col2, support_col3 = st.columns(3)

    support_col1.metric(
        "Nearest Train Patient",
        support["nearest_train_patient"],
    )

    support_col2.metric(
        "Maximum RNA Similarity",
        f"{support['max_similarity']:.3f}",
    )

    support_col3.metric(
        "Support Threshold",
        f"{support['support_threshold']:.3f}",
    )

    if support["low_support"]:
        st.warning(
            "Low molecular support: this patient's RNA profile has "
            "relatively low similarity to the training cohort."
        )
    else:
        st.success(
            "Molecularly supported: at least one training patient "
            "exceeds the predefined similarity threshold."
        )

    st.caption(
        "The support threshold was derived from the training cohort. "
        "This is a similarity-based support heuristic, not a formal "
        "out-of-distribution classification."
    )

    # --------------------------------------------------------
    # Molecular Twins
    # --------------------------------------------------------
    st.header("5. Top-5 Molecular Twins")

    st.write(
        """
        Molecular Twins are Train patients with RNA-expression
        profiles most similar to the query patient's RNA profile.
        Clinical variables and PFI outcomes are not used to
        determine similarity.
        """
    )

    display_twins = twins.copy()

    # Existing precomputed results use pfi_event / pfi_time.
    # Real-time new-patient results may use PFI / PFI.time.
    display_twins = display_twins.rename(
        columns={
            "twin_patient_id": "Train Patient",
            "similarity": "RNA Similarity",
            "age": "Age",
            "gender": "Gender",
            "stage": "Stage",
            "grade": "Grade",
            "pfi_event": "PFI Event",
            "pfi_time": "PFI Time (days)",
            "PFI": "PFI Event",
            "PFI.time": "PFI Time (days)",
        }
    )

    twin_columns = [
        "Train Patient",
        "RNA Similarity",
        "Age",
        "Gender",
        "Stage",
        "Grade",
        "PFI Event",
        "PFI Time (days)",
    ]

    available_columns = [
        column
        for column in twin_columns
        if column in display_twins.columns
    ]

    display_twins = display_twins[available_columns].copy()

    if "RNA Similarity" in display_twins.columns:
        display_twins["RNA Similarity"] = (
            display_twins["RNA Similarity"].round(3)
        )

    st.dataframe(
        display_twins,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "PFI event and time are shown only as retrospective information "
        "after RNA-based similarity search. Twin outcomes are not "
        "predictions of the query patient's outcome."
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------
    st.header("6. Patient-level Summary")

    if support["low_support"]:
        support_text = (
            "The patient's molecular profile has relatively low "
            "support from similar training examples."
        )
    else:
        support_text = (
            "The patient's molecular profile has at least one "
            "training example above the predefined support threshold."
        )

    st.write(
        f"""
        **Patient: {patient_label}**

        - Clinical + RNA CoxNet relative risk score: **{risk_score:.3f}**
        - Nearest Train-patient RNA similarity:
          **{support['max_similarity']:.3f}**
        - Molecular Support threshold:
          **{support['support_threshold']:.3f}**
        - {support_text}
        """
    )


# ============================================================
# Title
# ============================================================

st.title("TCGA-KIRC Prognosis Explorer")

st.caption(
    "Patient-level PFI prognosis exploration using a frozen "
    "Clinical + RNA CoxNet model."
)

st.info(
    "Research/portfolio prototype. "
    "The CoxNet risk score is a relative prognostic score, "
    "not an absolute probability of progression or recurrence."
)


# ============================================================
# Mode selection
# ============================================================

st.sidebar.header("Prediction Mode")

mode = st.sidebar.radio(
    "Select input mode",
    [
        "Existing TCGA Test Patient",
        "New Patient",
    ],
)


# ============================================================
# Existing TCGA Test Patient
# ============================================================

if mode == "Existing TCGA Test Patient":

    patient_ids = get_available_patients()

    patient_id = st.sidebar.selectbox(
        "Select a Test patient",
        patient_ids,
    )

    st.sidebar.caption(
        f"{len(patient_ids)} Test patients are available "
        "for the current demonstration."
    )

    result = predict_patient(
        patient_id,
        top_xai=10,
        top_twins=5,
    )

    show_results(
        clinical=result["clinical"],
        risk_score=result["risk_score"],
        support=result["molecular_support"],
        contributions=result["top_contributions"],
        twins=result["molecular_twins"],
        patient_label=patient_id,
    )


# ============================================================
# New Patient
# ============================================================

else:

    st.header("New Patient Input")

    st.write(
        """
        Enter clinical information and upload RNA-seq expression
        values in TPM. The frozen preprocessing pipeline and
        frozen Clinical + RNA CoxNet model are applied without
        refitting on the new patient.
        """
    )

    # --------------------------------------------------------
    # Clinical input
    # --------------------------------------------------------

    st.subheader("Clinical Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=120,
            value=60,
            step=1,
        )

        gender = st.selectbox(
            "Gender",
            [
                "FEMALE",
                "MALE",
            ],
        )

    with col2:
        stage = st.selectbox(
            "Pathologic Stage",
            [
                "Stage I",
                "Stage II",
                "Stage III",
                "Stage IV",
                "Unknown",
            ],
        )

        grade = st.selectbox(
            "Histologic Grade",
            [
                "G1",
                "G2",
                "G3",
                "G4",
                "Unknown",
            ],
        )

    clinical_data = {
        "age": float(age),
        "gender": gender,
        "stage": stage,
        "grade": grade,
    }

    # --------------------------------------------------------
    # RNA input
    # --------------------------------------------------------

    st.subheader("RNA-seq Expression")

    st.write(
        """
        Upload a CSV containing gene identifiers and TPM expression
        values.

        Required columns: `gene_id`, `tpm`
        """
    )

    uploaded_file = st.file_uploader(
        "Upload RNA TPM CSV",
        type=["csv"],
    )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    if uploaded_file is None:
        st.info(
            "Upload an RNA TPM CSV file to enable prediction."
        )

    else:
        try:
            rna_df = pd.read_csv(uploaded_file)

            required_columns = {
                "gene_id",
                "tpm",
            }

            missing_columns = (
                required_columns
                - set(rna_df.columns)
            )

            if missing_columns:
                raise ValueError(
                    "RNA CSV must contain the columns: "
                    "gene_id and tpm."
                )

            if rna_df["gene_id"].isna().any():
                raise ValueError(
                    "gene_id contains missing values."
                )

            if rna_df["gene_id"].duplicated().any():
                raise ValueError(
                    "RNA CSV contains duplicated gene_id values."
                )

            rna_df["gene_id"] = (
                rna_df["gene_id"].astype(str)
            )

            rna_df["tpm"] = pd.to_numeric(
                rna_df["tpm"],
                errors="coerce",
            )

            if rna_df["tpm"].isna().any():
                raise ValueError(
                    "TPM contains missing or non-numeric values."
                )

            if (rna_df["tpm"] < 0).any():
                raise ValueError(
                    "TPM values must be non-negative."
                )

            rna_data = rna_df.set_index(
                "gene_id"
            )["tpm"]

            st.success(
                f"RNA file loaded successfully: "
                f"{len(rna_data):,} genes."
            )

            run_prediction = st.button(
                "Run Prediction",
                type="primary",
            )

            if run_prediction:

                with st.spinner(
                    "Running frozen Clinical + RNA inference..."
                ):
                    result = predict_new_patient(
                        clinical_data=clinical_data,
                        rna_data=rna_data,
                        top_xai=10,
                        top_twins=5,
                    )

                st.divider()

                show_results(
                    clinical=result["clinical"],
                    risk_score=result["risk_score"],
                    support=result["molecular_support"],
                    contributions=result["top_contributions"],
                    twins=result["molecular_twins"],
                    patient_label="New Patient",
                )

        except Exception as exc:
            st.error(
                f"Unable to process the RNA input: {exc}"
            )


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "TCGA-KIRC patient-level PFI prognosis research prototype. "
    "This application is intended for research and portfolio "
    "demonstration purposes and is not a clinical decision-support tool."
)