from flask import request, jsonify, render_template
from controllers.ingestion_controller import IngestionController
from controllers.parsing_controller import ParsingController
from controllers.ranking_controller import RankingController
from controllers.export_controller import ExportController
from app.services.resume_store import ResumeStore

def register_routes(app):

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/upload", methods=["POST"])
    def upload():
        return IngestionController.upload(request)

    @app.route("/parse", methods=["POST"])
    def parse():
        return ParsingController.parse()

    @app.route("/rank", methods=["POST"])
    def rank():
        return RankingController.rank(request)

    @app.route("/sort", methods=["POST"])
    def sort():
        return RankingController.sort(request)

    @app.route("/rank/clear", methods=["POST"])
    def clear_rankings():
        ResumeStore.ranked_resumes = []
        return jsonify({"ranked": [], "count": 0})

    @app.route("/export", methods=["POST"])
    def export():
        return ExportController.export()

    @app.route("/status", methods=["GET"])
    def status():
        return jsonify({"status": "running", "candidates": len(ResumeStore.uploaded_files)})
