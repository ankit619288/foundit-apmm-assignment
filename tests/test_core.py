import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

from src.calculate_frl_winners import (
    OUTPUT_COLUMNS,
    REFERENCE_DATE,
    apply_eligibility_rules,
    classify_user,
    get_category_winners,
    load_purchase_data,
)
from src.talent_agent import agent_answer, comparison_answer, load_talent_data


BASE_DIR = Path(__file__).resolve().parents[1]


class TalentAgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.talent_df = load_talent_data()

    def test_required_ai_ml_question(self):
        answer = agent_answer(
            "How many AI/ML Engineer profiles are available in India?",
            self.talent_df,
        )
        self.assertIn("995K profiles", answer)

    def test_required_comparison_question(self):
        answer = agent_answer(
            "Which is larger - Data Scientist or DevOps talent, and by how much?",
            self.talent_df,
        )
        self.assertIn("21,101 profiles", answer)
        self.assertIn("DevOps Engineer", answer)

    def test_salary_question_is_declined(self):
        answer = agent_answer(
            "What salary should I offer a DevOps engineer in Pune?",
            self.talent_df,
        )
        self.assertIn("does not include salary", answer)

    def test_metric_specific_question_uses_12m_value(self):
        answer = agent_answer(
            "How many 12M active AI/ML profiles are available?",
            self.talent_df,
        )
        self.assertIn("605K 12M active profiles", answer)

    def test_metric_parser_accepts_plural_months(self):
        answer = agent_answer(
            "How many AI/ML profiles were active in the last 12 months?",
            self.talent_df,
        )
        self.assertIn("605K 12M active profiles", answer)

    def test_common_gender_alias_is_supported(self):
        answer = agent_answer(
            "How many women profiles are available?",
            self.talent_df,
        )
        self.assertIn("Female has 1.90 Mn profiles", answer)

    def test_common_city_spelling_is_supported(self):
        answer = agent_answer(
            "How many profiles are available in Chandigarh?",
            self.talent_df,
        )
        self.assertIn("Chandigrah has 95,360 profiles", answer)

    def test_unknown_role_does_not_fall_back_to_city(self):
        answer = agent_answer(
            "How many Java developers are available in Kochi?",
            self.talent_df,
        )
        self.assertIn("could not find that answer", answer)
        self.assertNotIn("Kochi has", answer)

    def test_cross_tab_question_is_not_invented(self):
        answer = agent_answer(
            "How many DevOps engineers are available in Pune?",
            self.talent_df,
        )
        self.assertIn("not a cross-tabbed intersection", answer)

    def test_equal_comparison_is_reported_as_equal(self):
        talent_df = pd.DataFrame(
            [
                {
                    "Category": "Role A",
                    "Category Lower": "role a",
                    "Section": "Role",
                    "Profiles": 10.0,
                    "Total Profiles": 10.0,
                },
                {
                    "Category": "Role B",
                    "Category Lower": "role b",
                    "Section": "Role",
                    "Profiles": 10.0,
                    "Total Profiles": 10.0,
                },
            ]
        )
        answer = comparison_answer("Compare Role A vs Role B", talent_df)
        self.assertIn("same total profiles", answer)

    def test_incomplete_comparison_does_not_return_single_count(self):
        answer = agent_answer(
            "Is Pune larger than London?",
            self.talent_df,
        )
        self.assertIn("could not make that comparison", answer)
        self.assertNotIn("Pune has", answer)


class FrlRuleTests(unittest.TestCase):
    @staticmethod
    def _winner_row(index, user_type="Existing", pc=0, oc=0, jp=0):
        return {
            "User Type": user_type,
            "company_name": f"Company {index}",
            "company_type": "company",
            "service_channel": "smb",
            "login": f"login_{index}",
            "email": f"user{index}@example.com",
            "PC": pc,
            "OC": oc,
            "JP": jp,
            "start_date_internal": pd.Timestamp("2025-01-01"),
            "end_date_internal": pd.Timestamp("2027-01-01"),
        }

    def test_new_user_date_boundaries_are_inclusive(self):
        self.assertEqual(classify_user(pd.Timestamp("2025-10-01")), "New")
        self.assertEqual(classify_user(pd.Timestamp("2026-01-31")), "New")
        self.assertEqual(classify_user(pd.Timestamp("2025-09-30")), "Existing")
        self.assertEqual(classify_user(pd.NaT), "Existing")

    def test_end_date_boundary_and_missing_date(self):
        rows = []
        for login, end_date in [
            ("keep", REFERENCE_DATE),
            ("old", REFERENCE_DATE - pd.Timedelta(days=1)),
            ("missing", pd.NaT),
        ]:
            rows.append(
                {
                    "account_type": "paid",
                    "login": login,
                    "service_channel": "smb",
                    "company_name": "sample company",
                    "end_date_internal": end_date,
                    "start_date_internal": pd.Timestamp("2025-10-01"),
                }
            )
        eligible = apply_eligibility_rules(pd.DataFrame(rows))
        self.assertEqual(eligible["login"].tolist(), ["keep"])

    def test_missing_required_columns_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            incomplete_file = Path(temp_dir) / "purchase.xlsx"
            pd.DataFrame({"company_name": ["Sample"]}).to_excel(
                incomplete_file,
                index=False,
            )
            with patch(
                "src.calculate_frl_winners.PURCHASE_FILE",
                incomplete_file,
            ):
                with self.assertRaisesRegex(ValueError, "missing required columns"):
                    load_purchase_data()

    def test_all_text_exclusion_rules(self):
        base = {
            "account_type": "paid",
            "login": "valid_login",
            "service_channel": "smb",
            "company_name": "valid company",
            "end_date_internal": REFERENCE_DATE,
            "start_date_internal": pd.Timestamp("2025-10-01"),
        }
        variants = [
            ("valid", {}),
            ("free_trial", {"account_type": "free_trial"}),
            ("test_job", {"account_type": "test_job"}),
            ("scrape_login", {"login": "source_scrape"}),
            ("jobs_login", {"login": "source_jobs"}),
            ("ftp_login", {"login": "ftp_user"}),
            ("scrape_channel", {"service_channel": "scrape channel"}),
            ("immigration", {"company_name": "Immigration Services"}),
            (
                "proprietor",
                {"company_name": "Ankit Sharma Proprietor Services"},
            ),
            ("freelancer", {"company_name": "Independent Freelancer"}),
        ]
        rows = []
        for identifier, changes in variants:
            row = {**base, **changes, "identifier": identifier}
            rows.append(row)

        eligible = apply_eligibility_rules(pd.DataFrame(rows))
        self.assertEqual(eligible["identifier"].tolist(), ["valid"])

    def test_category_winner_must_be_inside_overall_top_30(self):
        rows = [
            self._winner_row(index, pc=100 - index)
            for index in range(30)
        ]
        rows.append(self._winner_row(30, user_type="New", pc=1))
        winners = get_category_winners(pd.DataFrame(rows))
        search_winners = [
            winner for winner in winners if winner["Category"] == "Search Smasher"
        ]
        self.assertEqual(len(search_winners), 1)
        self.assertEqual(search_winners[0]["User Type"], "Existing")

    def test_generated_winner_workbook_schema_and_counts(self):
        winners = pd.read_excel(BASE_DIR / "outputs" / "fRL_winners.xlsx")
        self.assertEqual(winners.columns.tolist(), OUTPUT_COLUMNS)
        self.assertEqual(len(winners), 16)
        self.assertEqual((winners["Category"] == "MVP").sum(), 10)
        self.assertEqual((winners["Category"] != "MVP").sum(), 6)

    def test_generated_winner_identities_match_verified_result(self):
        winners = pd.read_excel(BASE_DIR / "outputs" / "fRL_winners.xlsx")
        actual = set(
            zip(winners["Category"], winners["User Type"], winners["Login"])
        )
        expected = {
            ("Search Smasher", "New", "xe_maenginx01"),
            ("Search Smasher", "Existing", "xbestinx34"),
            ("Campaign Captain", "New", "trillinium1"),
            ("Campaign Captain", "Existing", "xdirtinx01"),
            ("Posting Champion", "New", "xspectralcinx01"),
            ("Posting Champion", "Existing", "xinfosusltdxwrap"),
            ("MVP", "New", "xOrange_Wings_inx02"),
            ("MVP", "New", "xSeharish_Khulinx01"),
            ("MVP", "New", "xe_advantuminx01"),
            ("MVP", "New", "xe_rebafsinx01"),
            ("MVP", "New", "izeemanpower3"),
            ("MVP", "Existing", "xiciciblinx04"),
            ("MVP", "Existing", "xltitinx159"),
            ("MVP", "Existing", "xCertzine_Recrinx01"),
            ("MVP", "Existing", "C1xrkplacinx01"),
            ("MVP", "Existing", "brraysoft01"),
        }
        self.assertEqual(actual, expected)


class SubmissionArtifactTests(unittest.TestCase):
    def test_workflow_exports_have_expected_structure(self):
        expected_nodes = {
            "Manual Run",
            "Weekly Scheduled Run",
            "Download Latest Purchase File",
            "Clear Old Purchase File",
            "Save Purchase Input",
            "Run APMM Pipeline",
            "If",
            "Success Summary",
            "Read Winners Excel",
            "Update Winners in Drive",
            "Send Success Email",
            "Failure Summary",
            "Send Failure Email",
        }
        workflows = [
            ("foundit_apmm_n8n_workflow.json", True),
            ("foundit_apmm_n8n_workflow_hosted.json", False),
        ]
        for filename, expected_active in workflows:
            workflow = json.loads(
                (BASE_DIR / "n8n" / filename).read_text(encoding="utf-8")
            )
            nodes = {node["name"]: node for node in workflow["nodes"]}
            self.assertEqual(set(nodes), expected_nodes)
            self.assertIs(workflow["active"], expected_active)
            self.assertEqual(
                nodes["Send Success Email"]["parameters"]["emailType"],
                "text",
            )
            self.assertEqual(
                nodes["Send Failure Email"]["parameters"]["emailType"],
                "text",
            )
            schedule = nodes["Weekly Scheduled Run"]["parameters"]["rule"][
                "interval"
            ][0]
            self.assertEqual(schedule["field"], "weeks")
            self.assertEqual(schedule["triggerAtDay"], [1])
            self.assertEqual(schedule["triggerAtHour"], 9)

            connections = workflow["connections"]
            self.assertEqual(
                connections["Manual Run"]["main"][0][0]["node"],
                "Run APMM Pipeline",
            )
            self.assertEqual(
                connections["Weekly Scheduled Run"]["main"][0][0]["node"],
                "Download Latest Purchase File",
            )
            self.assertEqual(
                connections["If"]["main"][0][0]["node"],
                "Success Summary",
            )
            self.assertEqual(
                connections["If"]["main"][1][0]["node"],
                "Failure Summary",
            )

    def test_hosted_workflow_cannot_read_environment_secrets(self):
        workflow = json.loads(
            (
                BASE_DIR / "n8n" / "foundit_apmm_n8n_workflow_hosted.json"
            ).read_text(encoding="utf-8")
        )
        serialized_parameters = json.dumps(
            [node["parameters"] for node in workflow["nodes"]]
        )
        self.assertNotIn("process.env", serialized_parameters)
        self.assertNotIn("$env", serialized_parameters)

        compose = (BASE_DIR / "deploy" / "n8n" / "compose.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn('N8N_BLOCK_ENV_ACCESS_IN_NODE: "true"', compose)

    def test_bonus_note_is_complete(self):
        note = (BASE_DIR / "notes" / "task3_bonus_analysis.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(note.count("```"), 0)
        self.assertIn("## Data-Backed Insights", note)
        self.assertIn("## Recommended Improvements", note)

    def test_system_prompt_contains_required_guardrails(self):
        prompt = (BASE_DIR / "notes" / "task1_system_prompt.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Answer only from the provided dataset", prompt)
        self.assertIn("Do not invent numbers", prompt)
        self.assertIn("Do not combine separate cuts", prompt)
        self.assertIn("salary", prompt)


if __name__ == "__main__":
    unittest.main()
