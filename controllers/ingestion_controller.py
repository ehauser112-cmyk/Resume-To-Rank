from flask import jsonify
from app.services.file_ingestion_service import FileIngestionService

class IngestionController:

    @staticmethod
    def upload(request):
        try:
            files = request.files.getlist("files")
            result = FileIngestionService.handle_upload(files)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
