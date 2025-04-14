import requests
import json

def get_google_jobs():
    api_key = "9bb19ffe2ecf0a94607704bc225baf3b659fd1c7c915052a8a18d49be226dda6"
    base_url = "https://serpapi.com/search.json"
    queries = [
        "cinematographer jobs",
        "film crew jobs",
        "videographer jobs",
        "director of photography jobs",
        "gaffer jobs",
        "production assistant film",
        "sound recordist film",
        "camera operator jobs",
        "film jobs UK",
        "freelance film jobs"
    ]
    all_jobs = []
    for query in queries:
        params = {
            "engine": "google_jobs",
            "q": query,
            "api_key": api_key
        }
        try:
            res = requests.get(base_url, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            jobs = data.get("jobs_results", [])
            print(f"🔍 Google Jobs Query '{query}' returned {len(jobs)} jobs")
            for job in jobs:
                all_jobs.append({
                    "title": job.get("title", "Unknown"),
                    "company": job.get("company_name", "Unknown"),
                    "location": job.get("location", "Unknown"),
                    "date_posted": job.get("detected_extensions", {}).get("posted_at", "Recently"),
                    "link": job.get("via", "https://serpapi.com")
                })
        except Exception as e:
            print(f"⚠️ SerpAPI failed for query '{query}': {e}")
    return all_jobs
