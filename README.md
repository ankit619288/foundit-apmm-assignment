# foundit Talent Operations Assistant

## Project Overview

This project was built for the foundit APMM AI & Automation take-home assignment. It combines a micro talent-supply AI agent, an automated fRL winner calculation workflow, and a Streamlit dashboard that can be shared as a public demo.

### Live Links

| Resource | Link | Purpose |
|---|---|---|
| Public Streamlit app | [foundit Talent Operations Assistant](https://foundit-apmm.streamlit.app/) | Reviewer-facing Task 1 agent, dashboards, and fRL preview |
| GitHub repository | [foundit-apmm-assignment](https://github.com/ankit619288/foundit-apmm-assignment) | Source code, notes, workflow export, outputs, and evidence |
| n8n workflow export | [`n8n/foundit_apmm_n8n_workflow.json`](n8n/foundit_apmm_n8n_workflow.json) | Importable 13-node automation workflow |
| Hosted n8n export | [`n8n/foundit_apmm_n8n_workflow_hosted.json`](n8n/foundit_apmm_n8n_workflow_hosted.json) | Inactive-by-default workflow using isolated container paths |

### Current Status

| Area | Status | Evidence or note |
|---|---|---|
| Task 1 micro agent | Complete | Public Streamlit app, system prompt, three required Q&As, and screenshots |
| Task 2 fRL calculation | Complete | Validated Excel output and short method note |
| Bonus `winner.py` analysis | Complete | Plain-English analysis and business insights in `notes/task3_bonus_analysis.md` |
| Python automation | Complete | `python run_pipeline.py` validates inputs, runs both tasks, executes behavioral tests, and checks deliverables |
| n8n local orchestration | Published and validated | Latest local workflow version includes manual and weekly triggers, Drive input/output, success/failure routing, and Gmail notifications |
| Professional email templates | Included in export | Success and failure Gmail nodes use structured plain-text messages; live credentials remain local to n8n |
| Public Streamlit demo | Live | Accessible through the link above |
| Public n8n editor/runtime | Not deployed | The validated workflow currently runs on a local Windows n8n instance; see [Making n8n Public Safely](#making-n8n-public-safely) |
| Final submission email | User action | Attach the requested outputs and send them to the address in the assignment brief |

### Latest Verified Run

The full pipeline was rerun successfully on 5 September 2026:

```text
Original Purchase rows: 17,149
Eligible rows:          13,153
Removed rows:            3,996
Required files:          Passed
Generated Excel:         outputs/fRL_winners.xlsx
Screenshot evidence:     21 PNG files
Pipeline result:         Completed
Automated tests:         40 passed
```

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
    |-- manual or weekly scheduled trigger
    |-- download the latest Purchase file from Google Drive
    |-- clear and replace the local Purchase input
    |-- run and validate the Python pipeline
    |-- update the existing Drive output on success
    |-- send a professional success or failure email
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
|   |-- foundit_apmm_n8n_workflow_hosted.json
|
|-- deploy/
|   |-- n8n/
|       |-- Dockerfile
|       |-- compose.yaml
|       |-- .env.example
|       |-- README.md
|
|-- run_pipeline.py
|-- requirements.txt
|-- README.md
```

---

## Reviewer Guide - 5 Minute Walkthrough

1. Open the [public Streamlit app](https://foundit-apmm.streamlit.app/) and test the three required Task 1 questions.
2. Review `notes/task1_system_prompt.md` for the grounding and refusal rules.
3. Open `outputs/fRL_winners.xlsx` and verify the six category winners and ten MVP rows.
4. Read `notes/frl_method_note.md` for the short Task 2 method and anomaly note.
5. Read `notes/task3_bonus_analysis.md` for the optional `winner.py` analysis.
6. Open `n8n/foundit_apmm_n8n_workflow.json` or the screenshots listed in the evidence section to inspect the automation.

The repository deliberately separates reviewer-facing evidence from credentials. Google Drive and Gmail OAuth credentials stay inside the local or hosted n8n credential store and are not included in the workflow JSON.

---

## Input Files

### 1. `Assignment_brief.pdf`

The assignment brief explains the three tasks, expected outputs, and fRL winner rules.

### 2. `Sample_Data_for_agent.xlsx`

This file contains India IT/ITeS talent-supply counts from the foundit profile database. The data includes:

- Total profiles
- All-time sourced and registered profiles
- 12-month active, sourced, and registered profiles
- 6-month active, sourced, and registered profiles
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

The agent answers questions using only the provided talent data. It does not invent values. If any requested role, location, experience band, metric, time window, or other constraint is not present in the dataset, it declines the complete request instead of silently dropping that constraint and returning a broader count.

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

The parser supports all nine count measures present in the sheet, including flexible 6-month and 12-month overall paraphrases. It rejects unsupported calendar periods, asks for clarification when an active/sourced/registered scope is ambiguous, refuses unknown entities even when another known entity is present, and permits comparisons only within the same data dimension. It also refuses unsupported cross-tab or dimension-wide requests instead of replacing them with a broader India total.

The loader validates the source structure before serving answers. The current workbook resolves to 53 unambiguous rows: 9 overall measures and 44 category rows. Every category row must contain all nine supplied metrics; missing sections, duplicate labels, incomplete metrics, or negative counts stop the load instead of producing a plausible-looking answer.

Automated grounding coverage checks every one of the 44 category rows against all nine metrics (396 category-metric combinations). The regression suite also covers unknown roles and locations, unsupported time windows, ambiguous metrics, cross-tabs, mixed comparisons, dimension-level requests, unsupported statistics, and prompt-injection-style wording, with assertions that unsupported requests return no source count.

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
- `pc_end_date` is before 20 February 2026 or is blank/invalid, because active status cannot be verified

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
5. Runs the behavioral and artifact integrity test suite.
6. Checks workbook schema, notes, n8n exports, email mode, and screenshot evidence.

---

## n8n Automation Workflow

The project also includes an n8n workflow export:

```text
n8n/foundit_apmm_n8n_workflow.json
n8n/foundit_apmm_n8n_workflow_hosted.json
deploy/n8n/Dockerfile
deploy/n8n/compose.yaml
```

This workflow demonstrates how the Python pipeline can be operationalized for a business user. Python remains the data-processing engine, while n8n acts as the orchestration layer.

### Why n8n Was Added

Without n8n, the process is still automated but has to be started from the terminal:

```powershell
python run_pipeline.py
```

That works well for a technical user, but a Sales Operations or Product Marketing user may not want to open VS Code, remember commands, or inspect terminal logs manually.

With n8n, the same process becomes a workflow with two deliberate entry paths:

```text
Manual Run -----------------------------> Run APMM Pipeline

Weekly Scheduled Run
    -> Download Latest Purchase File from Google Drive
    -> Clear Old Purchase File locally
    -> Save Purchase Input locally
    -> Run APMM Pipeline
    |
IF status is Success
    |-- True  -> Success Summary -> Read Winners Excel -> Update Winners in Drive -> Send Success Email
    |-- False -> Failure Summary -> Send Failure Email
```

### What n8n Does

The n8n workflow:

1. Starts from either a manual trigger or a weekly Monday 09:00 trigger.
2. The scheduled path downloads the latest `purchase.xlsx` file from Google Drive; the manual path intentionally tests the current local input.
3. Removes the previous local `data/purchase.xlsx` file so the new download can be written cleanly.
4. Saves the downloaded file as the local input used by the Python pipeline.
5. Runs the Python pipeline that generates the fRL winners Excel.
6. Checks whether the pipeline completed successfully.
7. Confirms that `outputs/fRL_winners.xlsx` exists.
8. Routes the result to a success or failure branch.
9. Updates the existing `fRL_winners.xlsx` file in Google Drive.
10. Sends a success email or failure alert email.

The `true` branch means the pipeline passed the success condition. In this project, that means the Python script ran, the output Excel file exists, and the workflow can mark the submission as ready.

The `false` branch handles validation failures returned by the Python runner. If the pipeline reports failure or the final Excel is missing, the workflow returns a clear review-needed message and sends a failure alert instead of silently passing.

### Assignment Coverage And Production Gaps

The assignment-facing workflow covers the full demonstrated path: manual run, weekly schedule, Drive input, local file handling, Python execution, IF routing, Drive output update, and professional success/failure email. A separate n8n Error Trigger workflow is not configured. Therefore, infrastructure failures that stop a node before the IF node, such as expired Drive credentials or a Gmail outage, appear in n8n Executions but do not send this workflow's failure email.

Before production use, add a dedicated Error Trigger workflow, retry policies for Drive/Gmail, run-level idempotency, and atomic input replacement. These are production hardening items, not missing assignment requirements.

### Notification Design

Both Gmail nodes use structured plain-text messages for consistent rendering across email clients.

- The success email confirms the input, output, Drive update, Streamlit link, and GitHub link.
- The failure email reports the failed stage and validation message, then lists three recommended recovery actions.
- Notification messages do not include credentials, raw execution logs, or source data attachments.
- The exported workflow keeps the recipient visible for review; a production deployment should move it to configuration.

### Local Runtime Note

This workflow uses the local Python project as the processing engine. For scheduled execution from local n8n, the laptop and n8n server must be running. The local n8n server should be started with file and built-in module access restricted to this assignment folder:

```powershell
$env:NODE_FUNCTION_ALLOW_BUILTIN="child_process,fs,path"
$env:N8N_BLOCK_ENV_ACCESS_IN_NODE="true"
$env:N8N_RESTRICT_FILE_ACCESS_TO="C:\Users\India\OneDrive\Desktop\Foundit_APMM_Assignment"
n8n
```

This setup is suitable for a local assignment demonstration. In a hosted production environment, the Python runner and credentials should be deployed with tighter infrastructure-level controls.

### Import And Configure The Workflow

The exported JSON contains workflow structure and credential references, but it does not contain OAuth secrets. To run it on another n8n instance:

1. Import `n8n/foundit_apmm_n8n_workflow.json`.
2. Create or select a Google Drive OAuth2 credential for the two Drive nodes.
3. Create or select a Gmail OAuth2 credential for the success and failure email nodes.
4. Confirm the source `purchase.xlsx` Drive file and destination `fRL_winners.xlsx` Drive file IDs.
5. Confirm the notification recipient in both Gmail nodes.
6. Update the three Windows paths if the project is stored in another folder.
7. Start n8n with the restricted module and file-access environment variables shown above.
8. Run once from `Weekly Scheduled Run` and verify the green success route.
9. Test the false branch with controlled test data and verify the failure notification.
10. Publish the validated workflow so the weekly schedule uses the latest version.

For a Linux/Docker host, import `n8n/foundit_apmm_n8n_workflow_hosted.json` instead. It uses the fixed paths packaged by `deploy/n8n/Dockerfile`, blocks Code-node environment access, and imports as inactive until configuration is complete.

### Why The Current n8n URL Is Local Only

`http://localhost:5678` resolves to the machine running n8n. It is not a public URL and other people cannot open it from the internet. The current workflow also uses:

- A Windows-only project path
- A local Python executable
- Local file read/write nodes
- `child_process`, `fs`, and `path` inside n8n Code nodes
- Google OAuth credentials stored in the local n8n instance

For those reasons, copying the workflow into n8n Cloud is not a drop-in deployment. The Python project must also run in the hosted environment, and all local paths must be replaced with server paths or a hosted pipeline API.

### Making n8n Public Safely

There are two different sharing goals:

#### Goal A - Let A Reviewer Inspect The Work

This is already covered without exposing the n8n editor:

- Public Streamlit app for the working agent and dashboards
- Public GitHub repository for source code and workflow JSON
- Success, failure, schedule, Drive, and email screenshots in `screenshots/`

This is the recommended assignment-review path. n8n workflow sharing is designed for users on the same n8n instance, not as an anonymous public read-only workflow link. See the official [workflow sharing documentation](https://docs.n8n.io/build/manage-workflows/share-with-others).

#### Goal B - Let Other Authorized Users Run n8n

The recommended production path is a protected self-hosted n8n instance using Docker on a VPS or cloud VM:

1. Provision a Linux server, domain or subdomain, and HTTPS reverse proxy.
2. Deploy n8n with Docker and persistent storage for `/home/node/.n8n`.
3. Build the supplied `deploy/n8n/Dockerfile`, which packages the repository and Python dependencies with n8n.
4. Replace Windows paths with server paths such as `/opt/foundit-apmm`.
5. Set a permanent `N8N_ENCRYPTION_KEY` in the host secret manager. Never commit it.
6. Set the public editor and webhook URLs:

```text
N8N_EDITOR_BASE_URL=https://n8n.example.com
N8N_WEBHOOK_URL=https://n8n.example.com/
N8N_PROXY_HOPS=1
GENERIC_TIMEZONE=Asia/Kolkata
```

7. Allow only the modules and folder needed by this workflow:

```text
NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs,path
N8N_RESTRICT_FILE_ACCESS_TO=/opt/foundit-apmm
N8N_BLOCK_ENV_ACCESS_IN_NODE=true
```

8. If external task runners are enabled, apply the Code-node module allow-list to the task-runner configuration, as described in the official [module configuration guide](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/enable-modules-in-code-node).
9. Add the hosted OAuth callback URL in Google Cloud, then recreate the Drive and Gmail credentials inside the hosted n8n instance.
10. Import `n8n/foundit_apmm_n8n_workflow_hosted.json`, test, publish, and invite only authorized users. Do not expose the editor without authentication.

Official references:

- [n8n hosting options](https://docs.n8n.io/deploy/)
- [Docker Compose hosting](https://docs.n8n.io/deploy/host-n8n/install-options/use-a-cloud-provider/use-docker-compose)
- [Reverse-proxy webhook configuration](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/configure-webhook-urls-with-reverse-proxy)
- [Workflow sharing and permissions](https://docs.n8n.io/build/manage-workflows/share-with-others)

The hosted deployment is intentionally documented rather than silently exposing the local editor through a temporary tunnel. A temporary tunnel would still depend on the laptop remaining online and would expand access to a workflow that can read files, run Python, update Drive, and send email.

### Business Value

The n8n layer is useful because it turns a code-based process into an operations workflow. A non-technical user can run the pipeline from a button and immediately see whether the output is ready or needs review.

In a production setup, the same workflow could be extended further to:

1. Use a hosted runner instead of a local laptop.
2. Move paths, Drive file IDs, and notification recipients into environment variables.
3. Add approval steps before replacing the final shared output.
4. Add Slack or Teams alerts in addition to email.
5. Store historical outputs for audit and comparison.
6. Add a separate Error Trigger workflow, retries, and run-level idempotency.

For this assignment, the n8n workflow is intentionally kept reviewable while still demonstrating end-to-end orchestration from file intake to output update and notification.

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

## Validation And Evidence

### Automated Validation

The repository is validated with:

```powershell
python run_pipeline.py
```

The command checks required inputs, syntax-checks Python, regenerates the fRL output, runs the Task 1 smoke test plus edge-case tests, and validates the workbook, notes, workflow exports, plain-text email mode, and screenshots.

### n8n Evidence Map

| Evidence | File |
|---|---|
| Published weekly scheduled end-to-end success route | `screenshots/n8n_full_workflow_success.png` |
| Manual success route | `screenshots/n8n_manual_success_route.png` |
| Controlled failure route and failure-email node | `screenshots/n8n_failure_route_and_email.png` |
| Weekly schedule configuration | `screenshots/n8n_weekly_schedule_settings.png` |
| Existing Drive output updated | `screenshots/n8n_drive_output_updated.png` |
| Success email received | `screenshots/n8n_success_email_received.png` |
| Failure email received | `screenshots/n8n_failure_email_received.png` |

The success and failure routes are tested separately. A successful scheduled run downloads the latest input, replaces the local file, executes Python, updates Drive, and sends the success notification. A controlled false-branch test confirms that validation failures are routed to the review summary and failure notification instead of updating the final Drive output.

### What Is Intentionally Not Included

- OAuth client secrets, access tokens, refresh tokens, passwords, and the local n8n database
- A public unauthenticated n8n editor
- Old-winner exclusion, because no old-winners file was supplied
- Salary or compensation answers, because the Task 1 source contains no compensation data
- A hosted n8n runtime, because the current workflow depends on a local Python and filesystem runtime; the safe migration path is documented above
- A separate workflow-level Error Trigger; the current false branch covers pipeline validation failures, while production node failures remain visible in n8n Executions

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

The Streamlit public link and GitHub repository link can be included in the email body. The hosted workflow export and Docker starter are operational extras and do not need to be attached unless the reviewer asks about deployment.

---

## Known Assumptions

- No old-winners file was provided, so old-winner exclusion was not applied.
- The Purchase file is the only required Task 2 source.
- Salary, CTC, notice period, and offer benchmarking are not available in the talent data, so the agent refuses those questions.
- The agent is intentionally grounded on the provided Excel data rather than external web data.
- The deterministic parser favors safe refusals over guesses: an unfamiliar paraphrase may be declined, but an unsupported constraint is never intentionally ignored to produce a broader number.

---

## Future Improvements

If this were converted into a production workflow, the next improvements would be:

1. Deploy the supplied Docker starter on a protected hosted environment and complete live infrastructure testing.
2. Apply the hosted export's environment-variable strategy to the live local workflow and externalize Drive IDs, recipients, and dates.
3. Add an audit sheet showing exclusion counts by reason and a versioned execution history.
4. Add old-winner file intake when that source becomes available.
5. Add explicit duplicate-winner and source-schema validation tests.
6. Add richer agent routing for more complex sales and customer-success questions.
7. Add an approval step before replacing the final shared Drive output.
8. Add Slack or Teams notifications and centralized production logging.

---

## Project Tagline

AI-assisted talent supply lookup and recruiter-league winner automation for foundit-style Sales, CS, and Product Marketing workflows.
