# fRL Winner Calculation Method Note

- Method: Python standardized text, dates, and PC/OC/JP values, then applied every supplied Purchase eligibility rule before ranking.
- Cleaning: 17,149 source rows became 13,153 eligible rows; 3,996 rows were excluded.
- Classification: New means a start date from 1 October 2025 through 31 January 2026; all other or blank start dates are Existing.
- Winners: each PC/OC/JP category uses the overall top 30 and selects the highest New and Existing account; MVP requires all three metrics above zero and takes the top five per user type by PC + OC + JP.
- Anomalies/assumptions: 409 start dates and 409 end dates are blank/invalid; blank starts count as Existing, while blank ends are ineligible because active status cannot be verified, matching the supplied `winner.py`. No old-winners list was provided.
