# Task 3 - Bonus Analysis of `winner.py`

## Plain-English Summary

The supplied script automates the same decision process used in Task 2. It standardizes dates, text, and PC/OC/JP values; removes ineligible accounts; labels each account as New or Existing; and ranks the eligible pool for the category awards and MVP. It can also exclude previous winners when that file is supplied.

New covers start dates from 1 October 2025 through 31 January 2026; all other or blank starts are Existing. Category awards use one overall top-30 list per metric: PC for Search Smasher, OC for Campaign Captain, and JP for Posting Champion. The highest New and Existing accounts in each list win. MVP requires all three metrics above zero and selects the top five per user type by `PC + OC + JP`.

This directly connects to Task 2: my solution applies the same rules to the supplied Purchase file, while adding schema checks, deterministic tie ordering, and a formatted reviewer-ready workbook.

## Data-Backed Insights

1. After exclusions, 13,153 of 17,149 Purchase rows remain eligible. The pool contains 10,015 Existing versus 3,138 New accounts, while the award design gives both groups equal winner slots.
2. Only 289 eligible rows, about 2.2%, have positive PC, OC, and JP and qualify for MVP, making the all-rounder condition highly selective.
3. In the MVP-eligible pool, OC contributes about 71.8% of aggregate raw score, PC 28.1%, and JP 0.1%. If balanced cross-product usage is the goal, normalized measures or agreed business weights would reduce this scale effect.

## Recommended Improvements

- Move hardcoded paths, dates, and thresholds into validated configuration.
- Validate the schema and report invalid dates explicitly.
- Define a stable tie-break rule for reproducible winners.
- Add structured row-count logs and tests for boundaries, exclusions, top-30 logic, MVP eligibility, ties, and optional old-winner handling.
