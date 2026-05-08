import os

class Config:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
    OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", os.path.join(BASE_DIR, "storage", "output"))
    TEMP_FOLDER = os.environ.get("TEMP_FOLDER", os.path.join(BASE_DIR, "storage", "temp"))

    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB
