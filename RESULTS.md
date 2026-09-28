# NACC PD/LBD Language Project — Variable Verification & Sample-Size Report

Source: `NACC_PD_LBD_optional_subgroup_3523.csv` (3,523 rows, 1,771 columns).
Focused dataset: [`NACC_PD_LBD_language_project.csv`](NACC_PD_LBD_language_project.csv), built by
[`prepare_nacc_language_project.py`](prepare_nacc_language_project.py).

All requested column names were verified directly against the source CSV header before use. Every
requested variable was found **exactly as named**, with one formatting note: the amyloid-status
column's literal header is `CLARITI_AMYLOID_STATUS (RORAMYCENTRES)` (parentheses included, one
combined column, not two separate ones).

## Uncertainty flags (verify against your own codebook before relying on these)

1. **`UDSBENRS`** — expected a 0-17 Benson figure recognition score, but the data is strictly
   binary (0/1). This does not match standard NACC UDS3 coding as I recall it; may be a pass/fail
   recognition flag rather than a point score. Verify before using as a continuous outcome.
2. **`NACCLBDP`, `NACCALZP`** — the 1/2/3/7/8 "primary/contributing/non-contributing/NA/unknown"
   pattern was inferred from general NACC etiology-variable conventions, not a verified
   NACCLBDP-specific codebook entry. Treat as a plausible best guess, not confirmed.
3. **Custom derived booleans** (`PARKINSONISM_PHENOTYPE`, `REPORTED_PD_OR_PARKINSONISM`,
   `PARKINSONISM_PLUS_DIAGNOSIS`, `EVER_PARKINSONISM_PHENOTYPE`, `DIAGNOSIS_PLUS_BIOMARKER`,
   `ANTIPARKINSON_MEDICATION`) and `CLARITI_AMYLOID_STATUS (RORAMYCENTRES)` are **not standard
   NACC UDS variables** — they appear pre-derived by whoever built this "optional subgroup"
   extract. No documentation for their derivation logic was available; raw distributions are
   reported only. CLARITI was used only as *supplementary* positive/negative amyloid evidence
   (its meaning — elevated/non-elevated centiloid — is self-evident from the values).
4. **`NACCLBDS` code 7** (n=1) and **`PD` code 9** — small counts of ambiguous codes; excluded
   from "usable" counts out of caution rather than guessed at.

## 1. Variable availability table

| Category | Requested | Exact CSV column | Raw non-missing N | Valid/usable N | Missing/unusable N | Notes |
|---|---|---|---|---|---|---|
| Language | ANIMALS | ANIMALS | 3523 | 3005 | 518 | Excl. -4(NA),95(physical),96(cog/behav),97(other),98(refusal) |
| Language | VEG | VEG | 3523 | 2968 | 555 | same code scheme |
| Language | UDSVERFC | UDSVERFC | 3523 | 1383 | 2140 | -4=1989: phonemic fluency not collected most visits |
| Language | UDSVERLC | UDSVERLC | 3523 | 1371 | 2152 | same; max value 40 is a plausible outlier, flagged not removed |
| Language | MINTTOTS | MINTTOTS | 3523 | 1302 | 2221 | -4=2074: MINT only in newer UDS3.2+/UDS4 visits |
| Amyloid | AMYLPET | AMYLPET | 3523 | 266 | 3257 | 0=neg,1=pos,8=not assessed(1292),9=unk(1),-4=NA |
| Amyloid | AMYLCSF | AMYLCSF | 3523 | 115 | 3408 | 0=neg,1=pos,8=not assessed(1428),-4=NA |
| Amyloid | CLARITI_AMYLOID_STATUS | `CLARITI_AMYLOID_STATUS (RORAMYCENTRES)` | 10 | 10 | 3513 | string "elevated"/"non-elevated"; extremely sparse ancillary field |
| Amyloid | CSFAD | CSFAD | 3523 | 9 | 3514 | 0=no,1=yes,9=unk,-4=NA(3513); barely collected |
| Amyloid | TAUPET | TAUPET | 3523 | 9 | 3514 | tau marker, not amyloid; barely collected |
| Amyloid | TAUPETAD | TAUPETAD | 3523 | 82 | 3441 | tau-PET AD-pattern marker, not amyloid-specific |
| Memory | CRAFTVRS | CRAFTVRS | 3523 | 1344 | 2179 | 95-98/-4 excluded |
| Memory | CRAFTURS | CRAFTURS | 3523 | 1344 | 2179 | same |
| Memory | CRAFTDVR | CRAFTDVR | 3523 | 1324 | 2199 | same |
| Memory | CRAFTDRE | CRAFTDRE | 3523 | 1324 | 2199 | same |
| Executive function | TRAILB | TRAILB | 3523 | 2067 | 1456 | Excl. -4,995,996,997,998 (unable/refusal) |
| Processing speed | TRAILA | TRAILA | 3523 | 2671 | 852 | same scheme |
| Visuospatial | UDSBENTC | UDSBENTC | 3523 | 1318 | 2205 | copy score 0-17 |
| Visuospatial | UDSBENTD | UDSBENTD | 3523 | 1252 | 2271 | delayed recall 0-17 |
| Visuospatial | UDSBENRS | UDSBENRS | 3523 | 1251 | 2272 | **binary 0/1 only — see flag above** |
| Global cognition | MOCATOTS | MOCATOTS | 3523 | 1347 | 2176 | 88=not administered(102) |
| Global cognition | NACCMOCA | NACCMOCA | 3523 | 1339 | 2184 | 88=not admin(102), 99=unk(8) |
| PD/LBD | PD | PD | 3523 | 3364 | 159 | 0=no(1872),1=yes(952),9=unk(81),-4=NA(618) |
| PD/LBD | PARK | PARK | 3523 | 3468 | 55 | 0=no(2189),1=yes(1279),-4=NA(55) |
| PD/LBD | NACCLBDS | NACCLBDS | 3523 | 2312 | 1211 | 0=no(476),1=yes(1836); 7(n=1) treated non-usable, 8=NA(1210) |
| PD/LBD | NACCLBDE | NACCLBDE | 3523 | 3232 | 291 | 0/1 valid, 8=NA(291) |
| PD/LBD | NACCLBDP | NACCLBDP | 3523 | n/a (categorical, not filtered) | — | 1/2/3="primary/contributing/non-contributing"(best-guess), 7/8=NA — **uncertain** |
| PD/LBD | NACCLBDM | NACCLBDM | 3523 | 3523 | 0 | binary 0/1, no special codes observed |
| PD/LBD (custom) | PARKINSONISM_PHENOTYPE | PARKINSONISM_PHENOTYPE | 3523 | — | — | boolean, non-standard NACC var, derivation unverified |
| PD/LBD (custom) | REPORTED_PD_OR_PARKINSONISM | REPORTED_PD_OR_PARKINSONISM | 3523 | — | — | same flag |
| PD/LBD (custom) | PARKINSONISM_PLUS_DIAGNOSIS | PARKINSONISM_PLUS_DIAGNOSIS | 3523 | — | — | same flag |
| PD/LBD (custom) | EVER_PARKINSONISM_PHENOTYPE | EVER_PARKINSONISM_PHENOTYPE | 3523 | — | — | same flag |
| AD | NACCALZD | NACCALZD | 3523 | 3232 | 291 | 0/1 valid, 8=NA |
| AD | NACCALZP | NACCALZP | 3523 | n/a | — | 1/2/3 primary/contributing/non-contributing (best-guess), 7=not-applicable(no AD), 8=NA |
| AD | PROBAD | PROBAD | 3523 | 1834 | 1689 | legacy UDS2 field; -4=NA(1598) for UDS3+ visits |
| AD | POSSAD | POSSAD | 3523 | 1834 | 1689 | same |
| AD (custom) | DIAGNOSIS_PLUS_BIOMARKER | DIAGNOSIS_PLUS_BIOMARKER | 3523 | — | — | boolean, non-standard, derivation unverified |
| Demo | NACCAGE | NACCAGE | 3523 | 3523 | 0 | 36-102, mean 74.2, SD 8.8, median 75 |
| Demo | EDUC | EDUC | 3523 | 3500 | 23 | 99=unk(23); 0-30 yrs, mean 15.6, SD 3.5, median 16 |
| Demo | NACCSEX | NACCSEX | 3523 | 3523 | 0 | 1=M(2447), 2=F(1076) |
| Demo | NACCLANG | NACCLANG | 3523 | 3520 | 3 | 9=unk(3); 1=Eng(3310) dominant, 8=Other(48) kept as valid |
| Demo | RACE | RACE | 3523 | 3446 | 77 | -4=NA(55),99=unk(22); code 50(n=44) kept as "Multiracial" |
| Demo | NACCHISP | NACCHISP | 3523 | 3504 | 19 | 9=unk(19); 0=No(3288),1=Yes(216) |
| Demo | NACCUDSD | NACCUDSD | 3523 | 3523 | 0 | 1=Normal(291),2=Impaired-not-MCI(87),3=MCI(825),4=Dementia(2320) |
| PD clinical | TOTALUPDRS | TOTALUPDRS | 3523 | 41 | 3482 | -4=NA(3476), 888=not-parkinsonism(6) |
| PD clinical | PDAGE | PDAGE | 3523 | 5 | 3518 | 888=not-PD(49), 999=unk(1), -4=NA(3468); almost unusable |
| PD clinical | PDYR | PDYR | 3523 | 2768 | 755 | 8888=not-PD(1903), 9999=unk(82), -4=NA(673) |
| PD clinical | PARKAGE | PARKAGE | 3523 | 1263 | 2260 | 888=no-parkinsonism(273), -4=NA(1986) |
| PD clinical | PARKGAIT | PARKGAIT | 3523 | 1417 | 2106 | 0/1 valid, 8=unk(34), -4=NA(2072) |
| PD clinical | PARKSIGN | PARKSIGN | 3523 | 1501 | 2022 | 0/1 valid, -4=NA(2022) |
| PD clinical (custom) | ANTIPARKINSON_MEDICATION | ANTIPARKINSON_MEDICATION | 3523 | — | — | boolean, non-standard, derivation unverified |

## 2. Amyloid classification

Only `AMYLPET` and `AMYLCSF` are true amyloid-specific biomarkers with interpretable 0/1 coding
(0=negative, 1=positive; 8/9/-4 are missing-type codes). `TAUPET`/`TAUPETAD` are tau markers;
`CSFAD` is a composite AD CSF profile — none are amyloid-specific, so none were used to classify
amyloid status. `CLARITI_AMYLOID_STATUS` was used only as supplementary text evidence (10 rows).

**Discordance found:** 3 participants have AMYLPET=1 & AMYLCSF=0; 1 has AMYLPET=0 & AMYLCSF=1 — a
small number, resolved by giving positive evidence precedence (see `derive_amyloid_status()` in
the script).

**Rule:** `A+` if AMYLPET==1 OR AMYLCSF==1 OR CLARITI=="elevated"; `A-` if not A+ and (AMYLPET==0
OR AMYLCSF==0 OR CLARITI=="non-elevated"); else `Unknown`.

| | N |
|---|---|
| A+ | 182 |
| A− | 157 |
| Unknown | 3184 |
| A+ with all 5 language | 151 |
| A− with all 5 language | 133 |
| Known amyloid (A+/A−) with all 5 language | 284 |

## 3. Language phenotype completeness (Section A)

| Variable | Usable N | Mean ± SD | Median |
|---|---|---|---|
| ANIMALS | 3005 | 13.13 ± 6.58 | 13 |
| VEG | 2968 | 8.19 ± 4.59 | 8 |
| UDSVERFC | 1383 | 10.95 ± 5.28 | 11 |
| UDSVERLC | 1371 | 10.30 ± 5.10 | 10 |
| MINTTOTS | 1302 | 27.85 ± 4.86 | 29 |
| **All 5 simultaneously** | **1262** | — | — |

The phonemic-fluency (UDSVERFC/LC) and MINT items are the binding constraint — they were only
collected in a subset of visits (later UDS versions), which is why the all-5 N (1262) is far below
ANIMALS/VEG alone (~3000).

## 4. Cohort/sample-size table

| Cohort | Total N | Complete 5-lang N | A+ N | A− N | Known amyloid N | Lang+A+ | Lang+A− | Lang+known |
|---|---|---|---|---|---|---|---|---|
| PD==1 | 952 | 282 | 20 | 39 | 59 | 19 | 37 | 56 |
| PARK==1 | 1279 | 481 | 32 | 50 | 82 | 25 | 42 | 67 |
| NACCLBDS==1 | 1836 | 417 | 86 | 45 | 131 | 70 | 35 | 105 |
| PD==1 OR NACCLBDS==1 | 2565 | 633 | 100 | 76 | 176 | 83 | 65 | 148 |
| PD==1 OR PARK==1 OR NACCLBDS==1 | 2945 | 874 | 114 | 98 | 212 | 92 | 81 | 173 |

`PD`, `PARK`, `NACCLBDS` are **not interchangeable**: PD (physician-diagnosed PD, per differential
diagnosis) is the most restrictive; PARK is a broader parkinsonism flag; NACCLBDS (Lewy body
disease clinical syndrome) is the broadest and captures the most language-complete cases. Overlap
is partial, not nested.

## 5. Cognitive outcomes usable N (Section C)

| Outcome | All (N=3523) | Within lang-5 (N=1262) | Within lang-5 + known amyloid (N=284) |
|---|---|---|---|
| CRAFTVRS | 1344 | 1236 | 280 |
| CRAFTURS | 1344 | 1236 | 280 |
| CRAFTDVR | 1324 | 1226 | 275 |
| CRAFTDRE | 1324 | 1226 | 275 |
| TRAILB | 2067 | 972 | 222 |
| TRAILA | 2671 | 1182 | 263 |
| UDSBENTC | 1318 | 1238 | 280 |
| UDSBENTD | 1252 | 1183 | 264 |
| UDSBENRS | 1251 | 1182 | 264 |
| MOCATOTS | 1347 | 1245 | 280 |
| NACCMOCA | 1339 | 1240 | 280 |

## 6. RQ-specific sample sizes

**RQ1** (language phenotype discovery + amyloid association):
- N for phenotype discovery (all 5 language measures): **1262**
- N with known amyloid status within that set: **284** (A+ = 151, A− = 133)

**RQ2** (phenotype vs. non-language cognition), among the 1262 language-complete participants:
memory ~1226-1236, executive (TRAILB) 972, processing speed (TRAILA) 1182, visuospatial
1182-1238, global cognition 1240-1245 (see table above). TRAILB is the tightest constraint.

## Validation checks performed

- NACCID unique in source (3523/3523) and in focused CSV ✓
- Focused CSV re-read has exactly 3523 rows, same NACCID order/content ✓
- All reported sample sizes recomputed directly from `NACC_PD_LBD_language_project.csv` and
  matched the source-derived numbers ✓
- No duplication introduced at any step ✓

## Bottom line on sample-size limitations

**RQ1** is fundamentally constrained by phonemic fluency (UDSVERFC/LC) and MINT only being
collected in later UDS visits (~1,300-1,400 usable each) — this caps phenotype discovery at
**1,262**, well below the full 3,523. Amyloid biomarker collection is even sparser (only 266 with
valid PET, 115 with valid CSF), so the amyloid-association arm of RQ1 drops to **284** total,
split **151 A+ / 133 A−** — likely underpowered for anything beyond a coarse comparison, and this
shrinks further within any single PD/LBD cohort definition (e.g., only 56-173 depending on which
cohort you pick).

**RQ2** inherits the 1,262 language-complete base, but each cognitive domain has its own
missingness on top of that — Trail Making B is the bottleneck (972, ~23% additional loss), while
memory, visuospatial, and MoCA outcomes retain ~1,180-1,245. If you ultimately restrict to
amyloid-known participants for a joint RQ1+RQ2 model, expect final analytic N in the **220-280**
range for most outcomes — a serious power constraint worth planning for early (e.g., a priori
power analysis, or treating amyloid association as exploratory/secondary).
