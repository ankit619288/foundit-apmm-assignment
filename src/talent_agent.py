from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

TALENT_FILE = DATA_DIR / "Sample_Data_for_agent.xlsx"
SHEET_NAME = "India - ITITeS"


def load_raw_talent_data():
    return pd.read_excel(TALENT_FILE, sheet_name=SHEET_NAME)


def clean_label(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_text(value):
    return clean_label(value).lower()


def normalize_role_aliases(text):
    aliases = {
        "devops talent": "devops engineer",
        "devops": "devops engineer",
        "ai/ml": "ai/ml engineer",
        "ai ml": "ai/ml engineer",
        "ai engineer": "ai/ml engineer",
        "ml": "ai/ml engineer",
        "machine learning": "ai/ml engineer",
        "data science": "data scientist",
        "data scientists": "data scientist",
        "bangalore": "bengaluru",
        "cyber security": "cybersecurity analyst/engineer",
    }

    normalized = text

    for old, new in aliases.items():
        normalized = normalized.replace(old, new)

    return normalized


def load_talent_kb():
    """
    Converts the assignment Excel into a simple searchable knowledge base.
    The file is semi-structured, so we read the first label column and count column.
    """
    df = load_raw_talent_data()

    kb = []

    for _, row in df.iterrows():
        label = clean_label(row.get("Unnamed: 0"))
        count = row.get("Count")

        if not label:
            continue

        if pd.isna(count):
            continue

        try:
            count = int(count)
        except Exception:
            continue

        kb.append(
            {
                "label": label,
                "label_lower": label.lower(),
                "count": count,
            }
        )

    return kb


def format_count(value):
    if value >= 10_000_000:
        return f"{value / 10_000_000:.2f} Cr"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f} Mn"
    if value >= 100_000:
        return f"{value / 1000:.0f}K"
    return f"{value:,}"


def find_best_match(question, kb):
    q = normalize_role_aliases(normalize_text(question))

    exact_matches = []
    partial_matches = []

    for item in kb:
        label = item["label_lower"]

        if label in q:
            exact_matches.append(item)
        elif any(word in q for word in label.split() if len(word) > 2):
            partial_matches.append(item)

    if exact_matches:
        return exact_matches[0]

    if partial_matches:
        partial_matches = sorted(
            partial_matches,
            key=lambda x: len(x["label"]),
            reverse=True,
        )
        return partial_matches[0]

    return None


def compare_two_roles(question, kb):
    q = normalize_role_aliases(normalize_text(question))

    matched_items = []

    for item in kb:
        label = item["label_lower"]

        if label in q:
            matched_items.append(item)

    if len(matched_items) < 2:
        return None

    first = matched_items[0]
    second = matched_items[1]

    difference = abs(first["count"] - second["count"])

    if first["count"] > second["count"]:
        larger = first
        smaller = second
    else:
        larger = second
        smaller = first

    return (
        f"{larger['label']} is larger than {smaller['label']} by "
        f"{format_count(difference)} profiles. "
        f"{larger['label']} has {format_count(larger['count'])}, while "
        f"{smaller['label']} has {format_count(smaller['count'])}."
    )


def agent_answer(question):
    kb = load_talent_kb()
    q = normalize_role_aliases(normalize_text(question))

    unavailable_keywords = [
        "salary",
        "ctc",
        "offer",
        "compensation",
        "pay",
        "package",
        "notice period",
        "joining time",
        "available immediately",
    ]

    if any(keyword in q for keyword in unavailable_keywords):
        return (
            "The provided dataset does not include salary, CTC, compensation, "
            "notice period, or offer benchmarking data. I can only answer from "
            "the available IT/ITeS talent-supply counts."
        )

    if "compare" in q or "larger" in q or "more" in q or "vs" in q:
        comparison = compare_two_roles(question, kb)
        if comparison:
            return comparison

    match = find_best_match(question, kb)

    if match:
        return (
            f"{match['label']} has {format_count(match['count'])} profiles "
            f"in the provided India IT/ITeS talent-supply dataset."
        )

    total_match = next(
        (item for item in kb if item["label_lower"] == "total profiles"),
        None,
    )

    if "total" in q and total_match:
        return (
            f"Total India IT/ITeS profiles are "
            f"{format_count(total_match['count'])} in the provided dataset."
        )

    return (
        "I could not find that answer in the provided dataset. "
        "I can answer questions about available talent counts by role, city, "
        "experience, gender, and other categories present in Sample_Data_for_agent.xlsx."
    )


def run_demo_questions():
    questions = [
        "How many AI/ML Engineer profiles are available in India?",
        "Which is larger - Data Scientist or DevOps talent, and by how much?",
        "What salary should I offer a DevOps engineer in Pune?",
    ]

    print("\nFoundit Talent Intelligence Agent - Demo")
    print("-" * 60)

    for question in questions:
        print(f"\nQuestion: {question}")
        print(f"Answer: {agent_answer(question)}")


if __name__ == "__main__":
    run_demo_questions()
