# How reliable are ICD-10 diagnosis codes to identify cases of pediatric suicidality?

This study repository includes:

* **Suicidality ICD10 case definition** (SQL) 
* **Supplement**   
  1. Suicidality ICD10 Case Definition (XLS/TSV)
  2. Propensity Score Matching (Word/PDF)
  3. Suicidality Chart Review Guidelines (Word/PDF)
  4. Additional Statistical Measures (Word/PDF)
  
## Usage

To install the module, run `pip install cumulus-library-suicidality-icd10`.

This will add a `cumulus-library-suicidality-icd10` study target to `cumulus-library`.

This study is built using SMART Cumulus:  
* [Cumulus Library](https://docs.smarthealthit.org/cumulus/library) for data processing
* [Chart Review](https://docs.smarthealthit.org/cumulus/chart-review/) packages for subject matter experts to label "ground truth"
* [Propensity Score Matching](https://docs.smarthealthit.org/cumulus/library/statistics/propensity-score-matching.html) (PSM) to select "case matched comparators"

## Publication

__Accuracy of ICD-10 codes for suicidal ideation and action in pediatric emergency department encounters__
Rena Xu, Louisa Bode, Alon Geva, Kenneth D. Mandl, Andrew J. McMurry. Pediatrics. 2024. 
https://doi.org/10.1101/2024.07.23.24310777