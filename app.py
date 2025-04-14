from flask import Flask, jsonify
from flask_cors import CORS
from scrapers.get_all_jobs import get_all_jobs
import os
import sys

app = Flask(__name__)
CORS(app)

def flush_print(*args, **kwargs):
    """Print and flush immediately for Render logging."""
    print(*args, **kwargs)
    sys.stdout.flush()

@app.route("/api/jobs")
def jobs_api():
    flush_print("🔔 /api/jobs endpoint hit")
    try:
        # Call get_all_jobs() from your orchestrator
        result = get_all_jobs()
        jobs = result.get("jobs", [])
        flush_print(f"✅ get_all_jobs() returned {len(jobs)} jobs")
        return jsonify(result)
    except Exception as e:
        flush_print(f"❌ get_all_jobs() failed: {e}")
        return jsonify({"jobs": [], "errors": [f"Scraper failed: {str(e)}"]})

@app.route("/")
def home():
    return "✅ FilmJobs API is live. Try /api/jobs"

if __name__ == "__main__":
    flush_print("🚀 Starting Flask server...")
    app.run(host="0.0.0.0", port=10000)
