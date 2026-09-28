# PD/LBD Amyloid Speech Project

Data-driven language phenotypes in Parkinsonian / Lewy body disorders, their association with
Alzheimer's amyloid co-pathology, and differences in non-language cognitive functioning.

## Contents

- [`prepare_nacc_language_project.py`](prepare_nacc_language_project.py) — reproducible script
  that verifies source columns, applies NACC missing/not-applicable code handling, derives
  `AMYLOID_STATUS` and PD/Parkinsonism/LBD cohort flags, and builds the focused dataset below.
  Missing-value handling and the amyloid classification rule are isolated in labeled functions.
- `NACC_PD_LBD_language_project.csv` — focused dataset (3,523 rows, all participants retained)
  containing NACCID, the five language-phenotype variables, amyloid biomarkers, non-language
  cognitive outcomes, PD/Parkinsonism/LBD diagnostic variables, AD diagnostic variables,
  demographics/covariates, PD/LBD clinical variables, the derived `AMYLOID_STATUS`, and boolean
  cohort indicators for five candidate PD/LBD cohort definitions.
- [`RESULTS.md`](RESULTS.md) — full variable-verification report: exact column names, usable-N
  counts after excluding NACC special missing codes, the amyloid classification rule and its
  rationale, cohort/sample-size tables, and RQ1/RQ2 sample-size summaries, including flags on
  variables whose coding could not be independently verified.

## Source data

Built from `NACC_PD_LBD_optional_subgroup_3523.csv` (3,523 rows, ~1,771 columns), not included in
this repo. Place that file alongside the script and run:

```
python3 prepare_nacc_language_project.py
```

## Research questions

**RQ1:** Are there distinct data-driven language phenotypes (semantic fluency, phonemic fluency,
confrontation naming) among individuals with Parkinsonian/Lewy body disorders, and is amyloid
co-pathology associated with phenotype membership?

**RQ2:** Do the identified language phenotypes differ in non-language cognitive functioning
(memory, executive function, processing speed/attention, visuospatial ability)?

See [`RESULTS.md`](RESULTS.md) for sample-size feasibility for both questions.
