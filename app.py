from flask import Flask, jsonify
from flask_cors import CORS
from scrapers.get_all_jobs import get_all_jobs
import os
import json
import time
import threading

app = Flask(__name__)
CORS(app)

CACHE_FILE = "jobs.json"
CACHE_DURATION = 24 * 60 * 60  # 1 day


def is_cache_fresh(file_path):
    return os.path.exists(file_path) and (time.time() - os.path.getmtime(file_path) < CACHE_DURATION)


def refresh_cache():
    try:
        print("🔄 Running background scraper...")
        result = get_all_jobs()
        with open(CACHE_FILE, "w") as f:
            json.dump(result["jobs"], f, indent=2)
        print(f"✅ Cache updated with {len(result['jobs'])} jobs.")
    except Exception as e:
        print(f"❌ Background scraper error: {e}")


@app.route("/api/jobs")
def jobs_api():
    # Start background update
    threading.Thread(target=refresh_cache).start()

    # Return cached results
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                jobs = json.load(f)
            return jsonify({"jobs": jobs, "errors": []})
        except Exception as e:
            return jsonify({"jobs": [], "errors": [f"Error reading jobs.json: {str(e)}"]})
    else:
        return jsonify({"jobs": [], "errors": ["No cached jobs available. Please try again in a moment."]})


@app.route("/")
def home():
    return "✅ FilmJobs API is live. Try /api/jobs"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
