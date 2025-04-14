import requests
from bs4 import BeautifulSoup

def get_staffmeup_jobs():
    print("📡 Scraping StaffMeUp...")
    jobs = []
    try:
        url = "https://staffmeup.com/jobs"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        listings = soup.select(".job-listing")
        for job in listings:
            title = job.select_one(".job-title").get_text(strip=True)
            company = job.select_one(".company").get_text(strip=True)
            location = job.select_one(".location").get_text(strip=True)
            link = "https://staffmeup.com" + job.select_one("a")["href"]
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "date_posted": "unknown",
                "link": link
            })
    except Exception as e:
        print(f"❌ StaffMeUp scrape failed: {e}")
    return jobs
