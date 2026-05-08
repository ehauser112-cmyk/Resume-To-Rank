from pathlib import Path

from docx import Document
from pypdf import PdfReader

from app.services.resume_store import ResumeStore


class ResumeParserService:
    @staticmethod
    def parse_all():
        parsed = []

        for item in ResumeStore.uploaded_files:
            path = Path(item["path"])
            text = ResumeParserService._extract_text(path)
            parsed.append(
                {
                    "filename": item["filename"],
                    "path": str(path),
                    "text": text,
                }
            )

        ResumeStore.parsed_resumes = parsed
        return {"parsed": parsed, "count": len(parsed)}

    @staticmethod
    def _extract_text(path):
        suffix = path.suffix.lower()

        if suffix == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")

        if suffix == ".docx":
            return ResumeParserService._extract_docx_text(path)

        if suffix == ".pdf":
            return ResumeParserService._extract_pdf_text(path)

        return ""

    @staticmethod
    def _extract_docx_text(path):
        document = Document(path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    @staticmethod
    def _extract_pdf_text(path):
        reader = PdfReader(path)
        page_text = []

        for page in reader.pages:
            page_text.append(page.extract_text() or "")

        return "\n".join(page_text)
