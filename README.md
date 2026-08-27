# foundit Talent Operations Assistant

## Project Overview

This project was built for the foundit APMM AI & Automation take-home assignment. It combines a micro talent-supply AI agent, an automated fRL winner calculation workflow, and a Streamlit dashboard that can be shared as a public demo.

The assignment had three parts:

1. Build a micro AI agent on the provided India IT/ITeS talent data.
2. Calculate fRL winners from the provided Purchase usage file using the rules in the assignment brief.
3. Review the provided `winner.py` script and connect it with the fRL winner calculation workflow.

The final solution uses Python because the assignment involves Excel data cleaning, rule-based winner calculation, repeatable automation, and a lightweight dashboard. Streamlit is used for the public-facing demo because it can show the agent, dashboard, and fRL output in one simple browser link.

---

## Business Problem

The assignment mirrors a real product marketing and sales operations workflow at foundit:

- Sales and Customer Success teams need quick answers about India IT/ITeS talent availability.
- Product Marketing needs to calculate fRL winners accurately from recruiter usage data.
- Manual Excel filtering can be slow, error-prone, and hard to repeat every cycle.
- The final output should be easy for business users to understand and easy for technical reviewers to audit.

The key challenge was to create something that is not just a static dashboard. The solution needed to show:

- Data understanding
- Cleaning logic
- Rule-based automation
- Agent-style question answering
- Business-friendly output
- Reusable pipeline structure

---

## Solution Summary

The project creates a small but complete automation pipeline:

```text
Input files
    |
    |-- Assignment_brief.pdf
    |-- Sample_Data_for_agent.xlsx
    |-- purchase.xlsx
    |-- winner.py
    |
Python pipeline
    |
    |-- inspect source files
    |-- clean Purchase usage data
    |-- apply fRL winner rules
    |-- generate fRL winners Excel
    |-- run talent agent smoke test
    |-- generate/check supporting notes
    |
Streamlit app
    |
    |-- Talent Supply Agent
    |-- Talent Dashboard
    |-- fRL Winners preview
    |-- Excel download
    |
n8n workflow
    |
    |-- manual trigger
    |-- run Python pipeline
    |-- verify success or failure
    |-- route to success/failure summary
```

The result is a practical tool that reduces manual work and creates a repeatable submission package.

---

## Why Python + Streamlit

Python was selected because:

- `pandas` is reliable for Excel data cleaning and transformation.
- The fRL rules are easier to audit in code than in manual spreadsheet filters.
- The same script can be rerun whenever the source file changes.
- The pipeline can be extended later into scheduled automation.

Streamlit was selected because:

- It creates a browser-based public demo quickly.
- It works well with Python and Excel outputs.
- It can show the micro agent, dashboard, and winner output in one place.
- It is easier to share with HR/interviewers than a local notebook.

n8n can also automate workflows, but for this assignment Python + Streamlit is a stronger main solution because the core task is data cleaning, rule calculation, and explainable analytics.

---

## Project Structure

```text
Foundit_APMM_Assignment/
|
|-- data/
|   |-- Assignment_brief.pdf
|   |-- Sample_Data_for_agent.xlsx
|   |-- purchase.xlsx
|   |-- winner.py
|
|-- src/
|   |-- inspect_files.py
|   |-- calculate_frl_winners.py
|   |-- talent_agent.py
|   |-- app.py
|
|-- notes/
|   |-- frl_method_note.md
|   |-- task1_system_prompt.md
|   |-- task1_test_qna.md
|   |-- task3_bonus_analysis.md
|
|-- outputs/
|   |-- fRL_winners.xlsx
|
|-- screenshots/
|
|-- n8n/
|   |-- foundit_apmm_n8n_workflow.json
|
|-- run_pipeline.py
|-- requirements.txt
|-- README.md
```

---

## Input Files

### 1. `Assignment_brief.pdf`

The assignment brief explains the three tasks, expected outputs, and fRL winner rules.

### 2. `Sample_Data_for_agent.xlsx`

This file contains India IT/ITeS talent-supply counts from the foundit profile database. The data includes:

- Total profiles
- Active profiles
- Experience bands
- City-level profile counts
- Role-level counts
- Gender counts
- Sub-industry counts

This file powers the micro AI agent and the talent dashboard.

### 3. `purchase.xlsx`

This file contains recruiter usage and purchase data. It is used to calculate fRL winners.

Important columns include:

- `company_name`
- `company_type`
- `account_type`
- `service_channel`
- `login`
- `email`
- `PC`
- `OC`
- `JP`
- `pc_start_date`
- `pc_end_date`

### 4. `winner.py`

This is the provided bonus script. It shows how the fRL winner logic can be automated in Python for repeatable winner generation.

---

## Task 1 - Micro AI Agent

The micro AI agent is built on top of `Sample_Data_for_agent.xlsx`.

The agent answers questions using only the provided talent data. It does not invent values. If the requested information is not present in the dataset, it clearly says that the data is unavailable.

Example supported questions:

```text
How many AI/ML Engineer profiles are available in India?
Which is larger - Data Scientist or DevOps talent, and by how much?
How many 3-5y profiles are available?
How many Pune profiles are available?
```

Example unsupported question:

```text
What salary should I offer a DevOps engineer in Pune?
```

The agent responds that salary/CTC/offer benchmarking data is not available in the provided dataset.

### Why This Counts As Agentic AI

The agent is not only displaying static data. It follows a tool-routing style:

1. It receives a natural-language question.
2. It normalizes the text and maps aliases such as `DevOps` to `DevOps Engineer`.
3. It decides whether the question is a lookup, comparison, total count, or unsupported request.
4. It retrieves the correct answer from the talent knowledge base.
5. It refuses unsupported salary/CTC/notice-period questions instead of hallucinating.

This makes the agent grounded, explainable, and safe for a sales or customer-success use case.

---

## Task 2 - fRL Winner Calculation

Task 2 calculates fRL winners from `purchase.xlsx`.

The automated script is:

```text
src/calculate_frl_winners.py
```

The output is:

```text
outputs/fRL_winners.xlsx
```

### Automated Cleaning

The script performs these cleaning steps:

1. Reads `purchase.xlsx`.
2. Converts `pc_start_date` and `pc_end_date` into date fields.
3. Converts key text columns into clean string values.
4. Converts `PC`, `OC`, and `JP` into numeric values.
5. Removes ineligible rows using the assignment rules.
6. Tags each eligible account as New or Existing.
7. Calculates category winners.
8. Calculates MVP winners.
9. Writes a polished Excel output.

### Eligibility Rules Applied

Rows are removed if any of the following are true:

- `account_type` is `free_trial` or `test_job`
- `login` contains `scrape`, `_jobs`, or `ftp`
- `service_channel` contains `scrape`
- `company_name` contains `immigration`, `ankit sharma proprietor`, or `freelancer`
- `pc_end_date` is before 20 February 2026

Old-winner exclusion was not applied because no old-winners file was provided in the assignment package.

### New vs Existing Logic

```text
New = pc_start_date between 1 Oct 2025 and 31 Jan 2026
Existing = all other rows, including blank start dates
```

### Category Winners

| Category | Metric |
|---|---|
| Search Smasher | PC |
| Campaign Captain | OC |
| Posting Champion | JP |

For each category:

1. Eligible accounts are ranked by the relevant metric.
2. The top 30 are considered.
3. The highest-ranked New account is selected.
4. The highest-ranked Existing account is selected.

### MVP Winners

For MVP, the script keeps only accounts where:

```text
PC > 0
OC > 0
JP > 0
```

Then it calculates:

```text
MVP Score = PC + OC + JP
```

The final MVP output includes:

- Top 5 New accounts
- Top 5 Existing accounts

### Output Formatting

The generated Excel file is polished for review:

- Sheet name: `fRL Winners`
- Header row styled
- Auto-filter enabled
- First row frozen
- Columns widened
- Dates formatted
- Non-applicable MVP fields shown as `-`

---

## Task 3 - Bonus Analysis

The bonus analysis is saved in:

```text
notes/task3_bonus_analysis.md
```

It explains:

- What `winner.py` does
- How it connects to Task 2
- Which parts of the fRL workflow it automates
- Current script strengths
- Suggested improvements

### Task 2 And Task 3 Connection

Task 2 is the actual calculation exercise on the provided Purchase source. Task 3 shows how the same rule framework can be converted into a reusable automation workflow.

Both use the same core logic:

1. Remove ineligible rows.
2. Tag accounts as New or Existing.
3. Calculate PC, OC, and JP category winners.
4. Calculate MVP Score as `PC + OC + JP`.
5. Rank New and Existing accounts separately.
6. Generate a final winner output.

The provided `winner.py` script also supports a Bridge source in addition to the Purchase source, which makes it closer to a production-style monthly fRL automation workflow.

---

## How To Run The Project

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the full automation pipeline:

```powershell
python run_pipeline.py
```

Start the Streamlit dashboard:

```powershell
python -m streamlit run src/app.py
```

---

## One-Command Pipeline

The main automation command is:

```powershell
python run_pipeline.py
```

This command:

1. Checks that all required input files are present.
2. Runs the fRL winner calculation.
3. Generates the polished fRL winners Excel.
4. Runs the talent agent smoke test.
5. Checks that required notes and outputs exist.

---

## n8n Automation Workflow

The project also includes an n8n workflow export:

```text
n8n/foundit_apmm_n8n_workflow.json
```

This workflow demonstrates how the Python pipeline can be operationalized for a business user. Python remains the data-processing engine, while n8n acts as the orchestration layer.

### Why n8n Was Added

Without n8n, the process is still automated but has to be started from the terminal:

```powershell
python run_pipeline.py
```

That works well for a technical user, but a Sales Operations or Product Marketing user may not want to open VS Code, remember commands, or inspect terminal logs manually.

With n8n, the same process becomes a workflow:

```text
Manual Trigger
    |
Run APMM Pipeline
    |
IF status is Success
    |-- True  -> Success Summary
    |-- False -> Failure Summary
```

### What n8n Does

The n8n workflow:

1. Starts from a manual trigger.
2. Runs the Python pipeline that generates the fRL winners Excel.
3. Checks whether the pipeline completed successfully.
4. Confirms that `outputs/fRL_winners.xlsx` exists.
5. Routes the result to a success summary or failure summary.

The `true` branch means the pipeline passed the success condition. In this project, that means the Python script ran, the output Excel file exists, and the workflow can mark the submission as ready.

The `false` branch is included for review handling. If the pipeline fails or the final Excel is missing, the workflow returns a clear review-needed message instead of silently passing.

### Business Value

The n8n layer is useful because it turns a code-based process into an operations workflow. A non-technical user can run the pipeline from a button and immediately see whether the output is ready or needs review.

In a production setup, the same workflow could be extended to:

1. Accept a new Purchase Excel file from a folder, form, email, or Drive upload.
2. Run the winner calculation automatically.
3. Store the generated Excel in a shared location.
4. Notify stakeholders by email, Slack, or WhatsApp.
5. Schedule the process weekly or monthly.
6. Keep execution history for audit and debugging.

For this assignment, the n8n workflow is intentionally kept simple and reviewable. It proves the pipeline can be orchestrated end to end without adding unnecessary complexity.

---

## Streamlit Dashboard

The dashboard is saved at:

```text
src/app.py
```

It contains three tabs:

### 1. Talent Agent

A question-answer interface for India IT/ITeS talent-supply questions.

### 2. Talent Dashboard

A visual summary of talent counts from the source dataset.

### 3. fRL Winners

A preview of the fRL winners output with a download button for the Excel file.

---

## Final Outputs

The key submission outputs are:

```text
outputs/fRL_winners.xlsx
notes/frl_method_note.md
notes/task1_system_prompt.md
notes/task1_test_qna.md
notes/task3_bonus_analysis.md
README.md
n8n/foundit_apmm_n8n_workflow.json
```

For the final email, the main attachments should be:

1. `fRL_winners.xlsx`
2. `task1_system_prompt.md`
3. `task1_test_qna.md`
4. `frl_method_note.md`
5. `task3_bonus_analysis.md`
6. `foundit_apmm_n8n_workflow.json` if an n8n workflow export is requested

The Streamlit public link and GitHub repository link can be included in the email body.

---

## Known Assumptions

- No old-winners file was provided, so old-winner exclusion was not applied.
- The Purchase file is the only required Task 2 source.
- Salary, CTC, notice period, and offer benchmarking are not available in the talent data, so the agent refuses those questions.
- The agent is intentionally grounded on the provided Excel data rather than external web data.

---

## Future Improvements

If this were converted into a production workflow, the next improvements would be:

1. Move paths and dates into a config file.
2. Add an audit sheet showing exclusion counts by reason.
3. Add old-winner file upload support.
4. Add duplicate winner validation.
5. Add richer agent routing for more complex sales questions.
6. Add direct file intake and notification nodes to the n8n workflow.
7. Schedule the workflow using n8n, Airflow, or Windows Task Scheduler.
8. Automatically email the output to stakeholders after validation.

---

## Project Tagline

AI-assisted talent supply lookup and recruiter-league winner automation for foundit-style Sales, CS, and Product Marketing workflows.

