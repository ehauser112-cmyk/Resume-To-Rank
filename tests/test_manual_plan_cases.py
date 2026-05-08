import io
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.services.resume_store import ResumeStore


class ManualPlanTestConfig:
    TESTING = True
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024

    def __init__(self, root):
        self.UPLOAD_FOLDER = str(root / "uploads")
        self.OUTPUT_FOLDER = str(root / "output")
        self.TEMP_FOLDER = str(root / "temp")


class ResumeToRankManualPlanScriptTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.app = create_app(ManualPlanTestConfig(root))
        self.client = self.app.test_client()
        ResumeStore.reset()

    def tearDown(self):
        self.temp_dir.cleanup()
        ResumeStore.reset()

    def upload_resumes(self, resumes):
        files = [(io.BytesIO(content.encode("utf-8")), filename) for filename, content in resumes]
        response = self.client.post(
            "/upload",
            data={"files": files},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        return response.get_json()

    def parse_uploaded_resumes(self):
        response = self.client.post("/parse")
        self.assertEqual(response.status_code, 200)
        return response.get_json()

    def rank_by(self, criteria):
        response = self.client.post("/rank", json={"criteria": criteria})
        self.assertEqual(response.status_code, 200)
        return response.get_json()

    def sort_by(self, key):
        response = self.client.post("/sort", json={"key": key})
        self.assertEqual(response.status_code, 200)
        return response.get_json()

    def seed_ranked_candidates(self):
        self.upload_resumes(
            [
                ("alex.txt", "Python SQL leadership"),
                ("blair.txt", "Python project management"),
                ("casey.txt", "Customer support"),
            ]
        )
        self.parse_uploaded_resumes()
        return self.rank_by(["python", "sql"])

    def test_tc_01_generate_ranking_table_based_on_selected_criteria(self):
        self.upload_resumes(
            [
                ("alex.txt", "Python SQL leadership"),
                ("blair.txt", "Python project management"),
                ("casey.txt", "Customer support"),
            ]
        )
        parsed = self.parse_uploaded_resumes()
        ranked = self.rank_by(["python", "sql"])["ranked"]

        self.assertEqual(parsed["count"], 3)
        self.assertEqual([candidate["filename"] for candidate in ranked], ["alex.txt", "blair.txt", "casey.txt"])
        self.assertEqual([candidate["score"] for candidate in ranked], [2, 1, 0])
        self.assertEqual(ranked[0]["matches"], ["python", "sql"])

    def test_tc_02_generate_new_ranking_table_when_one_already_exists(self):
        self.upload_resumes(
            [
                ("alex.txt", "Python SQL leadership"),
                ("blair.txt", "Project management communication"),
                ("casey.txt", "SQL data analysis"),
            ]
        )
        self.parse_uploaded_resumes()

        first_rank = self.rank_by(["python"])["ranked"]
        refreshed_rank = self.rank_by(["communication"])["ranked"]

        self.assertEqual(first_rank[0]["filename"], "alex.txt")
        self.assertEqual(refreshed_rank[0]["filename"], "blair.txt")
        self.assertEqual(refreshed_rank[0]["matches"], ["communication"])

    @unittest.skip("TC-03 requires an authentication and upload page UI that is not present in this API-only app.")
    def test_tc_03_access_resume_upload_as_logged_in_hiring_manager(self):
        pass

    def test_tc_04_upload_multiple_resumes_in_one_request(self):
        uploaded = self.upload_resumes(
            [
                ("alex.txt", "Python SQL leadership"),
                ("blair.txt", "Project management"),
            ]
        )
        parsed = self.parse_uploaded_resumes()

        self.assertEqual(uploaded["uploaded"], ["alex.txt", "blair.txt"])
        self.assertEqual(uploaded["rejected"], [])
        self.assertEqual(parsed["count"], 2)

    @unittest.skip("TC-05 requires authorization controls that are not present in this API-only app.")
    def test_tc_05_restrict_resume_access_to_authorized_users(self):
        pass

    @unittest.skip("TC-06 requires user-scoped resume storage that is not present in this API-only app.")
    def test_tc_06_verify_stored_resumes_remain_private(self):
        pass

    @unittest.skip("TC-07 requires session logout and protected pages that are not present in this API-only app.")
    def test_tc_07_verify_privacy_during_normal_logged_in_use(self):
        pass

    def test_tc_08_display_uploaded_candidates_after_parsing(self):
        self.upload_resumes(
            [
                ("alex.txt", "Python SQL leadership"),
                ("blair.txt", "Project management"),
            ]
        )
        parsed = self.parse_uploaded_resumes()["parsed"]

        self.assertEqual([candidate["filename"] for candidate in parsed], ["alex.txt", "blair.txt"])
        self.assertTrue(all(candidate["text"] for candidate in parsed))

    def test_tc_09_sort_candidates_by_selected_top_skill_score(self):
        self.seed_ranked_candidates()
        sorted_result = self.sort_by("score")["ranked"]

        self.assertEqual([candidate["score"] for candidate in sorted_result], [2, 1, 0])
        self.assertEqual(sorted_result[0]["filename"], "alex.txt")

    def test_tc_10_change_sorting_from_score_to_filename(self):
        self.seed_ranked_candidates()

        score_sorted = self.sort_by("score")["ranked"]
        filename_sorted = self.sort_by("filename")["ranked"]

        self.assertEqual([candidate["score"] for candidate in score_sorted], [2, 1, 0])
        self.assertEqual([candidate["filename"] for candidate in filename_sorted], ["alex.txt", "blair.txt", "casey.txt"])

    def test_tc_11_sort_candidates_when_some_do_not_match_selected_skill(self):
        self.upload_resumes(
            [
                ("alex.txt", "Python SQL leadership"),
                ("blair.txt", "Project management"),
                ("casey.txt", "Customer support"),
            ]
        )
        self.parse_uploaded_resumes()
        ranked = self.rank_by(["sql"])["ranked"]

        self.assertEqual(ranked[0]["filename"], "alex.txt")
        self.assertEqual(ranked[0]["score"], 1)
        self.assertTrue(all(candidate["score"] == 0 for candidate in ranked[1:]))

    def test_tc_12_ranking_and_sorting_remain_usable_with_longer_candidate_list(self):
        self.upload_resumes(
            [
                ("candidate_01.txt", "Python SQL leadership"),
                ("candidate_02.txt", "Python"),
                ("candidate_03.txt", "SQL"),
                ("candidate_04.txt", "AWS"),
                ("candidate_05.txt", "Communication"),
                ("candidate_06.txt", "Python SQL AWS"),
                ("candidate_07.txt", "Project management"),
                ("candidate_08.txt", "Python data analysis"),
            ]
        )
        parsed = self.parse_uploaded_resumes()
        ranked = self.rank_by(["python", "sql", "aws"])["ranked"]
        sorted_by_filename = self.sort_by("filename")["ranked"]

        self.assertEqual(parsed["count"], 8)
        self.assertEqual(len(ranked), 8)
        self.assertEqual(ranked[0]["filename"], "candidate_06.txt")
        self.assertEqual(ranked[0]["score"], 3)
        self.assertEqual(sorted_by_filename[0]["filename"], "candidate_01.txt")
        self.assertEqual(sorted_by_filename[-1]["filename"], "candidate_08.txt")


if __name__ == "__main__":
    unittest.main(verbosity=2)
