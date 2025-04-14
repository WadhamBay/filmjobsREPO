import requests
import json

def get_google_jobs():
    api_key = "9bb19ffe2ecf0a94607704bc225baf3b659fd1c7c915052a8a18d49be226dda6"
    base_url = "https://serpapi.com/search.json"
    # Expanded list of queries to cover a wide range of film job roles
    queries = [
        # Cinematography
        "cinematographer jobs",
        "director of photography jobs",
        "DOP jobs",
        
        # Camera and grip roles
        "camera operator jobs",
        "assistant camera operator jobs",
        "dolly grip jobs",
        "steadicam operator jobs",
        
        # Lighting
        "gaffer jobs",
        "lighting technician jobs",
        "best boy jobs",
        
        # Production assistants
        "production assistant film jobs",
        "set runner film jobs",
        
        # Editing
        "film editor jobs",
        "assistant editor jobs",
        
        # Sound
        "sound recordist jobs",
        "boom operator jobs",
        
        # Makeup and hair
        "makeup artist film jobs",
        "hair stylist film jobs",
        
        # Art department
        "art director film jobs",
        "set designer film jobs",
        
        # Casting
        "casting director jobs film",
        "casting assistant film jobs",
        
        # General film production roles
        "film crew jobs",
        "film production jobs",
        "freelance film jobs",
        "film industry jobs"
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
            print(f"🔍 Query '{query}' returned {len(jobs)} jobs")
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

if __name__ == "__main__":
    results = get_google_jobs()
    print(f"Total jobs fetched: {len(results)}")
    # Optionally, save to a file for debugging
    with open("google_jobs.json", "w") as f:
        json.dump(results, f, indent=2)
