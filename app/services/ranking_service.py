from app.services.resume_store import ResumeStore


class RankingService:
    @staticmethod
    def rank(criteria):
        if criteria is None:
            criteria = []

        normalized_criteria = [str(item).lower() for item in criteria if str(item).strip()]
        ranked = []

        for resume in ResumeStore.parsed_resumes:
            text = resume.get("text", "").lower()
            matches = [criterion for criterion in normalized_criteria if criterion in text]
            ranked.append(
                {
                    "filename": resume["filename"],
                    "score": len(matches),
                    "matches": matches,
                }
            )

        ranked.sort(key=lambda item: item["score"], reverse=True)
        ResumeStore.ranked_resumes = ranked
        return {"ranked": ranked, "criteria": normalized_criteria}

    @staticmethod
    def sort_by(key):
        if key not in {"filename", "score"}:
            return {"error": "Invalid sort key", "allowed": ["filename", "score"]}

        reverse = key == "score"
        sorted_resumes = sorted(ResumeStore.ranked_resumes, key=lambda item: item[key], reverse=reverse)
        ResumeStore.ranked_resumes = sorted_resumes
        return {"ranked": sorted_resumes, "sort_key": key}

