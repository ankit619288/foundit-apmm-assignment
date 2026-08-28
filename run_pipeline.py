from pathlib import Path
import json
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
NOTES_DIR = BASE_DIR / "notes"
N8N_DIR = BASE_DIR / "n8n"
DEPLOY_N8N_DIR = BASE_DIR / "deploy" / "n8n"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

REQUIRED_FILES = [
    DATA_DIR / "Assignment_brief.pdf",
    DATA_DIR / "Sample_Data_for_agent.xlsx",
    DATA_DIR / "purchase.xlsx",
    DATA_DIR / "winner.py",
]

EXPECTED_OUTPUTS = [
    OUTPUT_DIR / "fRL_winners.xlsx",
    NOTES_DIR / "frl_method_note.md",
    NOTES_DIR / "task1_system_prompt.md",
    NOTES_DIR / "task1_test_qna.md",
    NOTES_DIR / "task3_bonus_analysis.md",
    BASE_DIR / "README.md",
    BASE_DIR / "requirements.txt",
    N8N_DIR / "foundit_apmm_n8n_workflow.json",
    N8N_DIR / "foundit_apmm_n8n_workflow_hosted.json",
    DEPLOY_N8N_DIR / "Dockerfile",
    DEPLOY_N8N_DIR / "compose.yaml",
    DEPLOY_N8N_DIR / ".env.example",
    DEPLOY_N8N_DIR / "README.md",
]

EXPECTED_SCREENSHOTS = [
    "n8n_drive_output_updated.png",
    "n8n_failure_email_received.png",
    "n8n_failure_route_and_email.png",
    "n8n_full_workflow_success.png",
    "n8n_manual_success_route.png",
    "n8n_success_email_received.png",
    "n8n_weekly_schedule_settings.png",
]

MIN_SCREENSHOT_BYTES = 100_000


def check_required_files():
    print("\nChecking required input files...")
    missing = []

    for file_path in REQUIRED_FILES:
        if file_path.exists():
            print(f"OK: {file_path.name}")
        else:
            print(f"MISSING: {file_path.name}")
            missing.append(file_path)

    if missing:
        raise FileNotFoundError("Some assignment input files are missing.")


def run_command(command):
    print(f"\nRunning: {' '.join(command)}")
    result = subprocess.run(command, cwd=BASE_DIR)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}")


def check_outputs():
    print("\nChecking generated submission files...")
    missing = []

    for file_path in EXPECTED_OUTPUTS:
        if file_path.exists():
            print(f"OK: {file_path.relative_to(BASE_DIR)}")
        else:
            print(f"MISSING: {file_path.relative_to(BASE_DIR)}")
            missing.append(file_path)

    screenshot_count = len(list(SCREENSHOT_DIR.glob("*.png"))) if SCREENSHOT_DIR.exists() else 0
    missing_screenshots = [
        name for name in EXPECTED_SCREENSHOTS if not (SCREENSHOT_DIR / name).exists()
    ]
    if missing_screenshots:
        for name in missing_screenshots:
            print(f"MISSING: screenshots/{name}")
            missing.append(SCREENSHOT_DIR / name)
    else:
        print(
            f"OK: all {len(EXPECTED_SCREENSHOTS)} required n8n screenshots "
            f"({screenshot_count} total PNG files)"
        )

    undersized_screenshots = [
        SCREENSHOT_DIR / name
        for name in EXPECTED_SCREENSHOTS
        if (SCREENSHOT_DIR / name).exists()
        and (SCREENSHOT_DIR / name).stat().st_size < MIN_SCREENSHOT_BYTES
    ]
    for screenshot_path in undersized_screenshots:
        print(f"INVALID: {screenshot_path.relative_to(BASE_DIR)} is unexpectedly small")
        missing.append(screenshot_path)

    bonus_note = NOTES_DIR / "task3_bonus_analysis.md"
    if bonus_note.exists():
        bonus_text = bonus_note.read_text(encoding="utf-8")
        bonus_valid = (
            bonus_text.count("```") % 2 == 0
            and "## Data-Backed Insights" in bonus_text
            and "## Recommended Improvements" in bonus_text
            and "Task 2" in bonus_text
        )
        if bonus_valid:
            print("OK: Task 3 bonus analysis is complete and linked to Task 2")
        else:
            print("INVALID: notes/task3_bonus_analysis.md is incomplete")
            missing.append(bonus_note)

    method_note = NOTES_DIR / "frl_method_note.md"
    if method_note.exists():
        method_lines = [
            line
            for line in method_note.read_text(encoding="utf-8").splitlines()
            if line.startswith("- ")
        ]
        if len(method_lines) == 5:
            print("OK: Task 2 method note contains the requested 5 concise lines")
        else:
            print("INVALID: Task 2 method note must contain exactly 5 bullet lines")
            missing.append(method_note)

    workflow_expectations = [
        (N8N_DIR / "foundit_apmm_n8n_workflow.json", True),
        (N8N_DIR / "foundit_apmm_n8n_workflow_hosted.json", False),
    ]
    for workflow_path, expected_active in workflow_expectations:
        if not workflow_path.exists():
            continue
        try:
            workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
            node_names = [node["name"] for node in workflow.get("nodes", [])]
            valid = (
                len(node_names) == 13
                and len(node_names) == len(set(node_names))
                and "Clear Old Purchase File" in node_names
                and workflow.get("active") is expected_active
            )
        except (json.JSONDecodeError, KeyError, TypeError):
            valid = False

        if valid:
            print(
                f"OK: {workflow_path.relative_to(BASE_DIR)} "
                f"(13 nodes, active={expected_active})"
            )
        else:
            print(f"INVALID: {workflow_path.relative_to(BASE_DIR)}")
            missing.append(workflow_path)

    return missing


def main():
    print("Foundit APMM Automation Pipeline")
    print("=" * 40)

    OUTPUT_DIR.mkdir(exist_ok=True)
    NOTES_DIR.mkdir(exist_ok=True)

    check_required_files()

    run_command(
        [
            sys.executable,
            "-m",
            "py_compile",
            "src/app.py",
            "src/talent_agent.py",
            "src/calculate_frl_winners.py",
            "run_pipeline.py",
            "tests/test_core.py",
        ]
    )
    run_command([sys.executable, "src/calculate_frl_winners.py"])
    run_command([sys.executable, "src/talent_agent.py"])
    run_command(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ]
    )

    missing_outputs = check_outputs()
    if missing_outputs:
        raise FileNotFoundError("Some generated submission files are missing.")

    print("\nPipeline completed.")
    print("To open the dashboard, run:")
    print("python -m streamlit run src/app.py")


if __name__ == "__main__":
    main()
