# fRL Winner Calculation Method Note

Source file used: `purchase.xlsx`

## Automated Cleaning Summary

- Original rows: 17149
- Eligible rows after cleaning: 13153
- Removed rows: 3996

## Rules Applied

1. Removed ineligible rows where:
   - account_type is free_trial or test_job
   - login contains scrape, _jobs, or ftp
   - service_channel contains scrape
   - company_name contains immigration, ankit sharma proprietor, or freelancer
   - pc_end_date is before 20 February 2026

2. Tagged each eligible account:
   - New: pc_start_date between 1 October 2025 and 31 January 2026
   - Existing: all other rows, including blank start dates

3. Category winners:
   - Search Smasher: highest PC
   - Campaign Captain: highest OC
   - Posting Champion: highest JP
   - Ranked eligible accounts by each metric, checked the top 30, and selected the top New and Existing account.

4. MVP winners:
   - Kept only accounts where PC > 0, OC > 0, and JP > 0
   - MVP Score = PC + OC + JP
   - Ranked New and Existing separately
   - Selected top 5 from each group

Note: Old-winner exclusion was not applied because no old-winners file was provided.
