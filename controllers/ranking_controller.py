from flask import jsonify
from app.services.ranking_service import RankingService

class RankingController:

    @staticmethod
    def rank(request):
        try:
            criteria = request.json.get("criteria", [])
            result = RankingService.rank(criteria)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def sort(request):
        try:
            key = request.json.get("key")
            result = RankingService.sort_by(key)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
