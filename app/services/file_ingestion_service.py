from pathlib import Path

from flask import current_app
from werkzeug.utils import secure_filename

from app.services.resume_store import ResumeStore


class FileIngestionService:
    @staticmethod
    def handle_upload(files):
        if not files:
            return {"uploaded": [], "rejected": [], "message": "No files provided"}

        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        upload_folder.mkdir(parents=True, exist_ok=True)

        allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]
        uploaded = []
        rejected = []

        for file_storage in files:
            filename = secure_filename(file_storage.filename or "")
            extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

            if not filename or extension not in allowed_extensions:
                rejected.append(filename or "unnamed")
                continue

            destination = upload_folder / filename
            file_storage.save(destination)
            ResumeStore.add_uploaded_file(destination)
            uploaded.append(filename)

        return {"uploaded": uploaded, "rejected": rejected}

