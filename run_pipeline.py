from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
NOTES_DIR = BASE_DIR / "notes"

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
]

EXPECTED_SCREENSHOT_MIN_COUNT = 6


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

    screenshot_dir = BASE_DIR / "screenshots"
    screenshot_count = len(list(screenshot_dir.glob("*.png"))) if screenshot_dir.exists() else 0
    if screenshot_count >= EXPECTED_SCREENSHOT_MIN_COUNT:
        print(f"OK: screenshots folder ({screenshot_count} PNG files)")
    else:
        print(
            f"MISSING: screenshots folder needs at least "
            f"{EXPECTED_SCREENSHOT_MIN_COUNT} PNG files; found {screenshot_count}"
        )
        missing.append(screenshot_dir)

    return missing


def main():
    print("Foundit APMM Automation Pipeline")
    print("=" * 40)

    OUTPUT_DIR.mkdir(exist_ok=True)
    NOTES_DIR.mkdir(exist_ok=True)

    check_required_files()

    run_command([sys.executable, "src/calculate_frl_winners.py"])
    run_command([sys.executable, "src/talent_agent.py"])

    missing_outputs = check_outputs()
    if missing_outputs:
        raise FileNotFoundError("Some generated submission files are missing.")

    print("\nPipeline completed.")
    print("To open the dashboard, run:")
    print("python -m streamlit run src/app.py")


if __name__ == "__main__":
    main()
