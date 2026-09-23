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

* Commit: **미확인**

* Push: **미확인**

* Commit message: **미확인**

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