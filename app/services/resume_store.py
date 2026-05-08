from pathlib import Path


class ResumeStore:
    uploaded_files = []
    parsed_resumes = []
    ranked_resumes = []

    @classmethod
    def reset(cls):
        cls.uploaded_files = []
        cls.parsed_resumes = []
        cls.ranked_resumes = []

    @classmethod
    def add_uploaded_file(cls, path):
        stored_path = Path(path)
        existing = [item for item in cls.uploaded_files if item["path"] != str(stored_path)]
        existing.append({"filename": stored_path.name, "path": str(stored_path)})
        cls.uploaded_files = existing

