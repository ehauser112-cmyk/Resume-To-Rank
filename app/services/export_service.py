import csv
from pathlib import Path

from flask import current_app

from app.services.resume_store import ResumeStore


class ExportService:
    @staticmethod
    def export():
        output_folder = Path(current_app.config["OUTPUT_FOLDER"])
        output_folder.mkdir(parents=True, exist_ok=True)
        destination = output_folder / "ranked_resumes.csv"

        with destination.open("w", newline="", encoding="utf-8") as export_file:
            writer = csv.DictWriter(export_file, fieldnames=["filename", "score", "matches"])
            writer.writeheader()
            for resume in ResumeStore.ranked_resumes:
                writer.writerow(
                    {
                        "filename": resume["filename"],
                        "score": resume["score"],
                        "matches": ", ".join(resume.get("matches", [])),
                    }
                )

        return {"exported": str(destination), "count": len(ResumeStore.ranked_resumes)}
