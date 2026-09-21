# Project Progress Log

## 2026-09-21

### 1. 오늘의 목표
- [x] RNA expression matrix 생성
- [x] Clinical-RNA matched cohort 확정
- [x] Primary modeling cohort 확정 및 PRE-SPLIT QC
- [ ] Train / Validation / Test split

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

### 4. 생성/수정된 파일
- `data/interim/kirc_matched_cohort.parquet`
  - Clinical-RNA matched cohort, 531 patients
- `data/interim/rna_tpm_matched.parquet`
  - matched cohort RNA TPM matrix, 531 × 19,962
- `data/interim/kirc_modeling_cohort.parquet`
  - primary survival modeling cohort, 529 patients
- `data/interim/rna_tpm_modeling_raw.parquet`
  - raw TPM matrix for modeling cohort, 529 × 19,962
- `reports/progress_log.md`
  - 2026-09-21 작업 종료 상태 업데이트

### 5. 오늘 결정한 분석 기준
- 분석 단위: patient-level
- Primary endpoint: PFI
- 531명은 Clinical-RNA matched cohort로 구분
- 529명은 primary survival modeling cohort로 구분
- RNA expression: GDC STAR Counts의 TPM 사용
- RNA gene set: protein-coding genes 기준
- 이후 split: Train / Validation / Test = 70 / 15 / 15
- split stratification: `pfi_event`
- random seed: 42
- low-expression filtering, scaling, feature selection, hyperparameter tuning은 Train 기준으로 수행하여 data leakage 방지
- log transform은 `log2(TPM + 1)` 사용 예정

### 6. 확인해야 할 문제 / 미완료
- 529명 Train / Validation / Test split 아직 미실행
- `splits.csv` 미생성
- 각 split의 환자 수 및 event 비율 QC 필요
- Train 기준 low-expression filtering 미실행
- log2(TPM+1) 변환 및 scaling 미실행
- Clinical / RNA / Clinical+RNA / Clinical+Hallmark survival model 미구축

### 7. GitHub 상태
- Commit: ✅
- Push: ✅
- Commit message: `update progress log for 2026-09-21`

### 8. 현재 프로젝트 진행 위치
Clinical + RNA cohort 구축 완료  
→ RNA expression matrix 생성 완료  
→ Primary modeling cohort 529명 확정 및 PRE-SPLIT QC 완료  
→ **Train / Validation / Test split ← 다음 작업**  
→ leakage-safe preprocessing  
→ Clinical CoxNet baseline  
→ RNA / Clinical+RNA / Clinical+Hallmark 모델  
→ 최종 평가

### 9. 다음 작업
1. 529명을 Train / Validation / Test = 70 / 15 / 15로 event-stratified split
2. random seed = 42 고정
3. `splits.csv` 저장
4. 각 split의 환자 수와 PFI event 비율 QC
5. Train 기준 low-expression filtering
6. `log2(TPM + 1)` 변환
7. scaling 및 survival modeling pipeline 준비
