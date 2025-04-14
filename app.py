from flask import Flask, jsonify
from flask_cors import CORS
from scrapers.get_all_jobs import get_all_jobs
import os
import json
import time

app = Flask(__name__)
CORS(app)

CACHE_FILE = "jobs.json"
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds

def is_cache_fresh(file_path):
    return os.path.exists(file_path) and (time.time() - os.path.getmtime(file_path) < CACHE_DURATION)

@app.route("/api/jobs")
def jobs_api():
    if is_cache_fresh(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                jobs = json.load(f)
            return jsonify({"jobs": jobs, "errors": []})
        except Exception as e:
            return jsonify({"jobs": [], "errors": [f"Error reading jobs.json: {str(e)}"]})
    else:
        try:
            result = get_all_jobs()
            with open(CACHE_FILE, "w") as f:
                json.dump(result["jobs"], f, indent=2)
            return jsonify(result)
        except Exception as e:
            return jsonify({"jobs": [], "errors": [f"Scraper failed: {str(e)}"]})

@app.route("/")
def home():
    return "✅ FilmJobs API is live. Try /api/jobs"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
