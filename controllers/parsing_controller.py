from flask import jsonify
from app.services.resume_parser_service import ResumeParserService

class ParsingController:

    @staticmethod
    def parse():
        try:
            result = ResumeParserService.parse_all()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
