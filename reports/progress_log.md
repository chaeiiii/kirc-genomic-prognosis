# Project Progress Log

## 2026-09-21

### 1. 오늘의 목표

- [x] RNA expression matrix 생성

- [x] Clinical-RNA matched cohort 확정

- [x] Primary modeling cohort 확정 및 PRE-SPLIT QC

- [x] Train / Validation / Test split

### 2. 오늘 완료한 작업

- TCGA-KIRC Clinical cohort 535명과 대표 RNA 환자 533명을 patient-level로 매칭

- Clinical ∩ RNA 교집합으로 matched cohort 531명 확정

- GDC STAR Counts 기반 protein-coding RNA TPM matrix 생성

  - matched RNA matrix: 531 × 19,962

- 원본 TCGA-CDR에서 `PFI=0` 이면서 `PFI.time=0`인 2명 확인

- 위 2명을 primary survival modeling cohort에서 제외

- 최종 primary modeling cohort 529명 확정

- modeling cohort와 RNA matrix patient set 일치 확인

- PRE-SPLIT QC 완료

- Primary modeling cohort 529명을 Train / Validation / Test로 분할

  - Train: 370명
  - Validation: 79명
  - Test: 80명

- `pfi_event` 기준 stratified split 수행

- random seed = 42 고정

- `splits.csv` 생성 및 저장

- Split QC 완료

  - 전체 rows: 529
  - unique patients: 529
  - duplicated patients: 0
  - Train event proportion: 0.3000
  - Validation event proportion: 0.3038
  - Test event proportion: 0.3000

### 3. 주요 결과

- Clinical cohort: 535 patients

- RNA unique patients: 533 patients

- Clinical-RNA matched cohort: 531 patients

- Primary modeling cohort: 529 patients

- Modeling cohort PFI event distribution

  - event=0: 370
  - event=1: 159

- PFI time range: 2–4074 days

- Raw modeling RNA matrix: 529 × 19,962

- TPM missing values: 0

- protein-coding genes: 19,962

- Train / Validation / Test split

  - Train: 370 patients
    - PFI events: 111
    - event proportion: 0.3000

  - Validation: 79 patients
    - PFI events: 24
    - event proportion: 0.3038

  - Test: 80 patients
    - PFI events: 24
    - event proportion: 0.3000

- Split patient QC

  - total rows: 529
  - unique patients: 529
  - duplicated patients: 0

### 4. 생성/수정된 파일

- `data/interim/kirc_matched_cohort.parquet`

  - Clinical-RNA matched cohort, 531 patients

- `data/interim/rna_tpm_matched.parquet`

  - matched cohort RNA TPM matrix, 531 × 19,962

- `data/processed/kirc_modeling_cohort.parquet`

  - primary survival modeling cohort, 529 patients

- `data/processed/rna_tpm_modeling_raw.parquet`

  - raw TPM matrix for modeling cohort, 529 × 19,962

- `data/processed/splits.csv`

  - Train / Validation / Test patient split 정보, 529 patients

- `notebooks/02_split_preprocessing.ipynb`

  - modeling cohort split 및 split QC 수행

- `reports/progress_log.md`

  - 2026-09-21 작업 종료 상태 업데이트

### 5. 오늘 결정한 분석 기준

- 분석 단위: patient-level

- Primary endpoint: PFI

- 531명은 Clinical-RNA matched cohort로 구분

- 529명은 primary survival modeling cohort로 구분

- RNA expression: GDC STAR Counts의 TPM 사용

- RNA gene set: protein-coding genes 기준

- Train / Validation / Test = 70 / 15 / 15

- split stratification: `pfi_event`

- random seed: 42

- 확정된 `splits.csv`를 이후 모든 모델에서 동일하게 사용

- Clinical / RNA / Clinical+RNA / Clinical+Hallmark 모델 모두 동일 patient split 사용

- low-expression filtering, scaling, feature selection, hyperparameter tuning은 Train 기준으로 수행하여 data leakage 방지

- Validation / Test 데이터는 Train에서 결정된 preprocessing 기준만 적용

- log transform은 `log2(TPM + 1)` 사용 예정

### 6. 확인해야 할 문제 / 미완료

- Train 기준 low-expression filtering 미실행

- Train에서 선택된 gene set을 Validation / Test에 동일 적용 필요

- `log2(TPM + 1)` 변환 미실행

- scaling 미실행

- Clinical feature preprocessing 미실행

- feature selection 및 modeling pipeline 미구축

- Clinical CoxNet baseline 미구축

- RNA survival model 미구축

- Clinical+RNA survival model 미구축

- Clinical+Hallmark survival model 미구축

- Validation 기반 hyperparameter tuning 미실행

- Test set 최종 평가 미실행

### 7. GitHub 상태

- Commit: ✅

- Push: ✅

- Commit message: `update progress log for 2026-09-21`


### 8. 현재 프로젝트 진행 위치

Clinical + RNA cohort 구축 완료  

→ RNA expression matrix 생성 완료  

→ Primary modeling cohort 529명 확정 및 PRE-SPLIT QC 완료  

→ Train / Validation / Test split 완료  

→ Split QC 완료  

→ **Train 기준 leakage-safe RNA preprocessing ← 다음 작업**  

→ Clinical CoxNet baseline  

→ RNA survival model  

→ Clinical+RNA survival model  

→ Clinical+Hallmark survival model  

→ Validation 기반 모델 선택 및 hyperparameter tuning  

→ Test set 최종 평가

### 9. 다음 작업

1. `splits.csv`를 이용하여 RNA matrix를 Train / Validation / Test로 분리

2. Train 데이터만 사용하여 low-expression gene filtering 기준 결정

3. Train에서 선택된 gene set을 Validation / Test에 동일 적용

4. `log2(TPM + 1)` 변환

5. Train 기준 scaling 파라미터 계산

6. 동일한 scaling을 Validation / Test에 적용

7. 전처리 후 각 split의 shape 및 missing value QC

8. Clinical feature preprocessing 준비

9. Clinical CoxNet baseline modeling 준비

## 2026-09-22

### 1. 오늘의 목표

* [x] Train 기준 leakage-safe RNA preprocessing 완료
* [x] Clinical feature preprocessing 완료
* [x] RNA-only CoxNet 구축 및 Train 5-fold CV / Validation 평가
* [x] Clinical-only CoxNet 구축 및 Train 5-fold CV / Validation 평가
* [x] Clinical+RNA CoxNet 구축 및 Validation 평가
* [x] MSigDB Hallmark 50 gene sets 기반 pathway pipeline 구축
* [x] Clinical+Hallmark CoxNet 구축 및 Validation 평가
* [x] 4개 frozen CoxNet 모델의 untouched Test set 최종 평가
* [x] bootstrap confidence interval, Uno C, time-dependent AUC, Brier/IBS, calibration diagnostic 수행
* [x] 주요 결과 figure 생성

### 2. 오늘 완료한 작업

* 기존 primary modeling cohort 529명과 고정된 `splits.csv`를 기준으로 이후 분석을 진행

  * Train: 370명
  * Validation: 79명
  * Test: 80명
  * Train / Validation / Test 간 patient overlap 없음
* RNA expression preprocessing 수행

  * 시작 protein-coding genes: 19,962
  * Train 기준 low-expression filtering 적용
  * filtering 후 14,220 genes 유지
  * `log2(TPM + 1)` 변환 적용
* RNA CoxNet의 고차원 feature selection에서 data leakage를 방지하기 위해 5-fold CV 내부에서 preprocessing 및 MAD 기반 Top-K feature selection을 다시 fit하도록 구성
* RNA CoxNet에서 Top-K 후보 500 / 1000 / 2000 / 5000 및 여러 `l1_ratio` 조합을 Train 5-fold CV로 비교
* RNA-only CoxNet 최종 설정 확정

  * Top-K = 1000
  * `l1_ratio = 0.75`
  * `alpha_idx = 27`
  * Train 5-fold CV mean C-index = 0.7380 ± 0.0535
  * Validation C-index = 0.726262
  * 최종 non-zero genes = 144
* Clinical feature preprocessing 완료

  * 최종 input features = 10
* Clinical-only CoxNet Train 5-fold CV 수행

  * `l1_ratio = 0.90`
  * `alpha_idx = 37`
  * Train 5-fold CV mean C-index = 0.8220 ± 0.0509
  * Validation C-index = 0.784003
  * 최종 non-zero clinical features = 8
* Clinical+RNA CoxNet 구축 및 tuning 완료

  * Clinical 10 features + RNA Top-500 = 총 510 input features
  * Top-K = 500
  * `l1_ratio = 0.50`
  * `alpha_idx = 18`
  * Validation C-index = 0.813516
  * 최종 non-zero coefficients = 24

    * Clinical: 3
    * RNA: 21
* Clinical+RNA non-zero RNA genes에 대한 annotation 결과 저장
* MSigDB Human Hallmark gene set 확보

  * Hallmark 50 gene sets 사용
* Hallmark pathway score pipeline 구축 및 leakage audit 수행
* Clinical+Hallmark CoxNet 구축

  * Clinical 10 + Hallmark 50 = 총 60 input features
  * `l1_ratio = 0.75`
  * `alpha_idx = 31`
  * Validation C-index = 0.773311
  * 최종 non-zero coefficients = 14
* Validation 기반 모델 선택 및 specification 고정 후 untouched Test set 평가 수행
* 4개 모델의 Test Harrell C-index 계산
* Test set에서 Uno C 및 1-year / 3-year time-dependent AUC 평가 수행
* Test set에서 Brier score / Integrated Brier Score 평가 수행
* grouped calibration diagnostic 수행
* Clinical+RNA와 Clinical-only 모델 간 paired bootstrap 비교 수행

  * 5,000 bootstrap repetitions
* 결과 visualization notebook 생성 및 주요 figure 4개 생성
* Python/scikit-learn 관련 환경 문제 해결 후 모델링 파이프라인 정상 실행 완료
* XAI 방향은 CoxNet coefficient 기반 global interpretation, Hallmark pathway interpretation, patient-level feature contribution을 핵심으로 하고 SHAP은 optional로 두기로 정리

### 3. 주요 결과

* Primary modeling cohort: 529 patients

* PFI event distribution

  * event=0: 370
  * event=1: 159

* Fixed Train / Validation / Test split

  * Train: 370

    * events: 111
  * Validation: 79

    * events: 24
  * Test: 80

    * events: 24

* RNA preprocessing

  * Raw protein-coding genes: 19,962
  * Low-expression filtering 후: 14,220 genes

* Validation C-index

  * RNA-only: 0.726262
  * Clinical-only: 0.784003
  * Clinical+RNA: 0.813516
  * Clinical+Hallmark: 0.773311

* Test Harrell C-index

  * RNA-only: 0.714511
  * Clinical-only: 0.886830
  * Clinical+RNA: 0.891956
  * Clinical+Hallmark: 0.885647

* Test 3-year Uno C

  * RNA-only: 0.7032
  * Clinical-only: 0.8798
  * Clinical+RNA: 0.8970
  * Clinical+Hallmark: 0.8682

* Clinical+RNA vs Clinical-only Test Harrell C-index

  * ΔC = +0.005126
  * paired bootstrap 95% CI = -0.024295 ~ +0.044045
  * CI에 0이 포함되므로 RNA 추가에 따른 Test C-index 향상은 현재 결과에서 명확한 개선으로 단정하지 않음

* Non-zero coefficients

  * RNA-only: 144 genes
  * Clinical-only: 8 features
  * Clinical+RNA: 24 features

    * Clinical 3
    * RNA 21
  * Clinical+Hallmark: 14 features

* 추가 평가 완료

  * 1-year / 3-year time-dependent AUC
  * Brier score / IBS
  * grouped calibration diagnostic
  * bootstrap confidence interval

* Result visualization

  * Harrell C-index + bootstrap CI figure 생성
  * time-dependent AUC figure 생성
  * paired ΔC bootstrap CI figure 생성
  * IBS figure 생성
  * calibration diagnostic 자체는 완료했지만 별도 calibration figure는 아직 생성하지 않음

### 4. 생성/수정된 파일

* `notebooks/02_split_preprocessing.ipynb`

  * Train-based RNA preprocessing, feature selection 및 CoxNet 모델링 작업에 사용된 notebook

* `notebooks/03_results_visualization.ipynb`

  * 최종 evaluation 결과 및 figure 생성 notebook

* `data/external/msigdb/h.all.v2026.1.Hs.symbols.gmt`

  * MSigDB Human Hallmark 50 gene sets

* `data/processed/rna_coxnet_coefficients.csv`

  * RNA-only CoxNet coefficient 결과

* `data/processed/rna_coxnet_nonzero_genes.csv`

  * RNA-only CoxNet의 non-zero 144 genes

* `data/processed/clinical_coxnet_coefficients.csv`

  * Clinical-only CoxNet coefficient 결과

* `data/processed/clinical_coxnet_nonzero_features.csv`

  * Clinical-only CoxNet non-zero features

* `data/processed/clinical_rna_coxnet_coefficients.csv`

  * Clinical+RNA CoxNet coefficient 결과

* `data/processed/clinical_rna_coxnet_nonzero_features.csv`

  * Clinical+RNA CoxNet non-zero feature 결과

* `data/processed/clinical_rna_nonzero_genes_annotated.csv`

  * Clinical+RNA non-zero RNA genes annotation 결과

* `data/processed/clinical_pathway_coxnet_coefficients.csv`

  * Clinical+Hallmark CoxNet coefficient 결과

* `data/processed/clinical_pathway_coxnet_nonzero_features.csv`

  * Clinical+Hallmark CoxNet non-zero feature 결과

* `data/processed/clinical_pathway_cv_audit.csv`

  * Clinical+Hallmark pipeline의 CV / leakage audit 결과

* `data/processed/final_model_specifications.csv`

  * 최종 frozen model별 parameter 및 specification 기록

* `data/processed/test_predictions.csv`

  * untouched Test set에 대한 최종 model prediction 결과

* `data/processed/test_harrell_c_bootstrap_ci.csv`

  * 모델별 Test Harrell C-index bootstrap confidence interval 결과

* `data/processed/test_harrell_c_difference_ci.csv`

  * 모델 간 paired Harrell C-index difference bootstrap 결과

* `data/processed/test_discrimination_metrics.csv`

  * Harrell C, Uno C, time-dependent AUC 관련 discrimination metrics

* `data/processed/test_brier_ibs_metrics.csv`

  * Brier score 및 Integrated Brier Score 결과

* `data/processed/test_grouped_calibration.csv`

  * grouped calibration diagnostic 결과

* `data/processed/final_performance_summary.csv`

  * 최종 4개 모델 performance summary

* `reports/figures/fig1_test_harrell_cindex_ci.png`

  * Test Harrell C-index 및 95% bootstrap CI

* `reports/figures/fig2_time_dependent_auc.png`

  * 1-year / 3-year time-dependent AUC 비교

* `reports/figures/fig3_paired_cindex_difference_ci.png`

  * paired ΔC 및 bootstrap 95% CI

* `reports/figures/fig4_integrated_brier_score.png`

  * 모델별 Integrated Brier Score 비교

* `reports/project_plan.md`

  * 2026-09-28까지 4-model evaluation, XAI, Molecular Twin, OOD, Streamlit을 포함하도록 프로젝트 최종 범위 및 일정 갱신

* `notebooks/04_xai_interpretation.ipynb`

  * CoxNet global/local XAI 및 biological interpretation을 수행하기 위한 notebook
  
### 5. 오늘 결정한 분석 기준

* 분석 단위는 patient-level 유지
* Primary endpoint는 PFI 유지
* Primary modeling cohort는 529명으로 고정
* Train / Validation / Test = 370 / 79 / 80 유지
* `pfi_event` 기준 stratified split 및 random seed 42 유지
* 모든 모델은 동일한 patient split을 사용
* Test set은 hyperparameter tuning이나 feature selection에 사용하지 않음
* RNA low-expression filtering은 Train 기준으로 수행
* RNA transform은 `log2(TPM + 1)` 사용
* 고차원 RNA feature selection은 CV fold 내부에서 다시 fit하여 validation fold 정보가 preprocessing에 유입되지 않도록 함
* RNA CoxNet에서는 MAD 기반 Top-K feature selection 사용
* Clinical / RNA / Clinical+RNA / Clinical+Hallmark 네 모델을 동일 평가 프레임워크에서 비교
* 최종 모델 specification은 Validation 기준으로 결정한 후 frozen 상태에서 Test를 평가
* Test 결과를 확인한 이후 해당 결과에 맞추어 hyperparameter나 feature selection을 다시 수정하지 않음
* 성능 평가는 Harrell C-index만으로 제한하지 않고 Uno C, 1y/3y time-dependent AUC, Brier/IBS, calibration을 함께 사용
* Clinical+RNA의 성능 향상 여부는 단일 C-index 차이만으로 판단하지 않고 paired bootstrap CI를 함께 확인
* XAI는 다음을 핵심으로 진행

  * CoxNet coefficient 기반 global explanation
  * Hallmark pathway-level biological interpretation
  * patient-level feature contribution
* SHAP은 필수 항목이 아니라 일정이 허용될 경우 추가하는 optional 분석으로 둠

### 6. 확인해야 할 문제 / 미완료

* [ ] XAI 분석 시작

  * Clinical+RNA를 primary explanation model로 사용
  * global coefficient interpretation
  * clinical / RNA feature 방향성 및 magnitude 정리
  * Hallmark pathway biological interpretation

* [ ] Patient-level local contribution 계산

  * `standardized feature × coefficient` 기반 contribution 산출
  * 현재 별도 scaler / preprocessing artifact 파일이 확인되지 않으므로 Train preprocessing을 정확히 재현할 방법부터 정리 필요
  * Test 데이터 자체로 mean / SD를 다시 계산하지 않도록 주의

* [ ] `notebooks/04_xai_interpretation.ipynb` 생성 및 XAI 결과 저장

* [ ] calibration diagnostic의 presentation용 figure 생성 여부 결정

* [ ] inference pipeline 함수화

  * patient input → preprocessing → risk score → explanation 흐름으로 정리

* [ ] Molecular Twin MVP 구현

  * Train reference patients 기준 top-k similar patient retrieval

* [ ] Train-distribution 기반 OOD score 및 warning 구현

* [ ] Streamlit에서 risk prediction / XAI / Molecular Twin / OOD를 end-to-end로 연결

* [ ] README 및 최종 portfolio documentation 작성


### 7. GitHub 상태

- Commit: ✅
- Push: ✅
- Commit message: `complete four-model evaluation and update progress log`

### 8. 현재 프로젝트 진행 위치

Clinical / RNA cohort 구축 ✅
→ Primary modeling cohort 529명 확정 ✅
→ Train / Validation / Test split 및 QC ✅
→ Leakage-safe RNA preprocessing ✅
→ RNA CoxNet ✅
→ Clinical CoxNet ✅
→ Clinical+RNA CoxNet ✅
→ Hallmark pathway pipeline ✅
→ Clinical+Hallmark CoxNet ✅
→ Validation 기반 model selection / freeze ✅
→ Untouched Test 평가 ✅
→ Bootstrap / Uno C / td-AUC / Brier-IBS / calibration ✅
→ Result visualization ✅
→ **XAI / patient-level explanation ← 현재 위치**
→ Inference pipeline 함수화
→ Molecular Twin
→ OOD detection
→ Streamlit demo
→ README / portfolio packaging

### 9. 다음 작업

1. `notebooks/04_xai_interpretation.ipynb`에서 frozen Clinical+RNA model의 feature 구조 재확인
   - `final_model_specifications.csv`
   - Clinical+RNA coefficient 파일
   - annotated non-zero gene 파일 불러오기

2. Clinical+RNA의 non-zero 24개 feature를 Clinical 3개 / RNA 21개로 구분하고 coefficient sign 및 magnitude 기반 global XAI table 작성

3. RNA 21개 gene을 gene symbol 및 Hallmark pathway와 연결하여 biological interpretation 정리

4. Clinical+Hallmark의 non-zero 14개 feature에 대해 coefficient 방향성과 주요 pathway 의미 정리

5. Train preprocessing을 동일하게 재현할 수 있도록 patient-level inference preprocessing pipeline 정리
   - Test 데이터 자체에서 mean / SD 등을 다시 계산하지 않도록 주의
   - Train에서 결정된 preprocessing 기준만 사용

6. 환자별 `standardized feature × coefficient` contribution 계산
   - risk score에 기여하는 positive top features
   - risk score를 낮추는 negative top features
   - 환자별 explanation 결과 생성

7. XAI 결과를 Streamlit에서도 재사용할 수 있도록 table / function / artifact 형태로 저장

8. XAI 완료 후 Molecular Twin용 feature space 확정
   - Train 환자를 reference로 사용
   - query patient와의 similarity 계산
   - top-k similar patients 반환

9. Train distribution을 기준으로 OOD score 및 warning threshold 구현
   - Test set을 threshold 결정에 사용하지 않음

10. prediction → XAI → Molecular Twin → OOD를 하나의 inference pipeline으로 연결

11. Streamlit에서
    - 환자 선택
    - risk score
    - XAI
    - similar patients
    - OOD warning
    순서로 end-to-end demo 구현

## 2026-09-23

### 1. 오늘의 목표

* [x] Clinical+RNA frozen CoxNet 기반 Global XAI 수행
* [x] Clinical+RNA preprocessing 및 frozen model 재현성 검증
* [x] Patient-level feature contribution 계산
* [x] Low / Middle / High-risk 대표 환자 선정
* [x] Clinical+RNA Local XAI 수행
* [ ] Clinical-only XAI
* [ ] Clinical+Hallmark XAI
* [ ] RNA gene biological interpretation

### 2. 오늘 완료한 작업

* `04_xai_interpretation.ipynb`에서 Clinical+RNA XAI 진행

* Clinical+RNA 모델의 non-zero feature 24개 확인
  * Clinical: 3개
  * RNA: 21개

* Clinical+RNA Global XAI 완료
  * CoxNet coefficient의 sign과 magnitude를 이용하여 각 feature의 risk 방향과 상대적 영향 확인
  * Clinical feature와 RNA feature를 구분하여 시각화
  * Global XAI Figure 5 생성

* 기존 Clinical+RNA preprocessing pipeline 재현
  * Train cohort: 370 patients
  * Test cohort: 80 patients
  * low-expression filtering 후 RNA: 14,220 genes
  * MAD 기반 Top-500 gene selection
  * Clinical 10 + RNA 500 = 총 510 input features
  * 기존 frozen model과 동일한 preprocessing 및 feature structure 재구성

* Frozen Clinical+RNA model 재현성 확인
  * 기존 frozen model과 재구성 model의 coefficient 차이 ≈ 0
  * 기존 `test_predictions.csv`와 재계산한 Test risk score 차이 ≈ 0
  * 기존 분석에서 확정한 frozen model을 정상적으로 재현했음을 확인

* Patient-level Local XAI 구현
  * Test 환자별로 `standardized feature × coefficient` contribution 계산
  * Clinical+RNA model의 non-zero 24개 feature를 대상으로 환자별 contribution 산출
  * 각 feature contribution의 합으로 Cox linear predictor를 재구성하여 기존 risk score와 일치함을 확인

* Test cohort에서 대표 환자 3명 선정
  * Low-risk patient
  * Middle-risk patient
  * High-risk patient

* Clinical+RNA Local XAI 완료
  * 대표 환자별 risk 증가 방향 contribution과 risk 감소 방향 contribution 확인
  * Low / Middle / High-risk 환자의 feature contribution을 비교할 수 있도록 시각화
  * Local XAI Figure 6 생성

### 3. 주요 결과

* Clinical+RNA Global XAI: 완료

* Clinical+RNA Local XAI: 완료

* Clinical+RNA frozen model non-zero features
  * 총 24개
  * Clinical: 3개
  * RNA: 21개

* Clinical+RNA preprocessing 재현
  * low-expression filtering 후: 14,220 genes
  * MAD Top-K: 500 genes
  * Clinical: 10 features
  * 최종 model input: 510 features

* Frozen model reproducibility
  * coefficient difference ≈ 0
  * Test risk-score difference ≈ 0

* Patient-level explanation
  * 각 환자의 Cox risk score를 `standardized feature × coefficient` contribution으로 직접 분해
  * Test 환자별 non-zero 24개 feature contribution 계산
  * contribution 합으로 기존 frozen model의 risk score를 재현

* Local XAI 대표 환자
  * Low-risk
  * Middle-risk
  * High-risk
  * 총 3명 선정

* Figure 생성
  * Figure 5: Clinical+RNA Global XAI
  * Figure 6: Clinical+RNA Local XAI

### 4. 생성/수정된 파일

* `notebooks/04_xai_interpretation.ipynb`

  * Clinical+RNA frozen CoxNet의 Global / Local XAI 및 model reproducibility 검증

* `reports/figures/fig5_clinical_rna_nonzero_coefficients.png`

  * Clinical+RNA CoxNet의 non-zero 24개 feature에 대한 coefficient 기반 Global XAI

* `reports/figures/fig6_clinical_rna_local_explanations.png`

  * Low / Middle / High-risk 대표 Test 환자 3명의 patient-level Local XAI

* `reports/figures/fig6_high_risk_local_contributions.png`

  * High-risk 대표 환자의 feature contribution Local XAI

* `reports/figures/fig6_middle_risk_local_contributions.png`

  * Middle-risk 대표 환자의 feature contribution Local XAI

* `reports/figures/fig6_low_risk_local_contributions.png`

  * Low-risk 대표 환자의 feature contribution Local XAI

### 5. 오늘 결정한 분석 기준

* XAI 과정에서도 기존 frozen model을 유지하고 재학습하지 않음

* Clinical+RNA model의 Global XAI는 CoxNet coefficient를 직접 이용
  * coefficient > 0: 높은 Cox linear predictor 방향
  * coefficient < 0: 낮은 Cox linear predictor 방향
  * coefficient magnitude: standardized model scale에서 상대적 영향 확인

* Patient-level Local XAI는 별도의 surrogate model을 사용하지 않고 CoxNet 자체의 additive structure를 이용

* 환자별 Local contribution은 다음과 같이 정의

  `contribution_j = standardized feature_j × coefficient_j`

* 전체 feature contribution의 합이 해당 환자의 Cox linear predictor를 재현하는지 확인하여 Local XAI 계산의 정확성을 검증

* Test cohort는 XAI를 위한 모델 재학습이나 feature selection에 사용하지 않음

* Local XAI presentation을 위해 Test cohort에서 Low / Middle / High-risk 대표 환자 3명을 선정

* SHAP을 필수 분석으로 추가하지 않고 CoxNet의 직접적인 coefficient / contribution 기반 설명을 primary XAI 방법으로 유지

### 6. 확인해야 할 문제 / 미완료

* [ ] Clinical-only XAI
  * Clinical-only CoxNet의 non-zero clinical features 해석
  * coefficient 기반 Global XAI 정리

* [ ] Clinical+Hallmark XAI
  * non-zero Hallmark / clinical feature 확인
  * pathway coefficient 방향 및 magnitude 해석
  * pathway-level visualization 생성

* [ ] RNA gene biological interpretation
  * Clinical+RNA non-zero RNA 21개 gene의 biological relevance 조사
  * KIRC / cancer progression과 관련된 기존 연구 근거 확인
  * 과도한 인과적 해석을 피하고 모델 association과 기존 biological evidence를 구분하여 기술

* [ ] XAI 결과를 Streamlit / inference pipeline에서 재사용할 수 있도록 artifact 및 function 형태로 정리

* [ ] Molecular Twin 구현

* [ ] Train distribution 기반 OOD detection 구현

* [ ] prediction → XAI → Molecular Twin → OOD inference pipeline 연결

* [ ] Streamlit end-to-end demo 구현

* [ ] README 및 최종 portfolio documentation 작성

### 7. GitHub 상태

* Commit: ✅

* Push: ✅

* Commit message: `complete clinical RNA XAI analysis`

### 8. 현재 프로젝트 진행 위치

Cohort / Split / QC ✅  
→ RNA preprocessing ✅  
→ RNA-only CoxNet ✅  
→ Clinical-only CoxNet ✅  
→ Clinical+RNA CoxNet ✅  
→ Clinical+Hallmark CoxNet ✅  
→ Validation model selection / freeze ✅  
→ Untouched Test evaluation ✅  
→ Bootstrap / Uno C / td-AUC / Brier-IBS / calibration ✅  
→ Result visualization ✅  
→ Clinical+RNA Global XAI ✅  
→ Clinical+RNA Local XAI ✅  
→ **Clinical-only XAI ← 현재 위치**  
→ Clinical+Hallmark XAI  
→ RNA gene biological interpretation  
→ Molecular Twin  
→ OOD detection  
→ Inference pipeline  
→ Streamlit demo  
→ README / 최종 패키징

### 9. 다음 작업

1. `notebooks/04_xai_interpretation.ipynb`에서 Clinical-only CoxNet XAI 진행
   * non-zero clinical feature 확인
   * coefficient sign / magnitude 해석
   * 필요 시 Clinical-only Global XAI figure 생성

2. Clinical+Hallmark CoxNet XAI 진행
   * non-zero clinical / Hallmark features 확인
   * 주요 Hallmark pathway의 coefficient 방향과 magnitude 분석
   * pathway-level XAI figure 생성

3. Clinical+RNA의 non-zero RNA 21개 gene에 대한 biological interpretation 수행
   * gene symbol 확인
   * KIRC 및 cancer progression 관련 근거 조사
   * 모델에서 관찰된 association과 기존 biological evidence를 구분하여 정리

4. Clinical+RNA / Clinical-only / Clinical+Hallmark XAI 결과를 하나의 해석 구조로 정리

5. XAI 결과를 이후 Streamlit에서 사용할 수 있도록 reusable artifact / function 형태로 정리

6. XAI 완료 후 Molecular Twin용 feature space 확정
   * Train patients를 reference cohort로 사용
   * patient similarity 계산
   * top-k similar patients 반환

7. Train distribution 기반 OOD score 및 warning threshold 구현
   * Test cohort를 threshold 결정에 사용하지 않음

8. risk prediction → XAI → Molecular Twin → OOD를 하나의 patient-level inference pipeline으로 연결

9. Streamlit에서 patient 선택 → risk prediction → explanation → similar patients → OOD warning의 end-to-end demo 구현

# Project Progress Log

## 2026-09-24

### 1. 오늘의 목표

* [x] 최종 분석 결과 정리 및 README 작성
* [x] Frozen Clinical+RNA inference artifacts 저장 및 재현성 검증
* [x] Patient-level inference pipeline 구축
* [x] Molecular Twin / support 정보를 inference에 연결
* [x] Streamlit 데모 구축 및 정상/low-support case 검증
* [x] Git commit / push
* [ ] Streamlit UI 최종 마무리
* [ ] 전체 프로젝트 최종 QC
* [ ] 발표자료 제작

### 2. 오늘 완료한 작업

* `notebooks/07_final_results_summary.ipynb`에서 최종 분석 결과를 정리하고 GitHub에 반영.
* `README.md`를 작성하여 프로젝트 목적, 분석 pipeline, 주요 결과 및 실행 구조를 정리하고 GitHub에 반영.
* 최종 Clinical+RNA 모델의 **frozen inference artifacts 5개**를 저장.
* 저장된 artifacts를 다시 불러와 기존 prediction과 비교:

  * Risk difference = **0.0**
  * 저장/재로드 후 prediction이 정확히 재현됨을 확인.
* `src/patient_inference.py` 구축:

  * 학습 notebook과 독립적으로 frozen artifacts를 이용한 patient-level inference가 가능하도록 구현.
  * `TCGA-BP-5169`에서 risk score **0.877533...**를 정확히 재현.
* Molecular Twin / support 정보를 inference pipeline에 연결.
* `app.py`를 작성하여 Streamlit patient-level prediction demo 구축.
* Streamlit **1.64.0** 설치 및 실행 확인.
* 정상-support 환자에서 inference 및 UI 정상 작동 확인.
* Low-support case 검증:

  * Patient: `TCGA-B0-5694`
  * Similarity: **0.304**
  * Low-support threshold: **0.381**
  * `0.304 < 0.381`에서 warning이 정상적으로 표시됨.
* 오늘 작업에 대한 Git commit / push 완료.

### 3. 주요 결과

* 기존 분석/모델링/XAI 결과를 실제 환자 inference에 사용할 수 있는 형태로 연결 완료.
* 최종 Clinical+RNA 모델:

  * Input: Clinical 10 + RNA Top-500 = **510 features**
  * Non-zero coefficients: **24 (Clinical 3 + RNA 21)**
  * Test Harrell C-index: **0.8920**
  * Test Uno C-index (3y): **0.8970**
  * AUC 1y / 3y: **0.8797 / 0.9440**
  * IBS 1–3y: **0.0992**
* Clinical+RNA vs Clinical-only:

  * ΔC = **+0.005126**
  * 95% CI = **-0.024295 ~ +0.044045**
  * RNA 추가에 따른 명확하고 일관된 incremental discrimination benefit은 확인되지 않음.
* Frozen artifact reload:

  * Risk difference = **0.0**
* Independent inference:

  * `TCGA-BP-5169` risk = **0.877533...**
* Low-support detection:

  * `TCGA-B0-5694`: similarity **0.304 < 0.381**
  * Warning 정상 작동.
* 분석 결과 → frozen model → independent inference → support 판단 → Streamlit UI까지 하나의 재사용 가능한 pipeline으로 연결 완료.

### 4. 생성/수정된 파일

* `notebooks/07_final_results_summary.ipynb`

  * 프로젝트 최종 분석 결과 요약 notebook.

* `README.md`

  * 프로젝트 목적, 방법, 결과 및 실행 구조 문서.

* Frozen Clinical+RNA inference artifacts 5개

  * 최종 모델과 preprocessing을 독립 inference에서 동일하게 재사용하기 위한 저장 artifacts.
  * 개별 파일명/경로는 현재 기록에서 확인되지 않아 임의 기재하지 않음.

* `src/patient_inference.py`

  * Frozen artifacts 기반 patient-level risk 및 support inference module.

* `app.py`

  * Patient-level inference를 실행하고 결과 및 low-support warning을 표시하는 Streamlit application.

* `reports/progress_log.md`

  * 2026-09-24 작업 내용 추가.

### 5. 오늘 결정한 분석 기준

* 기존 529명 primary modeling cohort, PFI endpoint, Train/Validation/Test split 및 frozen model specification을 변경하지 않음.
* Test 결과 확인 이후 feature/model/hyperparameter를 재선택하지 않음.
* 신규 환자 prediction에서는 모델을 다시 학습하지 않고 **저장된 frozen preprocessing/model artifacts를 그대로 사용**.
* Artifact 저장 후 prediction reproducibility를 반드시 확인하며 오늘 risk difference **0.0**을 검증.
* Molecular Twin similarity는 prediction 자체를 변경하는 값이 아니라 **training cohort 내 support 정도를 나타내는 보조 정보**로 사용.
* Similarity가 low-support threshold보다 낮은 경우 UI에서 별도 warning을 표시.
* Clinical+RNA의 관측 discrimination이 높더라도 paired bootstrap 및 IBS 결과를 함께 고려하여 RNA의 추가 예측 가치를 과장하지 않음.

### 6. 확인해야 할 문제 / 미완료

* [ ] Streamlit UI 레이아웃 및 설명 문구 최종 정리
* [ ] 정상-support / low-support / 잘못된 입력에 대한 전체 demo flow QC
* [ ] Frozen artifacts 5개의 실제 파일명·경로 및 dependency 최종 확인
* [ ] `README.md`의 실행 방법과 최종 Streamlit 실행 과정 일치 여부 확인
* [ ] 프로젝트 전체 notebook → processed data → artifact → inference 연결 관계 최종 QC
* [ ] 발표용 핵심 figure/table 선정
* [ ] 발표자료 제작 및 시연 시나리오 준비

### 7. GitHub 상태
- Commit: 완료
- Commit hash: `eaadd50`
- Push: 완료
- Commit message: `Add Streamlit patient inference demo`
- 반영 파일:
  - `app.py`
  - `src/patient_inference.py`
- Branch: `main`
- Remote 상태: `origin/main`과 동기화 완료
- Remaining uncommitted changes:
  - `notebooks/03_results_visualization.ipynb`
  - `notebooks/04_xai_interpretation.ipynb`

현재 working tree는 clean하지 않음.
위 두 notebook의 변경사항을 확인한 뒤 별도 commit 여부를 결정해야 함.

### 8. 현재 프로젝트 진행 위치

```text
Data / Cohort
→ Preprocessing
→ Modeling / CV
→ Final Test Evaluation
→ XAI
→ Molecular Twin / Support
→ Frozen Model Artifacts
→ Patient-level Inference
→ Final Results Summary
→ README
→ Streamlit 핵심 기능 구현·검증
                         ↑ 모두 완료
→ [현재] Streamlit UI 마무리
→ 전체 프로젝트 최종 QC
→ 발표자료 제작
→ 최종 발표
```

### 9. 다음 작업

1. `app.py`의 Streamlit UI를 최종 정리하고 개발용 출력 제거.
2. 정상-support 환자와 `TCGA-B0-5694` low-support 환자로 전체 demo flow 재검증.
3. 누락/잘못된 입력에 대한 예외처리 확인.
4. Frozen artifacts → `patient_inference.py` → `app.py` 연결을 최종 smoke test.
5. README 실행 방법과 실제 실행 과정을 대조하여 필요한 부분만 수정.
6. 프로젝트 전체 결과 파일 및 notebook 연결 관계를 최종 QC하고 분석 코드를 freeze.
7. 발표에 사용할 핵심 성능 결과, XAI 결과, patient inference 및 support-warning 화면을 선정.
8. 발표자료 제작 및 실제 시연 순서 준비.

## 2026-09-25

### 1. 오늘의 목표

- [x] New Patient inference pipeline 구현
- [x] Streamlit New Patient 입력 기능 구현
- [x] 기존 Test-patient pipeline과 New Patient pipeline parity QC
- [x] Streamlit end-to-end inference QC
- [x] New Patient 관련 코드 GitHub 반영

### 2. 오늘 완료한 작업

- `src/patient_inference.py`에 실제 신규 환자를 위한 inference pipeline 추가
- 신규 환자 Clinical 입력 변수 확정
  - age
  - gender
  - stage
  - grade
- 신규 환자의 RNA TPM 데이터를 입력받아 frozen preprocessing을 적용하도록 구현
- 기존 Train-derived artifact만 사용하도록 구성
  - frozen clinical preprocessor
  - frozen combined scaler
  - frozen Clinical+RNA CoxNet
- 신규 환자의 patient-level feature contribution 계산 구현
- Molecular Twin을 신규 환자에 대해 실시간 계산하도록 구현
- Train reference와 cosine similarity를 이용해 Top-5 Molecular Twin 검색
- Train-derived molecular support threshold를 이용한 low-support warning 구현
- Molecular Twin 검색 후 Train 환자의 clinical/PFI metadata를 retrospective information으로 연결
- Streamlit에 두 가지 inference mode 구현
  - Existing TCGA Test Patient
  - New Patient
- New Patient mode에 Clinical 입력 UI 및 RNA TPM CSV 업로드 기능 추가

### 3. 주요 결과

#### New Patient parity QC

기존 Test 환자 `TCGA-BP-5169`를 신규 환자 입력처럼 사용하여 기존 pipeline과 비교함.

- Existing pipeline risk score: `0.8775333495883141`
- New Patient pipeline risk score: `0.8775333629488457`
- Absolute difference: `1.3360531569972522e-08`

Molecular Support 비교:

- Existing maximum similarity: `0.65425265`
- New Patient maximum similarity: `0.6542525913044144`
- Nearest Train patient: `TCGA-BP-4799` (동일)
- Existing low-support: `False`
- New Patient low-support: `False`

New Patient Top-5 Molecular Twins:

1. TCGA-BP-4799 — 0.654253
2. TCGA-BP-4352 — 0.585815
3. TCGA-B8-A54I — 0.585734
4. TCGA-G6-A8L7 — 0.582847
5. TCGA-BP-4761 — 0.568247

Risk score 차이는 약 `1.34e-08`로 부동소수점 계산 수준이며,
기존 inference와 신규 환자 inference가 사실상 동일한 결과를 재현함을 확인함.

#### Streamlit end-to-end QC

`TCGA-BP-5169`의 실제 RNA TPM 19,962 genes를 CSV로 생성하여
Streamlit New Patient mode에 업로드함.

Clinical input:

- age: 70
- gender: MALE
- stage: Stage I
- grade: G4

Streamlit 결과:

- Clinical+RNA CoxNet risk score: `0.878`
- Nearest Train patient: `TCGA-BP-4799`
- Maximum RNA similarity: `0.654`
- Molecular support threshold: `0.381`
- Molecular support: supported

CLI parity 결과와 Streamlit 결과가 일치함을 확인함.

### 4. 생성/수정된 파일

- `app.py`
  - Existing TCGA Test Patient / New Patient mode 구현
  - Clinical 입력 UI
  - RNA TPM CSV upload
  - 신규 환자 prediction 결과 표시

- `src/patient_inference.py`
  - `preprocess_new_patient()`
  - `calculate_new_patient_twins()`
  - `predict_new_patient()`
  - Molecular Twin retrospective metadata 연결

- `TCGA-BP-5169_tpm.csv`
  - Streamlit end-to-end QC용 임시 파일
  - QC 완료 후 삭제
  - GitHub에는 포함하지 않음

### 5. 오늘 결정한 분석 기준

- 신규 환자 Clinical 입력은 frozen model이 실제 사용하는 4개 변수만 사용
  - age
  - gender
  - stage
  - grade
- gender category:
  - FEMALE
  - MALE
- stage category:
  - Stage I
  - Stage II
  - Stage III
  - Stage IV
  - Unknown
- grade category:
  - G1
  - G2
  - G3
  - G4
  - Unknown
- 신규 환자 inference 과정에서 preprocessing/model fitting을 다시 수행하지 않음
- Train-derived frozen preprocessing/model artifact만 사용
- Molecular Twin similarity는 RNA expression만 사용
- Clinical/PFI 정보는 similarity 검색 이후 retrospective information으로만 표시
- Molecular support warning은 formal OOD classifier가 아닌 Train-distribution similarity heuristic으로 해석
- CoxNet risk score는 absolute probability가 아닌 relative linear predictor로 표시

### 6. 확인해야 할 문제 / 미완료

- `notebooks/03_results_visualization.ipynb` 수정사항 검토 필요
- `notebooks/04_xai_interpretation.ipynb` 수정사항 검토 필요
- README에 New Patient 입력 방법 및 RNA CSV 형식 반영 필요
- 최종 reproducibility / repository cleanup 필요
- 발표용 Streamlit demo flow 최종 점검 필요

### 7. GitHub 상태

New Patient 기능 관련 다음 파일은 commit/push 완료:

- `app.py`
- `src/patient_inference.py`

기존 작업 중인 notebook은 이번 commit에서 제외:

- `notebooks/03_results_visualization.ipynb`
- `notebooks/04_xai_interpretation.ipynb`

### 8. 현재 프로젝트 진행 위치

Data preparation
→ Cohort / Split
→ Leakage-safe preprocessing
→ 4-model training
→ Validation model selection
→ Untouched Test evaluation
→ Calibration / visualization
→ Global XAI
→ Patient-level XAI
→ Molecular Twin
→ Molecular Support warning
→ Existing-patient Streamlit
→ **New Patient inference + Streamlit + end-to-end QC 완료**
→ README / reproducibility cleanup
→ Final presentation preparation

### 9. 다음 작업

1. README에 New Patient 기능과 RNA 입력 형식 추가
2. 남아 있는 `03_results_visualization.ipynb`, `04_xai_interpretation.ipynb` 변경사항 검토
3. repository reproducibility / cleanup
4. 최종 Streamlit demo 시나리오 점검
5. 발표용 핵심 결과 및 프로젝트 설명 정리

응. 아래를 **`reports/progress_log.md`의 기존 내용 맨 아래에 2026-09-28 기록으로 그대로 추가**하면 돼. 네가 작성한 내용에 어제 실제로 했던 **교육원 PC 결과파일 회수, Git 통합, 최신 작업 pull, Streamlit 실행 실패 원인 확인**까지 반영해서 수정했어. 

응. 아래 버전으로 쓰면 돼. **`집 PC / 교육원 PC` 같은 개인적인 작업환경 표현은 전부 제거**하고, Git·artifact·deployment 관점에서 전문적으로 정리했어.

기존 `progress_log.md`의 이전 날짜는 건드리지 말고 **맨 아래에 그대로 추가**하면 돼.

## 2026-09-28

### 1. 오늘의 목표

- TCGA-KIRC 프로젝트 최종 결과 및 repository 상태 점검
- Git 비추적 상태로 남아 있던 최종 모델 coefficient / performance 결과 회수
- 로컬 및 원격 repository의 최신 작업 통합
- 최종 발표 흐름 및 슬라이드 구성 정리
- 기존 프로젝트 결과를 발표용 스토리라인에 맞게 재구성
- `README.md` 최종 수정
- Streamlit demo의 별도 실행 환경 재현 가능 여부 점검
- 최종 발표 전 repository 및 demo 환경 QC

### 2. 오늘 완료한 작업

- repository 및 Git 상태를 점검함.
- `data/processed/`에 존재하지만 Git에서 추적되지 않던 최종 모델 및 성능 관련 CSV를 확인함.
- `git ls-files data/processed/*.csv` 결과가 비어 있음을 확인하여 해당 결과 파일들이 Git 추적 대상이 아님을 확인함.
- 최종 결과 보존을 위해 필요한 coefficient / performance CSV 18개를 `results/`로 복사하고 Git 추적 대상으로 추가함.
- 원격 repository의 최신 변경사항을 pull하여 기존 로컬 결과와 통합함.
- merge conflict 없이 정상적으로 병합됨.
- 다음 최신 분석 및 서비스 구현 결과가 repository에 정상적으로 통합된 것을 확인함.
  - Molecular Twin / Molecular Support
  - OOD
  - Patient-level inference
  - Streamlit prototype
  - `notebooks/05_molecular_twin_ood.ipynb`
  - `notebooks/06_patient_inference.ipynb`
  - `notebooks/07_final_results_summary.ipynb`
  - `src/patient_inference.py`
  - `app.py`
  - 관련 `results/` 산출물
- 결과 파일 통합 이후 GitHub push를 완료하고 당시 repository가 `origin/main`과 동기화된 clean 상태임을 확인함.
- 기존 TCGA-KIRC 분석 결과를 기반으로 최종 발표자료 구성 작업을 진행함.
- 발표에서 단순 성능 나열이 아니라 다음 흐름이 드러나도록 프로젝트 스토리를 재구성함.
  - PFI 예후 예측 문제 정의
  - Clinical / RNA-seq 데이터 구성 및 전처리
  - 4개 모델 비교
  - 최종 Clinical+RNA 모델 평가
  - Global / Local XAI
  - Molecular Twin / Molecular Support
  - OOD
  - Frozen model 기반 patient-level inference
  - Streamlit demo
- Clinical+RNA가 관측상 가장 높은 Test discrimination을 보였지만 Clinical-only 대비 paired bootstrap ΔC의 95% CI가 0을 포함한다는 해석을 유지함.
- 추가 Fig 7 / Fig 8 생성 필요성을 재검토하고, 기존 Fig 1~6과 Molecular Twin / OOD / inference / Streamlit 결과로 핵심 발표 흐름을 구성할 수 있으므로 필수 작업에서 제외함.
- 새로운 preprocessing, feature selection, model retraining, hyperparameter tuning 또는 Test 재평가는 수행하지 않음.
- 기존 frozen 분석 결과를 변경하지 않고 발표 및 배포 준비 단계로 진행함.
- `README.md`를 최종 프로젝트 설명 및 발표 흐름에 맞게 수정하고 stage함.

#### Streamlit deployment reproducibility 점검

- 별도 실행 환경에서 Streamlit smoke test를 수행함.
- 실행 과정에서 다음 frozen artifact를 찾을 수 없어 `FileNotFoundError`가 발생함.

```text
models/clinical_preprocessor.joblib
```

- `src/patient_inference.py`의 artifact loading 부분을 확인하여 inference에 필요한 frozen artifact 5개를 확정함.

```text
models/clinical_preprocessor.joblib
models/combined_scaler.joblib
models/clinical_rna_coxnet.joblib
models/selected_rna_genes.joblib
models/clinical_rna_config.joblib
```

- 해당 실행 환경의 `models/` 디렉터리에 frozen artifact가 존재하지 않음을 확인함.
- `.gitignore`를 점검하여 다음 설정으로 인해 `models/` 전체가 Git 추적 대상에서 제외되어 있음을 확인함.

```text
# Models
models/
```

- 따라서 기존 개발 환경에서는 정상적으로 동작했던 frozen model 기반 inference가 새로운 실행 환경에서는 repository만으로 재현되지 않는 문제를 확인함.
- 이는 model training 또는 inference logic의 오류가 아니라 **frozen artifact의 배포 및 repository 관리 문제**로 판단함.
- 모델을 재학습하여 대체하지 않고 기존에 prediction parity까지 검증한 frozen artifact를 그대로 사용하기로 함.
- 검증된 frozen artifact가 새로운 실행 환경에서도 동일하게 사용될 수 있도록 artifact 관리 방식을 보완하기로 함.
- 향후 프로젝트 완료 여부 판단 시 Git 동기화뿐 아니라 실행에 필요한 non-tracked artifact, 환경 의존성 및 새로운 실행 환경에서의 실행 가능성을 포함하는 **deployment reproducibility QC**를 수행하기로 함.

### 3. 주요 결과

오늘 새로운 모델 학습이나 데이터 전처리를 수행하지 않았으므로 아래 수치는 오늘 새롭게 산출된 값이 아니라 최종 발표 준비 과정에서 유지·확인한 프로젝트의 확정 결과임.

- Primary modeling cohort: **529명**
- PFI event:
  - Event = 1: **159명**
  - Event = 0: **370명**
- Train / Validation / Test:
  - Train: **370명**
  - Validation: **79명**
  - Test: **80명**
- Event distribution:
  - Train: **111 events**
  - Validation: **24 events**
  - Test: **24 events**
- Raw protein-coding RNA TPM matrix:
  - **529 × 19,962**
- Train RNA preprocessing:
  - Low-expression filtering 후 **14,220 genes**
  - `log2(TPM+1)`
  - MAD Top-500 selection
- Final Clinical+RNA input:
  - Clinical: **10 features**
  - RNA: **500 features**
  - Combined: **510 features**
- Final Clinical+RNA CoxNet:
  - `l1_ratio = 0.50`
  - `n_alphas = 50`
  - `alpha_min_ratio = 0.01`
  - `max_iter = 100000`
  - Best CV setting: **K=500, L1=0.50, alpha_idx=18**
- Final model non-zero coefficients:
  - Total: **24**
  - Clinical: **3**
  - RNA: **21**
- Test Harrell C-index:
  - RNA-only: **0.7145**
  - Clinical-only: **0.8868**
  - Clinical+RNA: **0.8920**
  - Clinical+Hallmark: **0.8856**
- Test Uno C-index (3-year):
  - RNA-only: **0.7032**
  - Clinical-only: **0.8798**
  - Clinical+RNA: **0.8970**
  - Clinical+Hallmark: **0.8682**
- Clinical+RNA vs Clinical-only paired bootstrap:
  - ΔC = **+0.005126**
  - 95% CI = **-0.024295 ~ +0.044045**
  - CI가 0을 포함하므로 RNA 추가에 따른 명확한 incremental discrimination benefit이 입증됐다고 해석하지 않음.
- Frozen model reproducibility:
  - Reload 후 risk difference = **0.0**
- Patient inference 검증:
  - `TCGA-BP-5169`
  - Risk = **0.877533...**
- Molecular support low-support 검증:
  - `TCGA-B0-5694`
  - Similarity = **0.304**
  - Threshold = **0.381**
  - Low-support warning 정상 작동
- Cohort / split / preprocessing / modeling / evaluation 단계에서 새로운 분석 오류는 발견되지 않음.
- 별도 실행 환경 점검을 통해 frozen model artifact의 repository 배포 문제가 추가 QC 항목으로 확인됨.

### 4. 생성/수정된 파일

#### Git 비추적 상태에서 회수하여 `results/`에 추가한 파일

- `results/clinical_coxnet_coefficients.csv`
- `results/clinical_coxnet_nonzero_features.csv`
- `results/clinical_pathway_coxnet_coefficients.csv`
- `results/clinical_pathway_coxnet_nonzero_features.csv`
- `results/clinical_rna_coxnet_coefficients.csv`
- `results/clinical_rna_coxnet_nonzero_features.csv`
- `results/clinical_rna_nonzero_genes_annotated.csv`
- `results/rna_coxnet_coefficients.csv`
- `results/rna_coxnet_nonzero_genes.csv`
- `results/final_model_comparison.csv`
- `results/final_model_specifications.csv`
- `results/final_performance_summary.csv`
- `results/test_brier_ibs_metrics.csv`
- `results/test_discrimination_metrics.csv`
- `results/test_grouped_calibration.csv`
- `results/test_harrell_c_bootstrap_ci.csv`
- `results/test_harrell_c_difference_ci.csv`
- `results/test_predictions.csv`

총 **18개 결과 파일**을 Git 추적 가능한 `results/`에 보존함.

#### 원격 repository와 동기화된 주요 파일

- `app.py`
- `src/patient_inference.py`
- `notebooks/05_molecular_twin_ood.ipynb`
- `notebooks/06_patient_inference.ipynb`
- `notebooks/07_final_results_summary.ipynb`
- `results/molecular_support_config.csv`
- `results/molecular_twin_features.csv`
- `results/molecular_twin_results.csv`
- `results/molecular_twin_train_reference.parquet`
- `results/ood_results.csv`
- `results/patient_inference_qc.csv`
- `results/patient_molecular_support_summary.csv`

#### 기타

- `README.md`
  - 최종 프로젝트 설명 및 발표 준비에 맞춰 수정.
  - Git stage까지 확인함.
  - 해당 수정분의 최종 commit / push 여부는 다음 작업 시작 시 실제 Git 상태를 기준으로 확인함.

### 5. 오늘 결정한 분석 기준

- 최종 발표 단계에서 기존 분석 결과를 변경하기 위한 추가 model tuning을 수행하지 않음.
- Primary modeling cohort **529명** 유지.
- Endpoint는 **PFI** 유지.
- 기존 event-stratified Train / Validation / Test split **370 / 79 / 80**, random seed **42** 유지.
- RNA preprocessing은 기존 Train-derived pipeline 유지:
  - protein-coding genes
  - Train-derived low-expression filtering
  - `log2(TPM+1)`
  - Train-derived MAD Top-500
- preprocessing, feature selection 및 scaling parameter를 Test data에서 재추정하지 않음.
- Test 결과를 확인한 뒤 model / hyperparameter를 다시 선택하지 않음.
- 발표에서는 동일한 4-model comparison을 유지:
  - Clinical-only
  - RNA-only
  - Clinical+RNA
  - Clinical+Hallmark
- Clinical+RNA의 Test C-index가 관측상 가장 높다는 결과와 Clinical-only 대비 ΔC CI가 0을 포함한다는 결과를 함께 제시함.
- RNA 추가 효과를 과장하여 해석하지 않음.
- XAI는 model prediction에 대한 global / local interpretation으로 한정하고 인과적 biomarker 발견으로 확대 해석하지 않음.
- Molecular Twin / Molecular Support는 유사한 Train 환자를 이용한 보조 설명 및 support 정보로 사용하며 별도의 예후 모델로 해석하지 않음.
- OOD / support warning은 prediction error probability 또는 임상적 확신도로 해석하지 않음.
- Streamlit은 연구용 patient-level inference prototype으로 설명하며 임상적 진단 또는 실제 의료 의사결정 도구로 표현하지 않음.
- Fig 7 / Fig 8은 현재 최종 발표에 필수적이지 않다고 판단하여 추가 생성하지 않음.
- 기존 frozen model을 새로운 실행 환경에서 재학습하여 대체하지 않고 동일 artifact를 사용함.
- 프로젝트 완료 QC에 **deployment reproducibility / cross-environment reproducibility** 점검을 포함함.

### 6. 확인해야 할 문제 / 미완료

- 검증된 frozen artifact 5개의 repository 관리 및 배포 방식 보완:
  - `clinical_preprocessor.joblib`
  - `combined_scaler.joblib`
  - `clinical_rna_coxnet.joblib`
  - `selected_rna_genes.joblib`
  - `clinical_rna_config.joblib`
- 원격 repository에 반영된 frozen artifact를 새로운 실행 환경으로 동기화.
- 동일 frozen artifact를 사용한 Streamlit 재실행.
- Streamlit demo 최종 smoke test.
- Demo Patient / New Patient 전체 inference flow 최종 확인.
- `TCGA-BP-5169` inference 재현 확인.
- `TCGA-B0-5694` low-support warning 확인.
- 발표자료 전체 슬라이드 최종 검수.
- 슬라이드 숫자와 `README.md` 및 final result 파일의 수치 일치 여부 확인.
- Clinical+RNA와 Clinical-only 비교 해석이 과장되지 않았는지 최종 확인.
- 발표용 figure의 축, 범례, caption 및 가독성 확인.
- `README.md` 수정분의 최종 commit / push 상태 확인.
- 발표자료 최종 파일 저장 및 발표 환경 정상 작동 확인.
- 최종 repository / 실행환경 / 발표파일 패키징 확인.

### 7. GitHub 상태

- Branch: `main`
- Git 비추적 상태로 존재하던 최종 결과 CSV 18개를 `results/`에 회수하여 repository에 통합함.
- 원격 repository의 최신 Molecular Twin / OOD / inference / Streamlit 작업을 로컬 repository와 merge함.
- merge conflict 없음.
- 결과 통합 이후 push 완료 및 당시 `origin/main`과 동기화된 clean 상태를 확인함.
- 이후 `README.md`를 추가 수정하고 `git add README.md`까지 실행한 기록이 있으므로 해당 README 수정분의 commit / push 여부는 다음 작업 시작 시 다시 확인함.
- `models/`가 `.gitignore`에 포함되어 frozen artifact가 repository를 통해 전달되지 않는 문제를 확인함.
- 검증된 frozen artifact의 repository 관리 방식을 보완한 뒤 새로운 실행 환경에서 재검증할 예정임.

### 8. 현재 프로젝트 진행 위치

```text
TCGA-KIRC Clinical / RNA data acquisition
        ✅
Clinical-RNA patient matching
        ✅
Primary modeling cohort (529)
        ✅
Train / Validation / Test split
        ✅
RNA preprocessing / feature selection
        ✅
4-model CoxNet modeling / CV
        ✅
Model freeze
        ✅
Untouched Test evaluation
        ✅
C-index / TD-AUC / IBS / Calibration
        ✅
XAI
        ✅
Molecular Twin / Molecular Support
        ✅
OOD
        ✅
Frozen inference artifact 생성 및 parity 검증
        ✅
Patient-level inference
        ✅
Streamlit prototype 구현
        ✅
Final result CSV 회수 / GitHub 통합
        ✅
README / 최종 결과 정리
        ✅
        ↓
최종 발표자료 및 발표 준비
        🔄 현재 단계
        ↓
Frozen artifact repository / deployment 보완
        🔄
        ↓
별도 실행 환경 Streamlit smoke test
        ↓
발표자료 / README / repository 최종 QC
        ↓
최종 발표
```

### 9. 다음 작업

1. `git status`를 실행하여 `README.md` 및 `reports/progress_log.md`의 현재 상태 확인.
2. 9/28 progress log를 저장하고 의도한 파일만 commit 대상에 포함되는지 확인.
3. 원격 repository에서 새롭게 반영된 frozen artifact 변경사항을 pull.
4. 다음 frozen artifact 5개가 새로운 실행 환경에 정상적으로 전달되었는지 확인:
   - `clinical_preprocessor.joblib`
   - `combined_scaler.joblib`
   - `clinical_rna_coxnet.joblib`
   - `selected_rna_genes.joblib`
   - `clinical_rna_config.joblib`
5. frozen artifact를 재학습하지 않고 동일 artifact를 사용하여 Streamlit 재실행.
6. `TCGA-BP-5169`의 기존 inference 결과가 동일하게 재현되는지 확인.
7. `TCGA-B0-5694`의 low-support warning이 동일하게 작동하는지 확인.
8. Demo Patient → risk prediction → local contribution → Molecular Support → OOD warning의 전체 demo flow 확인.
9. New Patient 입력 flow 최종 확인.
10. 발표자료를 처음부터 끝까지 실제 발표 순서로 재생하며 cohort 수, event 수, feature 수 및 모델 성능을 최종 결과와 대조.
11. Clinical+RNA Test C-index **0.8920**, Clinical-only **0.8868**, paired ΔC **+0.005126 (95% CI -0.024295 ~ +0.044045)**가 일관되게 제시되는지 확인.
12. XAI의 non-zero **24개(Clinical 3 + RNA 21)**와 global / local explanation 의미 확인.
13. Molecular Twin / OOD를 prediction probability 또는 임상적 confidence로 오해할 수 있는 표현이 없는지 확인.
14. 발표자료 최종본을 저장하고 실제 발표 환경에서 figure, 글꼴, 레이아웃 및 화면 비율 확인.
15. 마지막 `git status` / `git push` 확인 후 발표 버전으로 최종 freeze.
```
