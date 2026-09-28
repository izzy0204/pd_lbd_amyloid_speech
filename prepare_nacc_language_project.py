"""
prepare_nacc_language_project.py

Builds a focused analysis dataset for the NACC PD/LBD language-phenotype project
from NACC_PD_LBD_optional_subgroup_3523.csv.

All column names were verified directly against the source CSV header before use
(see README notes in the accompanying report). Missing/not-applicable code handling
and the amyloid-status derivation are isolated in clearly labeled functions below so
assumptions are auditable and easy to change.

Coding basis:
- Standard NACC UDS neuropsychological battery special values (ANIMALS, VEG, UDSVERFC,
  UDSVERLC, MINTTOTS, CRAFT*, UDSBENTC/D/RS): 95=physical problem, 96=cognitive/behavioral
  problem, 97=other problem, 98=verbal refusal, -4=not available (not collected this visit).
- TRAILA/TRAILB: 995/996/997/998 are the equivalent unable-to-complete/refusal codes; -4=NA.
- MOCATOTS/NACCMOCA: 88=test not administered, 99=unknown (NACCMOCA only); -4=NA.
- Binary presence/diagnosis flags (PD, AMYLPET, AMYLCSF, CSFAD, TAUPET, TAUPETAD, PROBAD,
  POSSAD, NACCALZD, PARKGAIT, PARKSIGN, PARK, NACCLBDS/E): 0=No, 1=Yes, 8=not
  assessed/N/A, 9=unknown, -4=not available this visit. Not every variable uses every code;
  observed codes are taken from the data itself (see report) rather than assumed.
- "Primary/contributing" etiology-style variables (NACCLBDP, NACCALZP): 1=Primary,
  2=Contributing, 3=Non-contributing, 7/8=not applicable or unassessed. This pattern is
  well documented for NACC etiology fields generally, but exact label text for codes 3/7
  on NACCLBDP was NOT independently verified against a codebook and is flagged as
  uncertain in the report.
- Demographic special codes: EDUC 99=Unknown; RACE -4=NA, 99=Unknown (code 50 is treated
  as a legitimate "Multiracial" category, not missing); NACCLANG 9=Unknown (8=Other is kept
  as a valid category); NACCHISP 9=Unknown.
- PDAGE/PARKAGE: -4=NA, 888=not applicable (no PD/parkinsonism); PDAGE also has 999=Unknown.
- PDYR: -4=NA, 8888=not applicable, 9999=Unknown.
- TOTALUPDRS: -4=NA, 888=not applicable (no parkinsonism).

Several requested variables (PARKINSONISM_PHENOTYPE, REPORTED_PD_OR_PARKINSONISM,
PARKINSONISM_PLUS_DIAGNOSIS, EVER_PARKINSONISM_PHENOTYPE, DIAGNOSIS_PLUS_BIOMARKER,
ANTIPARKINSON_MEDICATION, CLARITI_AMYLOID_STATUS (RORAMYCENTRES)) are NOT part of the
standard NACC UDS data dictionary. They appear to be custom-derived fields already present
in this extract. Their exact derivation logic could not be verified from the CSV alone and
is reported as-is with that uncertainty flagged.
"""

import numpy as np
import pandas as pd

SRC_PATH = "NACC_PD_LBD_optional_subgroup_3523.csv"
OUT_CSV_PATH = "NACC_PD_LBD_language_project.csv"

EXPECTED_N = 3523

# ---------------------------------------------------------------------------
# 1. Missing / not-applicable code definitions
# ---------------------------------------------------------------------------
# Each entry: variable -> set of numeric codes to treat as missing/not-applicable
# (i.e. NOT usable) for that specific variable. Codes not listed are treated as
# legitimate values. String-valued variables are handled separately.

SPECIAL_CODES = {
    # Language phenotype variables
    "ANIMALS": {-4, 95, 96, 97, 98},
    "VEG": {-4, 95, 96, 97, 98},
    "UDSVERFC": {-4, 95, 96, 97, 98},
    "UDSVERLC": {-4, 95, 96, 97, 98},
    "MINTTOTS": {-4, 95, 96, 97, 98},

    # Amyloid biomarker variables (0/1 valid; 8=not assessed, 9=unknown, -4=NA)
    "AMYLPET": {-4, 8, 9},
    "AMYLCSF": {-4, 8},
    "CSFAD": {-4, 9},
    "TAUPET": {-4, 8, 9},
    "TAUPETAD": {-4, 8},

    # Memory
    "CRAFTVRS": {-4, 95, 96, 97, 98},
    "CRAFTURS": {-4, 95, 96, 97, 98},
    "CRAFTDVR": {-4, 95, 96, 97, 98},
    "CRAFTDRE": {-4, 95, 96, 97, 98},

    # Executive / processing speed
    "TRAILB": {-4, 995, 996, 997, 998},
    "TRAILA": {-4, 995, 996, 997, 998},

    # Visuospatial
    "UDSBENTC": {-4, 95, 96, 97, 98},
    "UDSBENTD": {-4, 95, 96, 97, 98},
    "UDSBENRS": {-4, 95, 96, 97, 98},

    # Global cognition
    "MOCATOTS": {-4, 88},
    "NACCMOCA": {-4, 88, 99},

    # PD / Parkinsonism / LBD cohort variables
    "PD": {-4, 9},
    "PARK": {-4},
    "NACCLBDS": {-4, 7, 8},   # code 7 observed once; treated cautiously as non-usable (see report)
    "NACCLBDE": {-4, 8},
    "NACCLBDM": {-4},

    # AD / mixed pathology
    "NACCALZD": {-4, 8},
    "PROBAD": {-4, 8},
    "POSSAD": {-4, 8},

    # Demographics
    "EDUC": {99},
    "RACE": {-4, 99},
    "NACCLANG": {9},
    "NACCHISP": {9},

    # PD/LBD clinical characteristics
    "TOTALUPDRS": {-4, 888},
    "PDAGE": {-4, 888, 999},
    "PDYR": {-4, 8888, 9999},
    "PARKAGE": {-4, 888},
    "PARKGAIT": {-4, 8},
    "PARKSIGN": {-4},
}

# Variables with no special codes observed / treated as always usable when non-missing
NO_SPECIAL_CODE_VARS = ["NACCAGE", "NACCSEX", "NACCUDSD"]

LANGUAGE_VARS = ["ANIMALS", "VEG", "UDSVERFC", "UDSVERLC", "MINTTOTS"]

CLARITI_COL = "CLARITI_AMYLOID_STATUS (RORAMYCENTRES)"


# ---------------------------------------------------------------------------
# 2. Usability helpers
# ---------------------------------------------------------------------------

def usable_mask(df: pd.DataFrame, var: str) -> pd.Series:
    """Boolean mask: True where var has a non-missing, non-special-code value."""
    s = df[var]
    notna = s.notna()
    if var in SPECIAL_CODES:
        bad = s.isin(SPECIAL_CODES[var])
        return notna & ~bad
    return notna


def usable_count(df: pd.DataFrame, var: str) -> int:
    return int(usable_mask(df, var).sum())


# ---------------------------------------------------------------------------
# 3. Amyloid status derivation
# ---------------------------------------------------------------------------

def derive_amyloid_status(df: pd.DataFrame) -> pd.Series:
    """
    AMYLOID_STATUS = 'A+' / 'A-' / 'Unknown'

    Rule (documented, not assumed to be the only valid rule):
      A+  if AMYLPET == 1  OR  AMYLCSF == 1  OR  CLARITI text == 'elevated'
      A-  if not A+ AND (AMYLPET == 0 OR AMYLCSF == 0 OR CLARITI text == 'non-elevated')
      Unknown otherwise (covers -4/8/9 codes and all-missing cases)

    Positive evidence takes precedence over negative evidence when PET and CSF
    are discordant for the same participant (a small number of such cases exist
    in this dataset — see report). TAUPET/TAUPETAD/CSFAD are tau or composite
    AD-signature markers, not amyloid-specific, and are intentionally excluded
    from this derivation.
    """
    amylpet_pos = df["AMYLPET"] == 1
    amylpet_neg = df["AMYLPET"] == 0
    amylcsf_pos = df["AMYLCSF"] == 1
    amylcsf_neg = df["AMYLCSF"] == 0
    clariti = df[CLARITI_COL]
    clariti_pos = clariti == "elevated"
    clariti_neg = clariti == "non-elevated"

    is_pos = amylpet_pos | amylcsf_pos | clariti_pos
    is_neg = (~is_pos) & (amylpet_neg | amylcsf_neg | clariti_neg)

    status = pd.Series("Unknown", index=df.index, dtype=object)
    status[is_pos] = "A+"
    status[is_neg] = "A-"
    return status


# ---------------------------------------------------------------------------
# 4. Cohort definitions
# ---------------------------------------------------------------------------

def derive_cohort_flags(df: pd.DataFrame) -> pd.DataFrame:
    pd1 = df["PD"] == 1
    park1 = df["PARK"] == 1
    lbds1 = df["NACCLBDS"] == 1

    flags = pd.DataFrame(index=df.index)
    flags["COHORT_PD_EQ_1"] = pd1
    flags["COHORT_PARK_EQ_1"] = park1
    flags["COHORT_NACCLBDS_EQ_1"] = lbds1
    flags["COHORT_PD_OR_LBDS"] = pd1 | lbds1
    flags["COHORT_PD_OR_PARK_OR_LBDS"] = pd1 | park1 | lbds1
    return flags


# ---------------------------------------------------------------------------
# 5. Complete-case language / amyloid helpers
# ---------------------------------------------------------------------------

def complete_language_mask(df: pd.DataFrame) -> pd.Series:
    mask = pd.Series(True, index=df.index)
    for v in LANGUAGE_VARS:
        mask &= usable_mask(df, v)
    return mask


# ---------------------------------------------------------------------------
# 6. Reporting helpers
# ---------------------------------------------------------------------------

def variable_report_row(df, category, requested, exact_col, description):
    if exact_col not in df.columns:
        return {
            "Category": category, "Requested variable": requested,
            "Exact CSV column": "NOT FOUND", "Description": description,
            "Raw non-missing N": None, "Valid/usable N": None,
            "Missing/unusable N": None, "Notes": "Column not found in CSV",
        }
    raw_nonmissing = int(df[exact_col].notna().sum())
    if exact_col in SPECIAL_CODES or exact_col in NO_SPECIAL_CODE_VARS:
        valid = usable_count(df, exact_col)
    elif exact_col == CLARITI_COL:
        valid = int((df[exact_col].isin(["elevated", "non-elevated"])).sum())
    else:
        valid = raw_nonmissing
    return {
        "Category": category, "Requested variable": requested,
        "Exact CSV column": exact_col, "Description": description,
        "Raw non-missing N": raw_nonmissing, "Valid/usable N": valid,
        "Missing/unusable N": EXPECTED_N - valid, "Notes": "",
    }


def sample_size_for_mask(df, mask, amyloid_status):
    total = int(mask.sum())
    lang5 = int((mask & complete_language_mask(df)).sum())
    aplus = int((mask & (amyloid_status == "A+")).sum())
    aminus = int((mask & (amyloid_status == "A-")).sum())
    known = aplus + aminus
    lang5_aplus = int((mask & complete_language_mask(df) & (amyloid_status == "A+")).sum())
    lang5_aminus = int((mask & complete_language_mask(df) & (amyloid_status == "A-")).sum())
    lang5_known = lang5_aplus + lang5_aminus
    return {
        "Total N": total, "Complete 5-language N": lang5,
        "A+ N": aplus, "A- N": aminus, "Known amyloid N": known,
        "Complete language + A+": lang5_aplus, "Complete language + A-": lang5_aminus,
        "Complete language + known amyloid": lang5_known,
    }


# ---------------------------------------------------------------------------
# 7. Main pipeline
# ---------------------------------------------------------------------------

def main():
    df = pd.read_csv(SRC_PATH, low_memory=False)
    assert len(df) == EXPECTED_N, f"Expected {EXPECTED_N} rows, found {len(df)}"
    assert df["NACCID"].is_unique, "NACCID is not unique!"

    amyloid_status = derive_amyloid_status(df)
    cohort_flags = derive_cohort_flags(df)
    lang5_mask = complete_language_mask(df)

    # ---- Focused CSV -------------------------------------------------
    keep_cols = ["NACCID"] + LANGUAGE_VARS + [
        "AMYLPET", "AMYLCSF", CLARITI_COL, "CSFAD", "TAUPET", "TAUPETAD",
        "CRAFTVRS", "CRAFTURS", "CRAFTDVR", "CRAFTDRE",
        "TRAILB", "TRAILA",
        "UDSBENTC", "UDSBENTD", "UDSBENRS",
        "MOCATOTS", "NACCMOCA",
        "PD", "PARK", "NACCLBDS", "NACCLBDE", "NACCLBDP", "NACCLBDM",
        "PARKINSONISM_PHENOTYPE", "REPORTED_PD_OR_PARKINSONISM",
        "PARKINSONISM_PLUS_DIAGNOSIS", "EVER_PARKINSONISM_PHENOTYPE",
        "NACCALZD", "NACCALZP", "PROBAD", "POSSAD", "DIAGNOSIS_PLUS_BIOMARKER",
        "NACCAGE", "EDUC", "NACCSEX", "NACCLANG", "RACE", "NACCHISP", "NACCUDSD",
        "TOTALUPDRS", "PDAGE", "PDYR", "PARKAGE", "PARKGAIT", "PARKSIGN",
        "ANTIPARKINSON_MEDICATION",
    ]
    focused = df[keep_cols].copy()
    focused["AMYLOID_STATUS"] = amyloid_status
    focused["COMPLETE_5_LANGUAGE"] = lang5_mask
    focused = pd.concat([focused, cohort_flags], axis=1)

    assert len(focused) == EXPECTED_N
    assert focused["NACCID"].is_unique
    focused.to_csv(OUT_CSV_PATH, index=False)

    # ---- Validation ----------------------------------------------------
    reread = pd.read_csv(OUT_CSV_PATH, low_memory=False)
    assert len(reread) == EXPECTED_N, "Row count mismatch after re-read"
    assert reread["NACCID"].is_unique, "Duplicate NACCID after re-read"
    assert reread["NACCID"].tolist() == df["NACCID"].tolist(), "NACCID order/content changed"

    print(f"Focused CSV written: {OUT_CSV_PATH} ({len(focused)} rows, {focused.shape[1]} columns)")
    print(f"Complete 5-language N: {int(lang5_mask.sum())}")
    print(amyloid_status.value_counts())

    for name, mask in [
        ("PD==1", cohort_flags["COHORT_PD_EQ_1"]),
        ("PARK==1", cohort_flags["COHORT_PARK_EQ_1"]),
        ("NACCLBDS==1", cohort_flags["COHORT_NACCLBDS_EQ_1"]),
        ("PD==1 OR NACCLBDS==1", cohort_flags["COHORT_PD_OR_LBDS"]),
        ("PD==1 OR PARK==1 OR NACCLBDS==1", cohort_flags["COHORT_PD_OR_PARK_OR_LBDS"]),
    ]:
        print(name, sample_size_for_mask(df, mask, amyloid_status))


if __name__ == "__main__":
    main()
