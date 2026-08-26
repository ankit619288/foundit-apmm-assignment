import pandas as pd
from datetime import datetime

# ================= CONFIG =================
REFERENCE_DATE = datetime(2026, 2, 20)
TOP_N_MVP = 5

OLD_FILE = r"C:\Users\i-ssurya\OneDrive - MONSTER.Com (India) Pvt Ltd\Desktop\frl\old_SEA.xlsx"
BRIDGE_FILE = r"C:\Users\i-ssurya\OneDrive - MONSTER.Com (India) Pvt Ltd\Desktop\frl\bridge_SEA.xlsx"
PURCHASE_FILE = r"C:\Users\i-ssurya\OneDrive - MONSTER.Com (India) Pvt Ltd\Desktop\frl\purchase_SEA.xlsx"

OUTPUT_FILE = r"C:\Users\v-pksethi\OneDrive - MONSTER.Com (India) Pvt Ltd\Desktop\frl\FRL_Winners_SEA.xlsx"

NEW_MONTHS = [(2026, 1), (2025, 12), (2025, 11), (2025, 10)]
EXCLUDE_ACCOUNT_TYPES = ["free_trial", "test_job"]
# =========================================


# ---------- LOAD OLD WINNERS ----------
def load_old_winners():
    df = pd.read_excel(OLD_FILE, sheet_name="old")
    return set(df.iloc[:, 1].astype(str).str.lower())


# ---------- PREPROCESS ----------
def preprocess(df, start_col, end_col):
    # Use dynamic column names provided by process_file
    df['start_date_internal'] = pd.to_datetime(df[start_col], errors='coerce')
    df['end_date_internal'] = pd.to_datetime(df[end_col], errors='coerce')

    for col in [
        'company_name', 'company_type', 'service_channel',
        'login', 'email', 'account_type'
    ]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    for col in ['PC', 'OC', 'JP']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df


# ---------- USER TYPE ----------
def classify_user(start_date):
    if pd.isna(start_date):
        return "Existing"
    if (start_date.year, start_date.month) in NEW_MONTHS:
        return "New"
    return "Existing"


# ---------- GLOBAL EXCLUSIONS ----------
def apply_global_exclusions(df):
    return df[
        ~df['login'].str.lower().str.contains('scrape|_jobs|ftp', na=False) &
        ~df['service_channel'].str.lower().str.contains('scrape', na=False) &
        ~df['company_name'].str.lower().str.contains(
            'immigration|ankit sharma proprietor|freelancer', na=False
        ) &
        ~df['account_type'].str.lower().isin(EXCLUDE_ACCOUNT_TYPES) &
        (df['end_date_internal'] >= REFERENCE_DATE) # Using the internal end date
    ]


# ---------- CATEGORY WINNERS ----------
def find_category_winners(df, metric, old_companies):
    df = apply_global_exclusions(df)
    df = df.sort_values(metric, ascending=False).head(30)

    df['User Type'] = df['start_date_internal'].apply(classify_user)
    winners = []

    for user_type in ['New', 'Existing']:
        sub = df[df['User Type'] == user_type]
        sub = sub[~sub['company_name'].str.lower().isin(old_companies)]

        if not sub.empty:
            winners.append(sub.iloc[0])

    return winners


# ---------- MVP (TOP-N) ----------
def find_mvp(df, old_companies):
    df = apply_global_exclusions(df)

    df = df[
        (df['PC'] > 0) &
        (df['OC'] > 0) &
        (df['JP'] > 0)
    ]

    df['User Type'] = df['start_date_internal'].apply(classify_user)
    df = df[~df['company_name'].str.lower().isin(old_companies)]

    df['MVP Score'] = df['PC'] + df['OC'] + df['JP']
    df = df.sort_values('MVP Score', ascending=False)

    df['MVP Rank'] = df.groupby('User Type').cumcount() + 1
    df = df[df['MVP Rank'] <= TOP_N_MVP]

    return df.to_dict('records')


# ---------- PROCESS FILE ----------
def process_file(file_path, source, old_companies, start_col, end_col):
    # Pass the specific column names to the preprocess function
    df = preprocess(pd.read_excel(file_path), start_col, end_col)
    records = []

    categories = {
        "Search Smasher": "PC",
        "Campaign Captain": "OC",
        "Posting Champion": "JP"
    }

    for cat, metric in categories.items():
        winners = find_category_winners(df.copy(), metric, old_companies)
        for w in winners:
            records.append(build_row(w, source, cat))

    # MVP
    mvps = find_mvp(df.copy(), old_companies)
    for w in mvps:
        records.append(build_row(w, source, "MVP", w["MVP Rank"], w["MVP Score"]))

    return pd.DataFrame(records)


# ---------- OUTPUT FORMAT ----------
def build_row(w, source, category, rank=None, score=None):
    return {
        "Source": source,
        "Category": category,
        "User Type": w["User Type"],
        "MVP Rank": rank,
        "MVP Score": score,
        "Company Name": w["company_name"],
        "Company Type": w["company_type"],
        "Service Channel": w["service_channel"],
        "Login": w["login"],
        "Email": w["email"],
        "PC": w["PC"],
        "OC": w["OC"],
        "JP": w["JP"],
        "Start Date": w["start_date_internal"], # Renamed for consistency in output
        "End Date": w["end_date_internal"]
    }


# ================= MAIN =================
if __name__ == "__main__":
    old_companies = load_old_winners()

    # Call process_file with Bridge-specific columns
    bridge_df = process_file(BRIDGE_FILE, "Bridge", old_companies, "rv_start_date", "rv_end_date")
    
    # Call process_file with Purchase-specific columns
    purchase_df = process_file(PURCHASE_FILE, "Purchase", old_companies, "pc_start_date", "pc_end_date")

    final_df = pd.concat([bridge_df, purchase_df], ignore_index=True)
    final_df.to_excel(OUTPUT_FILE, index=False)

    print("✅ FRL Winners generated successfully")
    print(f"📁 Output saved at: {OUTPUT_FILE}")