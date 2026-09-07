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
    "dev ops": "DevOps Engineer",
    "ai talent": "AI/ML Engineer",
    "ai ml engineer": "AI/ML Engineer",
    "ai ml": "AI/ML Engineer",
    "ai/ml engineers": "AI/ML Engineer",
    "ai/ml engineer": "AI/ML Engineer",
    "ai/ml": "AI/ML Engineer",
    "artificial intelligence": "AI/ML Engineer",
    "machine-learning engineers": "AI/ML Engineer",
    "machine-learning engineer": "AI/ML Engineer",
    "machine learning engineers": "AI/ML Engineer",
    "ml engineer": "AI/ML Engineer",
    "ml engineers": "AI/ML Engineer",
    "ml talent": "AI/ML Engineer",
    "machine learning": "AI/ML Engineer",
    "ai engineer": "AI/ML Engineer",
    "artificial intelligence engineer": "AI/ML Engineer",
    "ml": "AI/ML Engineer",
    "data science": "Data Scientist",
    "data scientists": "Data Scientist",
    "females": "Female",
    "women": "Female",
    "woman": "Female",
    "males": "Male",
    "men": "Male",
    "cyber security": "Cybersecurity Analyst/Engineer",
    "cyber security analyst": "Cybersecurity Analyst/Engineer",
    "cyber security engineer": "Cybersecurity Analyst/Engineer",
    "cybersecurity": "Cybersecurity Analyst/Engineer",
    "cybersecurity analyst": "Cybersecurity Analyst/Engineer",
    "cybersecurity engineer": "Cybersecurity Analyst/Engineer",
    "cloud architects": "Cloud Architect/Engineer",
    "cloud architect": "Cloud Architect/Engineer",
    "cloud engineers": "Cloud Architect/Engineer",
    "cloud engineer": "Cloud Architect/Engineer",
    "cloud architect engineer": "Cloud Architect/Engineer",
    "b'lore": "Bengaluru",
    "blr": "Bengaluru",
    "bangalore": "Bengaluru",
    "banglore": "Bengaluru",
    "bombay": "Mumbai",
    "calcutta": "Kolkata",
    "cochin": "Kochi",
    "chandigarh": "Chandigrah",
    "delhi": "Delhi NCR",
    "ncr": "Delhi NCR",
    "baroda": "Vadodara",
    "bhubaneshwar": "Bhubaneswar",
    "hyd": "Hyderabad",
    "nasik": "Nashik",
    "vizag": "Visakhapatnam",
    "3-5y": "3-5 Years",
    "3-5 yrs": "3-5 Years",
    "3 to 5": "3-5 Years",
    "3 to 5 yrs": "3-5 Years",
    "1-3y": "1-3 Years",
    "1-3 yrs": "1-3 Years",
    "1 to 3": "1-3 Years",
    "1 to 3 yrs": "1-3 Years",
    "0-1y": "0-1 years",
    "0-1 year": "0-1 years",
    "0-1 yrs": "0-1 years",
    "0 to 1": "0-1 years",
    "0 to 1 yrs": "0-1 years",
    "0 to 1 years": "0-1 years",
    "5-10y": "5-10Years",
    "5-10 yrs": "5-10Years",
    "5-10 years": "5-10Years",
    "5 to 10 yrs": "5-10Years",
    "5 to 10 years": "5-10Years",
    "10-15y": "10-15 Years",
    "10-15 yrs": "10-15 Years",
    "10 to 15": "10-15 Years",
    "10 to 15 yrs": "10-15 Years",
    "10 to 15 years": "10-15 Years",
    "15y+": "15 Years+",
    "15 yrs+": "15 Years+",
    "15+ yrs": "15 Years+",
    "15+ years": "15 Years+",
    "15 plus years": "15 Years+",
    "15 yrs and above": "15 Years+",
    "15 years and above": "15 Years+",
    "15 years or more": "15 Years+",
    "information tech": "Information Technology",
    "info services": "Information Services",
}

LOCATION_SECTIONS = {"Location", "Tier II City", "Tier III City"}
LOCATION_TIER_PATTERNS = {
    "Tier II City": re.compile(
        r"(?<!\w)tier\s*(?:2|ii|two)(?:\s+cities|\s+city)?(?!\w)"
    ),
    "Tier III City": re.compile(
        r"(?<!\w)tier\s*(?:3|iii|three)(?:\s+cities|\s+city)?(?!\w)"
    ),
}

QUERY_FILLER_TOKENS = {
    "a",
    "about",
    "active",
    "aggregate",
    "aggregated",
    "all",
    "among",
    "an",
    "and",
    "approximately",
    "across",
    "are",
    "around",
    "architect",
    "architects",
    "at",
    "availability",
    "available",
    "average",
    "avg",
    "based",
    "band",
    "bands",
    "be",
    "between",
    "bigger",
    "bottom",
    "by",
    "can",
    "calculate",
    "calculated",
    "candidate",
    "candidates",
    "categories",
    "category",
    "categorize",
    "categorized",
    "city",
    "cities",
    "classification",
    "classify",
    "compare",
    "compared",
    "comparison",
    "combined",
    "common",
    "count",
    "counts",
    "coverage",
    "covered",
    "could",
    "create",
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
    "genders",
    "generate",
    "give",
    "greater",
    "gap",
    "group",
    "grouped",
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
    "industries",
    "is",
    "it",
    "it/ites",
    "ites",
    "large",
    "larger",
    "last",
    "less",
    "list",
    "listed",
    "located",
    "location",
    "locations",
    "lower",
    "m",
    "male",
    "many",
    "max",
    "maximum",
    "mean",
    "month",
    "months",
    "more",
    "most",
    "much",
    "min",
    "minimum",
    "number",
    "numbers",
    "of",
    "on",
    "or",
    "overall",
    "over",
    "past",
    "per",
    "percent",
    "percentage",
    "please",
    "pool",
    "position",
    "prepare",
    "previous",
    "profile",
    "profiles",
    "proportion",
    "provide",
    "provided",
    "registered",
    "reg",
    "respectively",
    "ratio",
    "rank",
    "ranked",
    "ranking",
    "range",
    "role",
    "roles",
    "scientist",
    "scientists",
    "segment",
    "segmentation",
    "segmented",
    "show",
    "should",
    "share",
    "six",
    "size",
    "smaller",
    "sourced",
    "sub",
    "summarize",
    "summary",
    "supply",
    "sum",
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
    "top",
    "twelve",
    "using",
    "versus",
    "view",
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
    "arithmetic",
    "stand",
    "spread",
    "where",
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

RANKING_COUNT_PATTERN = (
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
)

DIMENSION_SECTIONS = {
    "Location": LOCATION_SECTIONS,
    "Role": {"Role"},
    "Gender": {"Gender"},
    "Experience": {"Experience"},
    "Sub Industry": {"Sub Industry"},
}

DIMENSION_LABELS = {
    "Location": "locations",
    "Role": "roles",
    "Gender": "gender categories",
    "Experience": "experience bands",
    "Sub Industry": "sub-industries",
}

DIMENSION_SINGULAR_LABELS = {
    "Location": "location",
    "Role": "role",
    "Gender": "gender category",
    "Experience": "experience band",
    "Sub Industry": "sub-industry",
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

UNSUPPORTED_BUSINESS_INFERENCE_KEYWORDS = [
    "addressable market",
    "best city",
    "best location",
    "best market",
    "best role",
    "conversion",
    "demand",
    "forecast",
    "future",
    "growth",
    "hiring difficulty",
    "job openings",
    "market opportunity",
    "penetration",
    "potential",
    "prioritize",
    "projection",
    "recommend",
    "revenue",
    "target market",
    "time to hire",
    "trend",
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


def requested_location_sections(question):
    q = normalize_text(question)
    return [
        section
        for section, pattern in LOCATION_TIER_PATTERNS.items()
        if pattern.search(q)
    ]


def requested_location_section(question):
    matches = requested_location_sections(question)
    return matches[0] if len(matches) == 1 else None


def rows_for_dimension(talent_df, dimension, question=""):
    sections = DIMENSION_SECTIONS[dimension]
    if dimension == "Location":
        requested_section = requested_location_section(question)
        if requested_section:
            sections = {requested_section}
    return talent_df[talent_df["Section"].isin(sections)].copy()


def dimension_scope_label(dimension, question="", singular=False):
    requested_section = requested_location_section(question)
    if dimension == "Location" and requested_section:
        if requested_section == "Tier II City":
            return "Tier II city" if singular else "Tier II cities"
        return "Tier III city" if singular else "Tier III cities"
    return (
        DIMENSION_SINGULAR_LABELS[dimension]
        if singular
        else DIMENSION_LABELS[dimension]
    )


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


def format_exact_count(value):
    value = float(value)
    if value.is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


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
    for pattern in LOCATION_TIER_PATTERNS.values():
        residue = pattern.sub(" ", residue)
    residue = re.sub(
        r"(?<!\w)(?:(?:for|as)\s+(?:(?:a|an|the|my|our)\s+)?)?"
        r"(?:sales|marketing|customer\s+success|client|business|recruiter|"
        r"commercial|account|prospect|stakeholder|gtm|"
        r"go(?:-|\s+)to(?:-|\s+)market)"
        r"(?:\s+team)?\s+(?:brief|call|conversation|deck|discussion|insights?|"
        r"meeting|overview|pitch(?:\s+deck)?|planning|presentation|proposal|"
        r"report|reporting|review|use|view)(?!\w)",
        " ",
        residue,
    )
    residue = re.sub(
        r"(?<!\w)(?:sales|marketing|client|customer\s+success|business|"
        r"recruiter|commercial|prospect|stakeholder)"
        r"(?:-|\s+)ready(?!\w)",
        " ",
        residue,
    )
    residue = re.sub(
        r"(?<!\w)(?:market\s+size|talent\s+(?:landscape|market|snapshot))(?!\w)",
        " ",
        residue,
    )
    residue = re.sub(
        r"(?<!\w)(?:roles?|locations?|cities?|gender|experience(?:\s+bands?)?|"
        r"sub(?:-|\s*)industr(?:y|ies)|industr(?:y|ies))\s+"
        r"(?:classification|landscape|mix|overview|ranking|segmentation|snapshot)"
        r"(?!\w)",
        " ",
        residue,
    )
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


def detect_ranking_request(question):
    """Return a grounded top/bottom-N request when one is explicitly present."""
    q = normalize_text(question)
    match = re.search(
        rf"(?<!\w)(top|bottom)\s+({RANKING_COUNT_PATTERN})(?!\w)",
        q,
    )
    if match:
        raw_count = match.group(2)
        count = int(raw_count) if raw_count.isdigit() else MONTH_WORDS[raw_count]
        if count < 1:
            return None

        return {
            "direction": match.group(1),
            "count": count,
            "matched_text": match.group(0),
            "extreme": False,
        }

    counted_extreme = re.search(
        rf"(?<!\w)({RANKING_COUNT_PATTERN})\s+"
        r"(highest|largest|most|strongest|lowest|smallest|least|fewest|weakest)"
        r"(?!\w)",
        q,
    ) or re.search(
        r"(?<!\w)(highest|largest|most|strongest|lowest|smallest|least|fewest|"
        rf"weakest)\s+({RANKING_COUNT_PATTERN})(?!\w)",
        q,
    )
    if counted_extreme:
        first, second = counted_extreme.group(1), counted_extreme.group(2)
        if first in MONTH_WORDS or first.isdigit():
            raw_count, direction_word = first, second
        else:
            direction_word, raw_count = first, second
        count = int(raw_count) if raw_count.isdigit() else MONTH_WORDS[raw_count]
        return {
            "direction": (
                "bottom"
                if direction_word
                in {"lowest", "smallest", "least", "fewest", "weakest"}
                else "top"
            ),
            "count": count,
            "matched_text": counted_extreme.group(0),
            "extreme": False,
        }

    if phrase_in_text("at least", q):
        return None

    extreme = re.search(
        r"(?<!\w)(highest|largest|maximum|max|most|strongest|lowest|"
        r"smallest|minimum|min|least|fewest|weakest)(?!\w)",
        q,
    )
    if not extreme:
        return None

    return {
        "direction": (
            "bottom"
            if extreme.group(1)
            in {"lowest", "smallest", "minimum", "min", "least", "fewest", "weakest"}
            else "top"
        ),
        "count": 1,
        "matched_text": extreme.group(0),
        "extreme": True,
    }


def requests_dimension_breakdown(question):
    q = normalize_text(question)
    dimension_words = (
        r"(?:locations?|cities?|roles?|gender|experience(?:\s+bands?)?|"
        r"sub(?:-|\s*)industr(?:y|ies)|industr(?:y|ies))"
    )
    tier_city_words = r"(?:tier\s*(?:2|ii|two|3|iii|three)\s+cities)"
    patterns = [
        rf"(?<!\w)(?:profiles?|talent|candidates?)\s+by\s+{dimension_words}(?!\w)",
        rf"(?<!\w)(?:show|list|give|provide)(?:\s+me)?\s+(?:all\s+)?"
        rf"{dimension_words}(?!\w)",
        rf"(?<!\w)(?:generate|create|show|give|provide)(?:\s+me)?\s+"
        rf"(?:an?\s+)?aggregate(?:d)?(?:\s+(?:data|summary|view))?\s+"
        rf"(?:of|for|by)\s+(?:all\s+)?{dimension_words}(?!\w)",
        rf"(?<!\w)aggregate(?:d)?(?:\s+(?:data|summary|view))?\s+"
        rf"(?:of|for|by)\s+(?:all\s+)?{dimension_words}(?!\w)",
        rf"(?<!\w)aggregate(?:d)?\s+(?:profiles?|talent|candidates?|data)\s+"
        rf"by\s+{dimension_words}(?!\w)",
        rf"(?<!\w)(?:classification|segmentation)(?:\s+of\s+(?:profiles?|talent))?"
        rf"(?:\s+by)?\s+{dimension_words}(?!\w)",
        rf"(?<!\w)(?:categorize|classify|group|segment)(?:\s+(?:profiles?|talent))?"
        rf"\s+by\s+{dimension_words}(?!\w)",
        rf"(?<!\w)(?:availability|coverage|landscape|mix|overview|snapshot)"
        rf"(?:\s+of\s+(?:profiles?|talent))?\s+by\s+{dimension_words}(?!\w)",
        rf"(?<!\w)(?:profiles?|talent)(?:\s+pool)?(?:\s+size)?\s+by\s+"
        rf"{dimension_words}(?!\w)",
        rf"(?<!\w)(?:rank|ranking)(?:\s+(?:all|the))?\s+{dimension_words}(?!\w)",
        rf"(?<!\w){dimension_words}\s+(?:classification|landscape|mix|overview|"
        rf"ranking|segmentation|snapshot)(?!\w)",
        rf"(?<!\w)(?:show|list|give|provide)(?:\s+me)?\s+(?:all\s+)?"
        rf"{tier_city_words}(?!\w)",
        rf"(?<!\w)(?:profiles?|talent|counts?)\s+(?:by|for|in)\s+"
        rf"{tier_city_words}(?!\w)",
    ]
    return any(re.search(pattern, q) for pattern in patterns)


def requests_dimension_count(question):
    q = normalize_text(question)
    if re.search(r"(?<!\w)(?:profiles?|talent|candidates?|headcount)(?!\w)", q):
        return False
    dimension_count_subject = (
        r"(?:roles?|locations?|cities?|gender\s+categories|genders?|"
        r"experience\s+bands?|sub(?:-|\s*)industr(?:y|ies)|"
        r"industr(?:y|ies)|categories|"
        r"tier\s*(?:2|ii|two|3|iii|three)\s+cities)"
    )
    return bool(
        re.search(
            rf"(?<!\w)(?:how many|number of|count of|count)\s+"
            rf"(?:available\s+)?{dimension_count_subject}(?!\w)",
            q,
        )
        or re.search(
            rf"(?<!\w){dimension_count_subject}\s+"
            r"(?:are\s+)?(?:available|covered|included|listed)(?!\w)",
            q,
        )
    )


def collection_constraint_terms(question, talent_df, ranking_request=None):
    """Validate extra terms after removing supported collection syntax."""
    q = normalize_text(question)
    if ranking_request:
        q = q.replace(ranking_request["matched_text"], " ")
    q = re.sub(
        r"(?<!\w)(?:aggregate|aggregated|breakdown|create|distribution|generate|"
        r"fewest|highest|including|largest|least|list|lowest|max|maximum|minimum|"
        r"min|most|ranked|ranking|smallest|split|strongest|summarize|summary|"
        r"view|weakest)(?!\w)",
        " ",
        q,
    )
    return unmatched_constraint_terms(q, talent_df)


def dimension_summary_answer(question, talent_df, matches, metric):
    """Answer exact single-dimension rankings and breakdowns from source rows."""
    ranking_request = detect_ranking_request(question)
    category_count_requested = requests_dimension_count(question)
    breakdown_requested = (
        requests_multi_category_scope(question)
        or requests_dimension_breakdown(question)
    )
    if not ranking_request and not breakdown_requested and not category_count_requested:
        return None

    dimensions = requested_dimensions(question)
    if len(dimensions) != 1:
        return unsupported_dimension_answer()

    dimension = next(iter(dimensions))
    scope_label = dimension_scope_label(dimension, question)
    scope_singular = dimension_scope_label(dimension, question, singular=True)
    dimension_heading = requested_location_section(question) or dimension
    matched_dimensions = {
        comparison_dimension(item["Section"])
        for item in matches
        if item["Section"] != "Overall"
    }
    if matched_dimensions and not matched_dimensions.issubset({dimension}):
        return unsupported_dimension_answer()

    if collection_constraint_terms(question, talent_df, ranking_request):
        return unsupported_constraint_answer()

    rows = rows_for_dimension(talent_df, dimension, question)
    rows = rows[rows[metric].notna()]
    if rows.empty:
        return unavailable_answer()

    if category_count_requested:
        categories = rows["Category"].astype(str).tolist()
        return (
            f"The provided dataset contains {len(categories)} "
            f"{scope_label}: "
            + ", ".join(categories)
            + "."
        )

    ascending = bool(
        ranking_request and ranking_request["direction"] == "bottom"
    )
    rows = rows.sort_values(
        [metric, "Category Lower"],
        ascending=[ascending, True],
        kind="mergesort",
    )

    available_count = len(rows)
    metric_label = (
        "total profiles" if metric == "Total Profiles" else metric_answer_label(metric)
    )
    if ranking_request:
        requested_count = ranking_request["count"]
        shown_count = min(requested_count, available_count)
        rows = rows.head(shown_count)
        if ranking_request["extreme"]:
            direction_label = (
                "Highest" if ranking_request["direction"] == "top" else "Lowest"
            )
            heading = (
                f"{direction_label} {scope_singular} "
                f"by {metric_label} in India"
            )
        else:
            dimension_label = (
                scope_singular
                if shown_count == 1
                else scope_label
            )
            heading = (
                f"{ranking_request['direction'].title()} {shown_count} "
                f"{dimension_label} by {metric_label} in India"
            )
        if requested_count > available_count:
            heading += (
                f" (the dataset contains {available_count} "
                f"{scope_label})"
            )
    elif re.search(r"(?<!\w)(?:rank|ranking)(?!\w)", normalize_text(question)):
        heading = (
            f"{dimension_heading} ranking by {metric_label} in India "
            f"({available_count} categories)"
        )
    else:
        heading = (
            f"{dimension_heading} breakdown by {metric_label} in India "
            f"({available_count} categories)"
        )

    entries = [
        f"{index}. {row['Category']}: {format_count(row[metric])}"
        for index, (_, row) in enumerate(rows.iterrows(), start=1)
    ]
    return heading + ":\n" + "\n".join(entries)


def ordinal(value):
    if 10 <= value % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
    return f"{value}{suffix}"


def extrema_pair_answer(question, talent_df, matches, metric):
    q = normalize_text(question)
    high_pattern = (
        r"(?<!\w)(?:highest|largest|maximum|max|most|strongest)(?!\w)"
    )
    low_pattern = (
        r"(?<!\w)(?:lowest|smallest|minimum|min|least|fewest|weakest)(?!\w)"
    )
    has_high = bool(re.search(high_pattern, q))
    has_low = bool(re.search(low_pattern, q))
    has_range = bool(
        re.search(r"(?<!\w)(?:range|spread)(?!\w)", q)
        and re.search(
            r"(?<!\w)(?:profiles?|talent|count|counts|supply|active|sourced|"
            r"registered)(?!\w)",
            q,
        )
    )
    if not ((has_high and has_low) or has_range):
        return None
    if detect_statistic_request(q):
        return "Please request one calculation at a time so the result is unambiguous."

    validation_question = re.sub(high_pattern, " ", q)
    validation_question = re.sub(low_pattern, " ", validation_question)
    if unmatched_constraint_terms(validation_question, talent_df):
        return unsupported_constraint_answer()

    explicit_dimensions = requested_dimensions(q)
    matched_dimensions = {
        comparison_dimension(item["Section"])
        for item in matches
        if item["Section"] != "Overall"
    }
    dimensions = explicit_dimensions.union(matched_dimensions)
    if len(dimensions) != 1:
        return unsupported_dimension_answer()
    dimension = next(iter(dimensions))
    if explicit_dimensions and matched_dimensions and not matched_dimensions.issubset(
        explicit_dimensions
    ):
        return unsupported_dimension_answer()

    if matches:
        if len(matches) < 2:
            return (
                "Please remove the single category constraint to use the complete "
                "dimension, or name at least two same-dimension categories."
            )
        rows = pd.DataFrame(sorted(matches, key=lambda item: match_position(q, item)))
    else:
        rows = rows_for_dimension(talent_df, dimension, q)
    rows = rows[rows[metric].notna()]
    if rows.empty:
        return unavailable_answer()

    highest = rows.sort_values(
        [metric, "Category Lower"],
        ascending=[False, True],
        kind="mergesort",
    ).iloc[0]
    lowest = rows.sort_values(
        [metric, "Category Lower"],
        ascending=[True, True],
        kind="mergesort",
    ).iloc[0]
    highest_value = float(highest[metric])
    lowest_value = float(lowest[metric])
    gap = highest_value - lowest_value
    return (
        f"Highest {dimension_scope_label(dimension, q, singular=True)} by "
        f"{metric_answer_label(metric)}: {highest['Category']} at "
        f"{format_calculated_count(highest_value)}. Lowest: {lowest['Category']} "
        f"at {format_calculated_count(lowest_value)}. The range is "
        f"{format_calculated_count(gap)}."
    )


def category_rank_answer(question, talent_df, matches, metric):
    q = normalize_text(question)
    rank_requested = bool(
        re.search(r"(?<!\w)(?:rank|ranking|position)(?!\w)", q)
        or re.search(r"(?<!\w)where\s+does\b.+\bstand(?!\w)", q)
    )
    if not rank_requested or detect_ranking_request(q):
        return None
    if len(matches) != 1:
        return None
    if unmatched_constraint_terms(q, talent_df):
        return unsupported_constraint_answer()

    item = matches[0]
    dimension = comparison_dimension(item["Section"])
    explicit_dimensions = requested_dimensions(q)
    if explicit_dimensions and explicit_dimensions != {dimension}:
        return unsupported_dimension_answer()

    rows = rows_for_dimension(talent_df, dimension, q)
    rows = rows[rows[metric].notna()]
    value = value_for_metric(item, metric)
    if rows.empty or value is None:
        return unavailable_answer()

    rank = int((rows[metric].astype(float) > value).sum()) + 1
    tied_count = int((rows[metric].astype(float) == value).sum())
    tie_text = " (tied)" if tied_count > 1 else ""
    return (
        f"{item['Category']} ranks {ordinal(rank)}{tie_text} out of {len(rows)} "
        f"{dimension_scope_label(dimension, q)} by "
        f"{metric_answer_label(metric)} in India, "
        f"with {format_count(value)}."
    )


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


def match_position(question, item):
    q = normalize_text(question)
    category = normalize_text(item["Category"])
    phrases = [category]
    phrases.extend(
        alias
        for alias, target in CATEGORY_ALIASES.items()
        if normalize_text(target) == category
    )
    positions = []
    for phrase in phrases:
        match = re.search(
            rf"(?<!\w){re.escape(normalize_text(phrase))}(?!\w)",
            q,
        )
        if match:
            positions.append(match.start())
    return min(positions) if positions else len(q)


def ratio_answer(question, talent_df, matches, metric):
    q = normalize_text(question)
    if not phrase_in_text("ratio", q):
        return None
    if detect_statistic_request(q) or re.search(
        r"(?<!\w)(?:percentage|percent|proportion|share)(?!\w)",
        q,
    ):
        return "Please request one calculation at a time so the result is unambiguous."
    if unmatched_constraint_terms(q, talent_df):
        return unsupported_constraint_answer()
    if not matches:
        dimensions = requested_dimensions(q)
        if len(dimensions) == 1:
            dimension = next(iter(dimensions))
            rows = rows_for_dimension(talent_df, dimension, q)
            if len(rows) == 2:
                matches = [row for _, row in rows.iterrows()]
    if len(matches) != 2:
        return (
            "Please name exactly two available categories from the same dimension "
            "for a ratio."
        )

    dimensions = {comparison_dimension(item["Section"]) for item in matches}
    if len(dimensions) != 1:
        return (
            "That ratio mixes different data dimensions. Please name two roles, "
            "two locations, two experience bands, two gender categories, or two "
            "sub-industries."
        )

    first, second = sorted(matches, key=lambda item: match_position(q, item))
    first_value = value_for_metric(first, metric)
    second_value = value_for_metric(second, metric)
    if first_value is None or second_value is None or second_value == 0:
        return unavailable_answer()

    ratio = first_value / second_value
    return (
        f"The {first['Category']}-to-{second['Category']} ratio for "
        f"{metric_answer_label(metric)} is {ratio:.2f}:1. "
        f"{first['Category']} has {format_count(first_value)}, while "
        f"{second['Category']} has {format_count(second_value)}."
    )


def share_answer(question, talent_df, matches, metric):
    q = normalize_text(question)
    if not re.search(r"(?<!\w)(?:percentage|percent|proportion|share)(?!\w)", q):
        return None
    if phrase_in_text("ratio", q) or detect_statistic_request(q):
        return "Please request one calculation at a time so the result is unambiguous."
    if unmatched_constraint_terms(q, talent_df):
        return unsupported_constraint_answer()
    if not matches:
        dimensions = requested_dimensions(q)
        if len(dimensions) == 1:
            dimension = next(iter(dimensions))
            rows = rows_for_dimension(talent_df, dimension, q)
            rows = rows[rows[metric].notna()]
            overall = overall_metric_match(talent_df, metric)
            denominator = None if overall is None else value_for_metric(overall, metric)
            if rows.empty or denominator in {None, 0}:
                return unavailable_answer()

            rows = rows.sort_values(
                [metric, "Category Lower"],
                ascending=[False, True],
                kind="mergesort",
            )
            entries = [
                (
                    f"{index}. {row['Category']}: "
                    f"{float(row[metric]) / denominator * 100:.1f}% "
                    f"({format_count(row[metric])} of {format_count(denominator)})"
                )
                for index, (_, row) in enumerate(rows.iterrows(), start=1)
            ]
            return (
                f"{requested_location_section(q) or dimension} shares of overall India "
                f"{metric_answer_label(metric)}:\n"
                + "\n".join(entries)
                + "\nEach percentage uses the matching overall India metric as "
                "the denominator; the source does not state that every category "
                "set is exhaustive or mutually exclusive."
            )
    if len(matches) != 1:
        dimensions = {comparison_dimension(item["Section"]) for item in matches}
        if len(matches) == 2 and len(dimensions) != 1:
            return (
                "That percentage mixes different data dimensions. Please use one "
                "category against the overall India metric, or two categories from "
                "the same dimension."
            )
        return (
            "Please name one available category for a percentage of the matching "
            "overall India metric."
        )

    item = matches[0]
    numerator = value_for_metric(item, metric)
    overall = overall_metric_match(talent_df, metric)
    denominator = None if overall is None else value_for_metric(overall, metric)
    if numerator is None or denominator in {None, 0}:
        return unavailable_answer()

    percentage = numerator / denominator * 100
    return (
        f"{item['Category']} represents {percentage:.1f}% of the overall India "
        f"{metric_answer_label(metric)} in the provided dataset "
        f"({format_count(numerator)} of {format_count(denominator)})."
    )


def detect_statistic_request(question):
    q = normalize_text(question)
    requested = []
    if re.search(r"(?<!\w)(?:average|avg|mean)(?!\w)", q):
        requested.append("average")
    if re.search(
        r"(?<!\w)(?:sum|arithmetic\s+total|combined\s+total|total\s+combined)(?!\w)",
        q,
    ):
        requested.append("sum")

    if len(requested) > 1:
        return "ambiguous"
    return requested[0] if requested else None


def format_calculated_count(value):
    friendly = format_count(value)
    exact = format_exact_count(value)
    if friendly == exact:
        return exact
    return f"{friendly} ({exact} exact)"


def dimension_statistic_answer(question, talent_df, matches, metric):
    """Calculate transparent arithmetic over rows from one source dimension."""
    statistic = detect_statistic_request(question)
    if statistic is None:
        return None
    if statistic == "ambiguous":
        return (
            "Please request either an arithmetic sum or an average, one at a time, "
            "so the calculation is unambiguous."
        )

    q = normalize_text(question)
    if phrase_in_text("ratio", q) or re.search(
        r"(?<!\w)(?:percentage|percent|proportion|share)(?!\w)",
        q,
    ):
        return "Please request one calculation at a time so the result is unambiguous."
    ranking_request = detect_ranking_request(q)
    if re.search(r"(?<!\w)(?:top|bottom)(?!\w)", q) and not ranking_request:
        return "Please specify how many top or bottom categories to include."

    validation_question = q
    if ranking_request:
        validation_question = validation_question.replace(
            ranking_request["matched_text"],
            " ",
        )
    if unmatched_constraint_terms(validation_question, talent_df):
        return unsupported_constraint_answer()

    explicit_dimensions = requested_dimensions(q)
    matched_dimensions = {
        comparison_dimension(item["Section"])
        for item in matches
        if item["Section"] != "Overall"
    }
    all_dimensions = explicit_dimensions.union(matched_dimensions)
    if len(all_dimensions) > 1:
        return (
            "That calculation mixes different data dimensions. Please calculate "
            "within roles, locations, experience bands, gender categories, or "
            "sub-industries, one dimension at a time."
        )

    if not all_dimensions:
        if statistic == "sum" and is_overall_request(q, metric):
            overall = overall_metric_match(talent_df, metric)
            if overall is None:
                return unavailable_answer()
            value = value_for_metric(overall, metric)
            return (
                f"The source-provided overall India {metric_answer_label(metric)} "
                f"count is {format_calculated_count(value)}. I used the workbook's "
                "overall row and did not add separate category cuts."
            )
        return (
            "Please specify one source dimension for this calculation: role, "
            "location, experience, gender, or sub-industry."
        )

    dimension = next(iter(all_dimensions))
    if matched_dimensions and explicit_dimensions and not matched_dimensions.issubset(
        explicit_dimensions
    ):
        return unsupported_dimension_answer()

    dimension_words = (
        r"(?:locations?|cities?|roles?|gender|experience(?:\s+bands?)?|"
        r"sub(?:-|\s*)industr(?:y|ies)|industr(?:y|ies))"
    )
    explicit_full_scope = bool(
        re.search(
            rf"(?<!\w)(?:all|each|every)\s+(?:the\s+)?{dimension_words}(?!\w)",
            q,
        )
    ) or bool(
        phrase_in_text("including", q)
        and re.search(
            rf"(?<!\w)(?:across|by|per)\s+(?:the\s+)?{dimension_words}(?!\w)",
            q,
        )
    )
    dimension_wide = not matches or explicit_full_scope

    if dimension_wide:
        rows = rows_for_dimension(talent_df, dimension, q)
    else:
        ordered_matches = sorted(matches, key=lambda item: match_position(q, item))
        if len(ordered_matches) < 2:
            return (
                "Please name at least two categories from the same dimension, or "
                "request the calculation across one complete source dimension."
            )
        rows = pd.DataFrame(ordered_matches)

    rows = rows[rows[metric].notna()].copy()
    if rows.empty:
        return unavailable_answer()

    if ranking_request:
        rows = rows.sort_values(
            [metric, "Category Lower"],
            ascending=[ranking_request["direction"] == "bottom", True],
            kind="mergesort",
        ).head(ranking_request["count"])

    values = rows[metric].astype(float)
    category_count = len(rows)
    category_names = rows["Category"].astype(str).tolist()
    if category_count == 0:
        return unavailable_answer()

    subset_label = (
        ", ".join(category_names)
        if category_count <= 5
        else f"all {category_count} listed {dimension_scope_label(dimension, q)}"
    )
    metric_label = metric_answer_label(metric)

    if statistic == "average":
        value = values.mean()
        return (
            f"The arithmetic mean of {metric_label} across {subset_label} "
            f"is {format_calculated_count(value)} across {category_count} source "
            "rows. This is a mean of category-level aggregate counts, not an "
            "average per candidate."
        )

    value = values.sum()
    return (
        f"The arithmetic sum of {metric_label} across {subset_label} is "
        f"{format_calculated_count(value)}. Because the workbook provides separate "
        "aggregate cuts and does not define category overlap, this must not be "
        "presented as a deduplicated unique-profile total."
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

    if len(requested_location_sections(q)) > 1:
        return (
            "Please request Tier II or Tier III cities one at a time. The workbook "
            "does not provide a combined tier total, so I should not merge them."
        )

    if any(
        phrase_in_text(keyword, q)
        for keyword in UNSUPPORTED_BUSINESS_INFERENCE_KEYWORDS
    ):
        return (
            "The provided workbook contains talent-supply counts, not demand, "
            "growth, forecasts, revenue, conversion, job openings, or market "
            "recommendation data. I can compare and rank the supplied counts, but "
            "I should not infer a business outcome from them."
        )

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
    elif requested_dimensions(q):
        # Metric labels such as "total profiles" also exist as overall rows. They
        # are not category constraints when the question explicitly names a
        # non-overall dimension such as role or location.
        matches = []

    if has_unmatched_experience(q, matches):
        return unsupported_constraint_answer()

    if has_ambiguous_data_label(q):
        return unsupported_constraint_answer()

    calculated_answer = extrema_pair_answer(q, talent_df, matches, metric)
    if calculated_answer:
        return calculated_answer

    calculated_answer = ratio_answer(q, talent_df, matches, metric)
    if calculated_answer:
        return calculated_answer

    calculated_answer = share_answer(q, talent_df, matches, metric)
    if calculated_answer:
        return calculated_answer

    calculated_answer = dimension_statistic_answer(q, talent_df, matches, metric)
    if calculated_answer:
        return calculated_answer

    calculated_answer = category_rank_answer(q, talent_df, matches, metric)
    if calculated_answer:
        return calculated_answer

    summary_answer = dimension_summary_answer(q, talent_df, matches, metric)
    if summary_answer:
        return summary_answer

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
            "gap",
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
