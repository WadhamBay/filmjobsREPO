from flask import Flask, jsonify
from scrapers.google_jobs import get_google_jobs
import os
import json

app = Flask(__name__)

@app.route("/api/jobs")
def get_all_jobs():
    jobs_file = "jobs.json"
    if os.path.exists(jobs_file):
        try:
            with open(jobs_file, "r") as f:
                jobs = json.load(f)
            return jsonify({"jobs": jobs, "errors": []})
        except Exception as e:
            return jsonify({"jobs": [], "errors": [f"Failed to read jobs.json: {str(e)}"]})
    else:
        try:
            jobs = get_google_jobs()
            return jsonify({"jobs": jobs, "errors": []})
        except Exception as e:
            return jsonify({"jobs": [], "errors": [f"Google Jobs failed: {str(e)}"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
