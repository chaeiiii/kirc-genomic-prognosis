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