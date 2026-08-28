from pathlib import Path
import re

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

TALENT_FILE = DATA_DIR / "Sample_Data_for_agent.xlsx"
SHEET_NAME = "India - ITITeS"

METRICS = [
    "Total Profiles",
    "All Time Sourced",
    "All Time Registered",
    "12M Active Profiles",
    "12M Sourced",
    "12M Registered",
    "6M Active Profiles",
    "6M Sourced",
    "6M Registered",
]

CATEGORY_ALIASES = {
    "devops talent": "DevOps Engineer",
    "devops": "DevOps Engineer",
    "ai ml engineer": "AI/ML Engineer",
    "ai ml": "AI/ML Engineer",
    "ml engineer": "AI/ML Engineer",
    "machine learning": "AI/ML Engineer",
    "ai engineer": "AI/ML Engineer",
    "ml": "AI/ML Engineer",
    "data science": "Data Scientist",
    "data scientists": "Data Scientist",
    "women": "Female",
    "woman": "Female",
    "men": "Male",
    "cyber security": "Cybersecurity Analyst/Engineer",
    "cybersecurity": "Cybersecurity Analyst/Engineer",
    "cloud architect": "Cloud Architect/Engineer",
    "cloud engineer": "Cloud Architect/Engineer",
    "bangalore": "Bengaluru",
    "chandigarh": "Chandigrah",
    "delhi": "Delhi NCR",
    "ncr": "Delhi NCR",
    "3-5y": "3-5 Years",
    "3 to 5": "3-5 Years",
    "1-3y": "1-3 Years",
    "1 to 3": "1-3 Years",
    "0-1y": "0-1 years",
    "5-10y": "5-10Years",
    "10-15y": "10-15 Years",
    "15y+": "15 Years+",
    "15+ years": "15 Years+",
}

UNAVAILABLE_KEYWORDS = [
    "salary",
    "ctc",
    "offer",
    "compensation",
    "pay",
    "package",
    "notice period",
    "joining time",
    "available immediately",
    "hiring cost",
]

ROLE_HINT_PATTERN = re.compile(
    r"(?<!\w)(developers?|engineers?|scientists?|architects?|analysts?|devops|"
    r"cybersecurity|cyber security|machine learning|ai/ml|ai ml|ml)(?!\w)"
)


def clean_label(value):
    if pd.isna(value):
        return ""
    return str(value).replace("\u00a0", " ").strip()


def normalize_text(value):
    text = clean_label(value).lower()
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\s*-\s*", "-", text)
    return " ".join(text.split())


def phrase_in_text(phrase, text):
    phrase = normalize_text(phrase)
    if not phrase:
        return False
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text) is not None


def canonical_metric(value):
    normalized = normalize_text(value)
    aliases = {
        "total profiles": "Total Profiles",
        "all time sourced": "All Time Sourced",
        "all time registered": "All Time Registered",
        "12m active profiles": "12M Active Profiles",
        "12m sourced": "12M Sourced",
        "12m registered": "12M Registered",
        "6m active profiles": "6M Active Profiles",
        "6m sourced": "6M Sourced",
        "6m registered": "6M Registered",
        "6m reg": "6M Registered",
    }
    return aliases.get(normalized)


def canonical_section(value):
    normalized = normalize_text(value)
    sections = {
        "by gender": "Gender",
        "by experience": "Experience",
        "location": "Location",
        "tier ii cities": "Tier II City",
        "tier iii cities": "Tier III City",
        "roles": "Role",
        "sub industry": "Sub Industry",
    }
    return sections.get(normalized, clean_label(value))


def to_number(value):
    number = pd.to_numeric(value, errors="coerce")
    return None if pd.isna(number) else float(number)


def load_raw_talent_data():
    return pd.read_excel(TALENT_FILE, sheet_name=SHEET_NAME)


def load_talent_data():
    """Parse the semi-structured sheet into category rows with all nine metrics."""
    raw_df = load_raw_talent_data()
    rows = []
    section = "Overall"
    metric_columns = {}

    for _, row in raw_df.iterrows():
        label = clean_label(row.iloc[0])
        count_value = row.iloc[1]

        if label and isinstance(count_value, str):
            section = canonical_section(label)
            metric_columns = {}
            for column in raw_df.columns[1:]:
                metric = canonical_metric(row[column])
                if metric:
                    metric_columns[column] = metric
            continue

        count = to_number(count_value)
        if not label or count is None:
            continue

        values = {metric: None for metric in METRICS}
        if metric_columns:
            for column, metric in metric_columns.items():
                values[metric] = to_number(row[column])
        else:
            values["Total Profiles"] = count
            label = canonical_metric(label) or label

        profiles = values["Total Profiles"]
        if profiles is None:
            continue

        rows.append(
            {
                "Category": label,
                "Category Lower": normalize_text(label),
                "Section": section,
                "Profiles": profiles,
                "Profiles Display": format_count(profiles),
                **values,
            }
        )

    return pd.DataFrame(rows)


def load_talent_kb():
    return load_talent_data().to_dict("records")


def format_count(value):
    value = float(value)
    if value >= 10_000_000:
        return f"{value / 10_000_000:.2f} Cr"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f} Mn"
    if value >= 100_000:
        return f"{value / 1000:.0f}K"
    if value.is_integer():
        return f"{int(value):,}"
    return f"{value:,.1f}"


def metric_answer_label(metric):
    labels = {
        "Total Profiles": "profiles",
        "All Time Sourced": "all-time sourced profiles",
        "All Time Registered": "all-time registered profiles",
        "12M Active Profiles": "12M active profiles",
        "12M Sourced": "12M sourced profiles",
        "12M Registered": "12M registered profiles",
        "6M Active Profiles": "6M active profiles",
        "6M Sourced": "6M sourced profiles",
        "6M Registered": "6M registered profiles",
    }
    return labels[metric]


def detect_metric(question):
    q = normalize_text(question)
    has_12m = bool(re.search(r"(?<!\w)(12m|12 months?|12-months?)(?!\w)", q))
    has_6m = bool(re.search(r"(?<!\w)(6m|6 months?|6-months?)(?!\w)", q))

    if has_12m:
        if "sourced" in q:
            return "12M Sourced"
        if "registered" in q or phrase_in_text("reg", q):
            return "12M Registered"
        return "12M Active Profiles"

    if has_6m:
        if "sourced" in q:
            return "6M Sourced"
        if "registered" in q or phrase_in_text("reg", q):
            return "6M Registered"
        return "6M Active Profiles"

    if "all time sourced" in q or "all-time sourced" in q:
        return "All Time Sourced"
    if "all time registered" in q or "all-time registered" in q:
        return "All Time Registered"
    if "sourced" in q:
        return "All Time Sourced"
    if "registered" in q:
        return "All Time Registered"
    return "Total Profiles"


def find_matches(question, talent_df):
    q = normalize_text(question)
    matches = {}

    for _, item in talent_df.iterrows():
        if phrase_in_text(item["Category Lower"], q):
            matches[item["Category"]] = item

    category_lookup = {
        normalize_text(item["Category"]): item for _, item in talent_df.iterrows()
    }
    for alias, category in sorted(
        CATEGORY_ALIASES.items(), key=lambda pair: len(pair[0]), reverse=True
    ):
        if phrase_in_text(alias, q):
            item = category_lookup.get(normalize_text(category))
            if item is not None:
                matches[item["Category"]] = item

    return list(matches.values())


def value_for_metric(item, metric):
    if item["Section"] == "Overall" and canonical_metric(item["Category"]) == metric:
        return item["Profiles"]
    value = item.get(metric)
    return None if pd.isna(value) else float(value)


def comparison_answer(question, talent_df, matches=None):
    metric = detect_metric(question)
    matches = find_matches(question, talent_df) if matches is None else matches
    matches = [item for item in matches if value_for_metric(item, metric) is not None]
    if len(matches) != 2:
        return None

    first, second = matches
    first_count = value_for_metric(first, metric)
    second_count = value_for_metric(second, metric)

    if first_count == second_count:
        return (
            f"{first['Category']} and {second['Category']} have the same "
            f"{metric.lower()}: {format_count(first_count)} profiles each."
        )

    larger, smaller = (
        (first, second) if first_count > second_count else (second, first)
    )
    larger_count = value_for_metric(larger, metric)
    smaller_count = value_for_metric(smaller, metric)
    difference = larger_count - smaller_count
    metric_context = (
        "" if metric == "Total Profiles" else f" for {metric_answer_label(metric)}"
    )
    return (
        f"{larger['Category']} is larger than {smaller['Category']} by "
        f"{format_count(difference)} profiles{metric_context}. "
        f"{larger['Category']} has {format_count(larger_count)}, while "
        f"{smaller['Category']} has {format_count(smaller_count)}."
    )


def unavailable_answer():
    return (
        "I could not find that answer in the provided dataset. I can answer "
        "questions about talent counts by role, city, experience band, gender, "
        "sub-industry, and the total, active, sourced, or registered metrics "
        "available in Sample_Data_for_agent.xlsx."
    )


def agent_answer(question, talent_df=None):
    talent_df = load_talent_data() if talent_df is None else talent_df
    q = normalize_text(question)

    if any(phrase_in_text(keyword, q) for keyword in UNAVAILABLE_KEYWORDS):
        return (
            "The provided dataset does not include salary, CTC, compensation, "
            "notice period, hiring cost, or offer benchmarking data. I can only "
            "answer from the available India IT/ITeS talent-supply counts."
        )

    metric = detect_metric(q)
    matches = find_matches(q, talent_df)
    non_overall = [item for item in matches if item["Section"] != "Overall"]
    if non_overall:
        matches = non_overall

    role_matches = [item for item in matches if item["Section"] == "Role"]
    if ROLE_HINT_PATTERN.search(q) and not role_matches:
        return unavailable_answer()

    comparison_requested = any(
        phrase_in_text(word, q)
        for word in ["compare", "larger", "more", "vs", "versus"]
    )
    if comparison_requested:
        answer = comparison_answer(q, talent_df, matches)
        if answer:
            return answer
        return (
            "I could not make that comparison from the provided dataset. "
            "Please name exactly two available roles, cities, experience bands, "
            "gender categories, or sub-industries."
        )

    sections = {item["Section"] for item in matches}
    if len(matches) > 1 or len(sections) > 1:
        return (
            "The dataset provides separate aggregate cuts, not a cross-tabbed "
            "intersection for those categories. I can report each available "
            "category separately, but I should not invent a combined count."
        )

    if not matches:
        total = talent_df[talent_df["Category Lower"] == "total profiles"]
        if "total" in q and not total.empty:
            return (
                f"Total India IT/ITeS profiles are "
                f"{format_count(total.iloc[0]['Profiles'])} in the provided dataset."
            )
        return unavailable_answer()

    match = matches[0]
    value = value_for_metric(match, metric)
    if value is None:
        return unavailable_answer()

    if match["Section"] == "Overall":
        if normalize_text(match["Category"]) == "total profiles":
            return (
                f"Total India IT/ITeS profiles are {format_count(value)} "
                "in the provided dataset."
            )
        return (
            f"{match['Category']} are {format_count(value)} "
            "in the provided India IT/ITeS talent-supply dataset."
        )

    metric_text = metric_answer_label(metric)
    return (
        f"{match['Category']} has {format_count(value)} {metric_text} "
        "in the provided India IT/ITeS talent-supply dataset."
    )


def run_demo_questions():
    questions = [
        "How many AI/ML Engineer profiles are available in India?",
        "Which is larger - Data Scientist or DevOps talent, and by how much?",
        "What salary should I offer a DevOps engineer in Pune?",
    ]

    talent_df = load_talent_data()
    print("\nFoundit Talent Intelligence Agent - Demo")
    print("-" * 60)
    for question in questions:
        print(f"\nQuestion: {question}")
        print(f"Answer: {agent_answer(question, talent_df)}")


if __name__ == "__main__":
    run_demo_questions()
