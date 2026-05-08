import io
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.services.resume_store import ResumeStore


PDF_WITH_SKILLS = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length 55 >>
stream
BT /F1 24 Tf 72 720 Td (Python SQL leadership) Tj ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000241 00000 n
0000000311 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
416
%%EOF
"""


class TestConfig:
    TESTING = True
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024

    def __init__(self, root):
        self.UPLOAD_FOLDER = str(root / "uploads")
        self.OUTPUT_FOLDER = str(root / "output")
        self.TEMP_FOLDER = str(root / "temp")


class ResumeToRankAppTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.app = create_app(TestConfig(root))
        self.client = self.app.test_client()
        ResumeStore.reset()

    def tearDown(self):
        self.temp_dir.cleanup()
        ResumeStore.reset()

    def test_status_endpoint_reports_running(self):
        response = self.client.get("/status")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "running")

    def test_home_page_renders_frontend(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Resume to Rank", response.data)
        self.assertIn(b"Candidate ranking table", response.data)
        self.assertIn(b"Add skill", response.data)

    def test_upload_parse_rank_sort_and_export_resume(self):
        response = self.client.post(
            "/upload",
            data={
                "files": (
                    io.BytesIO(b"Python Flask SQL leadership"),
                    "candidate.txt",
                )
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["uploaded"], ["candidate.txt"])

        parse_response = self.client.post("/parse")
        self.assertEqual(parse_response.status_code, 200)
        self.assertEqual(parse_response.get_json()["count"], 1)

        rank_response = self.client.post("/rank", json={"criteria": ["python", "sql", "aws"]})
        ranked = rank_response.get_json()["ranked"]
        self.assertEqual(rank_response.status_code, 200)
        self.assertEqual(ranked[0]["filename"], "candidate.txt")
        self.assertEqual(ranked[0]["score"], 2)

        sort_response = self.client.post("/sort", json={"key": "filename"})
        self.assertEqual(sort_response.status_code, 200)
        self.assertEqual(sort_response.get_json()["sort_key"], "filename")

        export_response = self.client.post("/export")
        export_json = export_response.get_json()
        self.assertEqual(export_response.status_code, 200)
        self.assertEqual(export_json["count"], 1)
        self.assertTrue(Path(export_json["exported"]).exists())

    def test_clear_rankings_removes_ranked_results(self):
        self.client.post(
            "/upload",
            data={
                "files": (
                    io.BytesIO(b"Python Flask SQL leadership"),
                    "candidate.txt",
                )
            },
            content_type="multipart/form-data",
        )
        self.client.post("/parse")
        self.client.post("/rank", json={"criteria": ["python", "sql"]})

        clear_response = self.client.post("/rank/clear")

        self.assertEqual(clear_response.status_code, 200)
        self.assertEqual(clear_response.get_json(), {"ranked": [], "count": 0})
        self.assertEqual(ResumeStore.ranked_resumes, [])

    def test_docx_resume_text_is_ranked_by_matching_skills(self):
        document = Document()
        document.add_paragraph("Python SQL leadership")
        resume = io.BytesIO()
        document.save(resume)
        resume.seek(0)

        upload_response = self.client.post(
            "/upload",
            data={"files": (resume, "candidate.docx")},
            content_type="multipart/form-data",
        )
        self.assertEqual(upload_response.status_code, 200)

        parse_response = self.client.post("/parse")
        self.assertEqual(parse_response.status_code, 200)
        self.assertIn("Python SQL leadership", parse_response.get_json()["parsed"][0]["text"])

        rank_response = self.client.post("/rank", json={"criteria": ["python", "sql"]})
        ranked = rank_response.get_json()["ranked"]
        self.assertEqual(ranked[0]["filename"], "candidate.docx")
        self.assertEqual(ranked[0]["score"], 2)
        self.assertEqual(ranked[0]["matches"], ["python", "sql"])

    def test_pdf_resume_text_is_ranked_by_matching_skills(self):
        upload_response = self.client.post(
            "/upload",
            data={"files": (io.BytesIO(PDF_WITH_SKILLS), "candidate.pdf")},
            content_type="multipart/form-data",
        )
        self.assertEqual(upload_response.status_code, 200)

        parse_response = self.client.post("/parse")
        self.assertEqual(parse_response.status_code, 200)
        self.assertIn("Python SQL leadership", parse_response.get_json()["parsed"][0]["text"])

        rank_response = self.client.post("/rank", json={"criteria": ["python", "sql"]})
        ranked = rank_response.get_json()["ranked"]
        self.assertEqual(ranked[0]["filename"], "candidate.pdf")
        self.assertEqual(ranked[0]["score"], 2)
        self.assertEqual(ranked[0]["matches"], ["python", "sql"])

    def test_upload_rejects_unsupported_file_type(self):
        response = self.client.post(
            "/upload",
            data={"files": (io.BytesIO(b"not a resume"), "notes.exe")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["uploaded"], [])
        self.assertEqual(response.get_json()["rejected"], ["notes.exe"])


if __name__ == "__main__":
    unittest.main()
