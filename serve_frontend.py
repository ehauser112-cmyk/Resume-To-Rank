import os

from run import app


if __name__ == "__main__":
    host = os.environ.get("RESUME_TO_RANK_HOST", "0.0.0.0")
    port = int(os.environ.get("RESUME_TO_RANK_PORT", "5055"))
    app.run(host=host, port=port, debug=False, use_reloader=False)
