# Task 3 - Bonus Analysis Of `winner.py`

## Overview

The provided `winner.py` script is an automation script for calculating fRL winners from recruiter usage data. It applies eligibility filters, classifies accounts as New or Existing, ranks companies across the PC/OC/JP usage metrics, and generates the final winner output.

This bonus task connects directly with Task 2. Task 2 was the calculation exercise on the provided `purchase.xlsx` file, while `winner.py` shows how the same rule framework can be operationalized as a repeatable automation pipeline for fRL winner generation.

---

## How Task 3 Relates To Task 2

In Task 2, I calculated the fRL winners from the Purchase source by applying the assignment rules step by step:

1. Remove ineligible rows.
2. Tag each account as New or Existing.
3. Rank eligible accounts by PC, OC, and JP.
4. Select the top New and Existing winner for each category.
5. Calculate MVP Score as `PC + OC + JP`.
6. Select the top 5 New and top 5 Existing MVP accounts.

The `winner.py` script follows the same core logic. It is essentially a reusable implementation of the Task 2 workflow. The main difference is that Task 2 focuses only on the provided Purchase source, while `winner.py` is designed to support both Purchase and Bridge sources in a production-style fRL workflow.

---

## What The Script Does

### 1. Configuration

The script defines key inputs and rules at the top:

- `REFERENCE_DATE = datetime(2026, 2, 20)`
- `TOP_N_MVP = 5`
- File paths for old winners, Bridge source, Purchase source, and output file
- `NEW_MONTHS = [(2026, 1), (2025, 12), (2025, 11), (2025, 10)]`
- Excluded account types: `free_trial` and `test_job`

This makes the winner calculation rule-driven, although some values are currently hardcoded.

---

### 2. Old Winner Exclusion

The function `load_old_winners()` reads a previous winners file and stores old winner company names in lowercase.

This is useful because the brief mentions that companies which already won in a previous cycle should be excluded if the old-winners list is provided.

In my Task 2 calculation, this exclusion was not applied because no old-winners file was provided with the assignment package.

---

### 3. Preprocessing

The `preprocess()` function standardizes the input data before applying business rules.

It performs three important steps:

1. Converts start and end dates into datetime fields.
2. Converts text columns such as company name, service channel, login, email, and account type into string format.
3. Converts PC, OC, and JP into numeric values and replaces invalid/missing values with zero.

This matches the cleaning logic needed in Task 2 before calculating winners.

---

### 4. New Vs Existing Classification

The `classify_user()` function tags accounts as New or Existing.

The script marks an account as New if the start date falls in one of these months:

- October 2025
- November 2025
- December 2025
- January 2026

If the start date is blank or outside these months, the account is classified as Existing.

This matches the Task 2 rule where New accounts are those with `pc_start_date` between 1 October 2025 and 31 January 2026.

---

### 5. Global Exclusions

The `apply_global_exclusions()` function removes ineligible rows.

It excludes rows where:

- login contains `scrape`, `_jobs`, or `ftp`
- service_channel contains `scrape`
- company_name contains `immigration`, `ankit sharma proprietor`, or `freelancer`
- account_type is `free_trial` or `test_job`
- end date is before 20 February 2026

This directly maps to the ineligible row removal rule in Task 2.

---

### 6. Category Winners

The `find_category_winners()` function calculates winners for three fRL categories:

| Category | Metric |
|---|---|
| Search Smasher | PC |
| Campaign Captain | OC |
| Posting Champion | JP |

For each metric, the script:

1. Applies global exclusions.
2. Sorts eligible accounts by the metric in descending order.
3. Looks at the top 30 accounts.
4. Selects the highest-ranked New account.
5. Selects the highest-ranked Existing account.
6. Excludes previous winners if old-winners data is available.

This is the same category-winner logic used in Task 2.

---

### 7. MVP Winners

The `find_mvp()` function calculates all-rounder winners.

It keeps only accounts where:

```text
PC > 0
OC > 0
JP > 0