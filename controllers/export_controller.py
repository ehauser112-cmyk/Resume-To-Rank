from flask import jsonify

from app.services.export_service import ExportService


class ExportController:
    @staticmethod
    def export():
        try:
            result = ExportService.export()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

