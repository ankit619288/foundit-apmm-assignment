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
    "ai/ml engineers": "AI/ML Engineer",
    "ai/ml engineer": "AI/ML Engineer",
    "ai/ml": "AI/ML Engineer",
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
    "cloud architects": "Cloud Architect/Engineer",
    "cloud architect": "Cloud Architect/Engineer",
    "cloud engineers": "Cloud Architect/Engineer",
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
    "0-1 year": "0-1 years",
    "0 to 1": "0-1 years",
    "0 to 1 years": "0-1 years",
    "5-10y": "5-10Years",
    "5-10 years": "5-10Years",
    "5 to 10 years": "5-10Years",
    "10-15y": "10-15 Years",
    "10 to 15": "10-15 Years",
    "10 to 15 years": "10-15 Years",
    "15y+": "15 Years+",
    "15+ years": "15 Years+",
    "15 years and above": "15 Years+",
    "15 years or more": "15 Years+",
}

LOCATION_SECTIONS = {"Location", "Tier II City", "Tier III City"}

QUERY_FILLER_TOKENS = {
    "a",
    "about",
    "active",
    "all",
    "among",
    "an",
    "and",
    "approximately",
    "are",
    "around",
    "architect",
    "architects",
    "at",
    "availability",
    "available",
    "based",
    "be",
    "between",
    "bigger",
    "by",
    "can",
    "candidate",
    "candidates",
    "categories",
    "category",
    "city",
    "cities",
    "compare",
    "compared",
    "comparison",
    "count",
    "counts",
    "could",
    "currently",
    "data",
    "database",
    "dataset",
    "developer",
    "developers",
    "did",
    "difference",
    "do",
    "does",
    "during",
    "each",
    "engineer",
    "engineers",
    "exact",
    "exactly",
    "experience",
    "female",
    "find",
    "for",
    "from",
    "gender",
    "give",
    "greater",
    "had",
    "has",
    "have",
    "headcount",
    "higher",
    "how",
    "i",
    "in",
    "india",
    "indian",
    "industry",
    "is",
    "it",
    "it/ites",
    "ites",
    "large",
    "larger",
    "last",
    "less",
    "located",
    "location",
    "locations",
    "lower",
    "m",
    "male",
    "many",
    "month",
    "months",
    "more",
    "most",
    "much",
    "number",
    "numbers",
    "of",
    "on",
    "or",
    "overall",
    "over",
    "past",
    "please",
    "pool",
    "previous",
    "profile",
    "profiles",
    "provide",
    "provided",
    "registered",
    "reg",
    "role",
    "roles",
    "scientist",
    "scientists",
    "show",
    "should",
    "six",
    "size",
    "smaller",
    "sourced",
    "sub",
    "supply",
    "s",
    "talent",
    "tell",
    "than",
    "that",
    "the",
    "there",
    "time",
    "to",
    "total",
    "twelve",
    "using",
    "versus",
    "vs",
    "was",
    "we",
    "were",
    "what",
    "which",
    "with",
    "within",
    "work",
    "working",
    "would",
    "you",
}

MONTH_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}

EXPERIENCE_REQUEST_PATTERN = re.compile(
    r"(?<!\w)(?:\d+\s*(?:-|to)\s*\d+|\d+\+|\d+)\s*"
    r"(?:years?|yrs?|y)(?!\w)"
)

DIMENSION_PATTERNS = {
    "Location": re.compile(r"(?<!\w)(?:locations?|cities?|city)(?!\w)"),
    "Role": re.compile(r"(?<!\w)roles?(?!\w)"),
    "Gender": re.compile(r"(?<!\w)gender(?!\w)"),
    "Experience": re.compile(r"(?<!\w)experience(?:\s+bands?)?(?!\w)"),
    "Sub Industry": re.compile(
        r"(?<!\w)(?:sub(?:-|\s*)industr(?:y|ies)|industr(?:y|ies))(?!\w)"
    ),
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

    talent_df = pd.DataFrame(rows)
    validate_talent_data(talent_df)
    return talent_df


def validate_talent_data(talent_df):
    """Fail closed if the source workbook no longer matches its expected schema."""
    if talent_df.empty:
        raise ValueError("Talent dataset did not produce any usable rows.")

    required_sections = {
        "Overall",
        "Gender",
        "Experience",
        "Location",
        "Tier II City",
        "Tier III City",
        "Role",
        "Sub Industry",
    }
    missing_sections = required_sections.difference(talent_df["Section"])
    if missing_sections:
        raise ValueError(
            "Talent dataset is missing required sections: "
            + ", ".join(sorted(missing_sections))
        )

    duplicate_categories = talent_df["Category Lower"].duplicated(keep=False)
    if duplicate_categories.any():
        duplicates = sorted(talent_df.loc[duplicate_categories, "Category"].unique())
        raise ValueError(
            "Talent dataset has ambiguous duplicate categories: "
            + ", ".join(duplicates)
        )

    overall = talent_df[talent_df["Section"] == "Overall"]
    overall_metrics = {
        canonical_metric(category)
        for category in overall["Category"]
        if canonical_metric(category)
    }
    missing_overall_metrics = set(METRICS).difference(overall_metrics)
    if missing_overall_metrics:
        raise ValueError(
            "Talent dataset is missing overall metrics: "
            + ", ".join(sorted(missing_overall_metrics))
        )

    category_rows = talent_df[talent_df["Section"] != "Overall"]
    missing_metric_values = category_rows[METRICS].isna().any(axis=1)
    if missing_metric_values.any():
        categories = sorted(
            category_rows.loc[missing_metric_values, "Category"].unique()
        )
        raise ValueError(
            "Talent dataset has incomplete metric rows for: "
            + ", ".join(categories)
        )

    if (talent_df[METRICS].fillna(0) < 0).any().any():
        raise ValueError("Talent dataset contains a negative profile count.")


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


def detect_month_windows(question):
    q = normalize_text(question)
    pattern = re.compile(
        r"(?<!\w)(\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
        r"eleven|twelve)\s*-?\s*(?:m|months?|month)(?!\w)"
    )
    windows = []
    for match in pattern.finditer(q):
        raw_value = match.group(1)
        windows.append(int(raw_value) if raw_value.isdigit() else MONTH_WORDS[raw_value])
    return windows


def detect_metric_request(question):
    """Return a supported metric or a fail-closed explanation."""
    q = normalize_text(question)
    windows = detect_month_windows(q)
    distinct_windows = set(windows)

    if any(window not in {6, 12} for window in distinct_windows):
        return None, (
            "The provided dataset does not include that time window. It only "
            "contains 6-month and 12-month active, sourced, and registered cuts, "
            "so I should not substitute a total-profile number."
        )
    if len(distinct_windows) > 1:
        return None, (
            "The question contains more than one time window. Please request "
            "either the 6-month or the 12-month metric so I do not combine them."
        )

    unsupported_relative_time = re.search(
        r"(?<!\w)(?:today|yesterday|ytd|mtd|qtd|last quarter|past quarter|"
        r"previous quarter|last weeks?|past weeks?|previous weeks?|last months?|"
        r"past months?|previous months?|last year|past year|previous year|"
        r"this day|this week|this month|this quarter|this year|"
        r"current day|current week|current month|current quarter|current year|"
        r"over time|across time|by time)(?!\w)",
        q,
    ) or re.search(
        r"(?<!\w)(?:last|past|previous|within)\s+"
        r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
        r"\s+(?:days?|weeks?|quarters?|years?)(?!\w)",
        q,
    )
    if not distinct_windows:
        unsupported_relative_time = unsupported_relative_time or re.search(
            r"(?<!\w)(?:in|during|for|per|by)\s+(?:a\s+|the\s+)?"
            r"months?(?!\w)",
            q,
        )
    if unsupported_relative_time or re.search(r"(?<!\w)(?:19|20)\d{2}(?!\w)", q):
        return None, (
            "The provided dataset does not include that calendar period. It only "
            "contains total, 6-month, and 12-month measures, so I cannot infer "
            "a value for the requested period."
        )

    has_active = phrase_in_text("active", q)
    has_sourced = phrase_in_text("sourced", q)
    has_registered = phrase_in_text("registered", q) or phrase_in_text("reg", q)
    qualifiers = [has_active, has_sourced, has_registered]
    if sum(qualifiers) > 1:
        return None, (
            "Please request one measure at a time: active, sourced, or registered. "
            "I should not choose between multiple requested measures."
        )

    if distinct_windows:
        window = distinct_windows.pop()
        if not any(qualifiers):
            return None, (
                f"The dataset has separate {window}-month active, sourced, and "
                "registered counts. Please specify which measure you need."
            )
        suffix = (
            "Active Profiles"
            if has_active
            else "Sourced"
            if has_sourced
            else "Registered"
        )
        return f"{window}M {suffix}", None

    has_all_time = bool(re.search(r"(?<!\w)all(?:-| )time(?!\w)", q))
    if has_active:
        return None, (
            "The dataset has both 6-month and 12-month active counts. Please "
            "specify the required time window so I do not choose one arbitrarily."
        )
    if has_sourced or has_registered:
        if not has_all_time:
            return None, (
                "The dataset has all-time, 6-month, and 12-month values for this "
                "measure. Please specify the time window so I do not assume one."
            )
        return ("All Time Sourced" if has_sourced else "All Time Registered"), None

    return "Total Profiles", None


def detect_metric(question):
    metric, _ = detect_metric_request(question)
    return metric or "Total Profiles"


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


def unmatched_constraint_terms(question, talent_df):
    """Find substantive query terms that the knowledge base did not recognize."""
    residue = normalize_text(question)
    residue = re.sub(
        r"(?<!\w)(?:tell|show|give|provide)\s+me(?!\w)",
        " ",
        residue,
    )
    residue = re.sub(
        r"(?<!\w)(?:6|12|six|twelve)\s*-?\s*(?:m|months?|month)(?!\w)",
        " ",
        residue,
    )
    recognized_phrases = set(talent_df["Category Lower"].dropna().tolist())
    recognized_phrases.update(CATEGORY_ALIASES)

    for phrase in sorted(recognized_phrases, key=len, reverse=True):
        if phrase_in_text(phrase, residue):
            residue = re.sub(
                rf"(?<!\w){re.escape(normalize_text(phrase))}(?!\w)",
                " ",
                residue,
            )

    tokens = re.findall(r"[a-z0-9]+(?:/[a-z0-9]+)?", residue)
    return sorted(
        {
            token
            for token in tokens
            if token not in QUERY_FILLER_TOKENS
            and token not in {"6m", "12m"}
        }
    )


def has_unmatched_experience(question, matches):
    if not EXPERIENCE_REQUEST_PATTERN.search(normalize_text(question)):
        return False
    return not any(item["Section"] == "Experience" for item in matches)


def comparison_dimension(section):
    return "Location" if section in LOCATION_SECTIONS else section


def requested_dimensions(question):
    """Return data dimensions explicitly named in the question."""
    q = normalize_text(question)
    q = re.sub(r"(?<!\w)(?:it|ites|it/ites)\s+industry(?!\w)", " ", q)
    return {
        dimension
        for dimension, pattern in DIMENSION_PATTERNS.items()
        if pattern.search(q)
    }


def requests_generic_category_scope(question):
    q = normalize_text(question)
    return any(
        re.search(pattern, q)
        for pattern in [
            r"(?<!\w)how many\s+categor(?:y|ies)(?!\w)",
            r"(?<!\w)(?:each|every|all)\s+categor(?:y|ies)(?!\w)",
            r"(?<!\w)(?:by|across|per)\s+categor(?:y|ies)(?!\w)",
            r"(?<!\w)(?:category|categories)\s+(?:breakdown|distribution|split)(?!\w)",
            r"(?<!\w)(?:breakdown|distribution|split)(?:\s+by)?\s+"
            r"categor(?:y|ies)(?!\w)",
        ]
    )


def requests_multi_category_scope(question):
    q = normalize_text(question)
    dimension_words = (
        r"(?:locations?|cities?|roles?|gender|experience(?:\s+bands?)?|"
        r"sub(?:-|\s*)industr(?:y|ies)|industr(?:y|ies))"
    )
    patterns = [
        rf"(?<!\w)(?:each|every|all)\s+{dimension_words}(?!\w)",
        rf"(?<!\w)all\s+(?:available\s+)?profiles\s+by\s+{dimension_words}(?!\w)",
        rf"(?<!\w)list\s+(?:all\s+)?{dimension_words}(?!\w)",
        rf"(?<!\w)(?:breakdown|distribution|split)(?:\s+by)?\s+{dimension_words}(?!\w)",
    ]
    return any(re.search(pattern, q) for pattern in patterns)


def has_ambiguous_data_label(question):
    q = normalize_text(question)
    return bool(
        re.search(
            r"(?<!\w)data\s+(?:profiles?|talent|candidates?)(?!\w)",
            q,
        )
    )


def has_unresolved_work_scope(question, matches):
    q = normalize_text(question)
    has_work_language = bool(
        re.search(r"(?<!\w)(?:work|working|located|based)(?!\w)", q)
    )
    if not has_work_language:
        return False

    if re.search(r"(?<!\w)based\s+on(?!\w)", q):
        return False

    dimensions = {
        comparison_dimension(item["Section"])
        for item in matches
        if item["Section"] != "Overall"
    }
    has_india_scope = phrase_in_text("india", q) or phrase_in_text("indian", q)
    return "Location" not in dimensions and not has_india_scope and len(dimensions) <= 1


def has_unresolved_scope_language(question, matches, metric):
    if matches or metric != "Total Profiles":
        return False
    q = normalize_text(question)
    return bool(
        re.search(
            r"(?<!\w)(?:by|during|previous|past|last|between|among)(?!\w)",
            q,
        )
    )


def overall_metric_match(talent_df, metric):
    overall = talent_df[talent_df["Section"] == "Overall"]
    for _, item in overall.iterrows():
        if canonical_metric(item["Category"]) == metric:
            return item
    return None


def is_overall_request(question, metric):
    q = normalize_text(question)
    has_count_subject = any(
        phrase_in_text(term, q)
        for term in [
            "profile",
            "profiles",
            "candidate",
            "candidates",
            "talent",
            "headcount",
        ]
    )
    return has_count_subject or metric != "Total Profiles" or phrase_in_text("total", q)


def value_for_metric(item, metric):
    if item["Section"] == "Overall" and canonical_metric(item["Category"]) == metric:
        return item["Profiles"]
    value = item.get(metric)
    return None if pd.isna(value) else float(value)


def comparison_answer(question, talent_df, matches=None, metric=None):
    metric = detect_metric(question) if metric is None else metric
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


def unsupported_constraint_answer():
    return (
        "The provided dataset does not include one or more requested categories "
        "or constraints. I should not ignore an unsupported constraint or "
        "substitute a broader India-wide count, so I cannot provide that number."
    )


def unsupported_dimension_answer():
    return (
        "The dataset contains separate aggregate cuts by role, location, "
        "experience, gender, and sub-industry, but it does not provide every "
        "breakdown or intersection. Please name one available category or two "
        "categories from the same dimension; I should not substitute the overall "
        "India count."
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

    metric, metric_error = detect_metric_request(q)
    if metric_error:
        return metric_error

    matches = find_matches(q, talent_df)
    non_overall = [item for item in matches if item["Section"] != "Overall"]
    if non_overall:
        matches = non_overall

    if has_unmatched_experience(q, matches):
        return unsupported_constraint_answer()

    if has_ambiguous_data_label(q):
        return unsupported_constraint_answer()

    if requests_multi_category_scope(q) or requests_generic_category_scope(q):
        return unsupported_dimension_answer()

    dimensions_requested = requested_dimensions(q)
    matched_dimensions = {
        comparison_dimension(item["Section"])
        for item in matches
        if item["Section"] != "Overall"
    }
    if dimensions_requested and not dimensions_requested.issubset(matched_dimensions):
        return unsupported_dimension_answer()

    if has_unresolved_work_scope(q, matches):
        return unsupported_constraint_answer()

    if has_unresolved_scope_language(q, matches, metric):
        return unsupported_constraint_answer()

    if unmatched_constraint_terms(q, talent_df):
        return unsupported_constraint_answer()

    role_matches = [item for item in matches if item["Section"] == "Role"]
    if ROLE_HINT_PATTERN.search(q) and not role_matches:
        return unsupported_constraint_answer()

    comparison_requested = any(
        phrase_in_text(word, q)
        for word in [
            "bigger",
            "compare",
            "compared",
            "difference",
            "greater",
            "higher",
            "larger",
            "less",
            "more",
            "most",
            "smaller",
            "vs",
            "versus",
        ]
    )
    if comparison_requested:
        dimensions = {comparison_dimension(item["Section"]) for item in matches}
        if len(matches) == 2 and len(dimensions) != 1:
            return (
                "That comparison mixes different data dimensions. Please compare "
                "two roles, two locations, two experience bands, two gender "
                "categories, or two sub-industries so the result is meaningful."
            )
        answer = comparison_answer(q, talent_df, matches, metric=metric)
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
        overall_match = overall_metric_match(talent_df, metric)
        if overall_match is not None and is_overall_request(q, metric):
            matches = [overall_match]
        else:
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
