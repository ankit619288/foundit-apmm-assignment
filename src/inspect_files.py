from pathlib import Path
import pandas as pd
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

FILES = {
    "Assignment Brief": DATA_DIR / "Assignment_brief.pdf",
    "Talent Data": DATA_DIR / "Sample_Data_for_agent.xlsx",
    "Purchase Data": DATA_DIR / "purchase.xlsx",
    "Winner Script": DATA_DIR / "winner.py",
}

def check_files():
    print("\nFILE CHECK")
    print("-" * 60)

    for name, path in FILES.items():
        status = "FOUND" if path.exists() else "MISSING"
        size = path.stat().st_size if path.exists() else 0
        print(f"{name}: {status} | {path.name} | {size} bytes")

def inspect_pdf():
    pdf_path = FILES["Assignment Brief"]

    print("\nPDF BRIEF")
    print("-" * 60)

    if not pdf_path.exists():
        print("Assignment brief PDF not found.")
        return

    reader = PdfReader(str(pdf_path))
    print(f"Pages: {len(reader.pages)}")

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        print(f"\n--- Page {i} Preview ---")
        print(text[:1500])

def inspect_excel_file(label, path):
    print(f"\n{label.upper()}")
    print("-" * 60)

    if not path.exists():
        print(f"{label} not found.")
        return

    excel = pd.ExcelFile(path)
    print("Sheets:", excel.sheet_names)

    for sheet in excel.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        print(f"\nSheet: {sheet}")
        print("Shape:", df.shape)
        print("Columns:")
        for col in df.columns:
            print(f"  - {col}")

        print("\nSample rows:")
        print(df.head(3).to_string(index=False))

def inspect_winner_script():
    script_path = FILES["Winner Script"]

    print("\nWINNER.PY PREVIEW")
    print("-" * 60)

    if not script_path.exists():
        print("winner.py not found.")
        return

    text = script_path.read_text(encoding="utf-8", errors="ignore")
    print(text[:3000])

def main():
    check_files()
    inspect_pdf()
    inspect_excel_file("Talent Data", FILES["Talent Data"])
    inspect_excel_file("Purchase Data", FILES["Purchase Data"])
    inspect_winner_script()

if __name__ == "__main__":
    main()