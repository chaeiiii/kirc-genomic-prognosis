import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.patient_inference import (
    get_available_patients,
    predict_patient,
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
# Patient selection
# ============================================================

patient_ids = get_available_patients()

st.sidebar.header("Patient Selection")

patient_id = st.sidebar.selectbox(
    "Select a Test patient",
    patient_ids,
)

st.sidebar.caption(
    f"{len(patient_ids)} Test patients are available "
    "for the current demonstration."
)


# ============================================================
# Run inference
# ============================================================

result = predict_patient(
    patient_id,
    top_xai=10,
    top_twins=5,
)

clinical = result["clinical"]
risk_score = result["risk_score"]
support = result["molecular_support"]
contributions = result["top_contributions"]
twins = result["molecular_twins"]


# ============================================================
# Patient information
# ============================================================

st.header("1. Patient Information")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Age", clinical["age"])
col2.metric("Gender", clinical["gender"])
col3.metric("Stage", clinical["stage"])
col4.metric("Grade", clinical["grade"])

st.caption(f"Patient ID: {patient_id}")


# ============================================================
# Risk score
# ============================================================

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


# ============================================================
# Patient-level XAI
# ============================================================

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


# ============================================================
# Molecular Support
# ============================================================

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


# ============================================================
# Molecular Twins
# ============================================================

st.header("5. Top-5 Molecular Twins")

st.write(
    """
    Molecular Twins are Train patients with RNA-expression
    profiles most similar to the selected Test patient.
    Clinical variables and PFI outcomes are not used to
    determine similarity.
    """
)

display_twins = twins[
    [
        "twin_patient_id",
        "similarity",
        "age",
        "gender",
        "stage",
        "grade",
        "pfi_event",
        "pfi_time",
    ]
].copy()

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
    }
)

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
    "predictions of the selected patient's outcome."
)


# ============================================================
# Interpretation summary
# ============================================================

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
    **Patient {patient_id}**

    - Clinical + RNA CoxNet relative risk score: **{risk_score:.3f}**
    - Nearest Train-patient RNA similarity:
      **{support['max_similarity']:.3f}**
    - Molecular Support threshold:
      **{support['support_threshold']:.3f}**
    - {support_text}
    """
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