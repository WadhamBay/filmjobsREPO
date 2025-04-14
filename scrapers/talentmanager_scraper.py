import requests
from bs4 import BeautifulSoup

def get_talent_manager_jobs(pages=5):
    print("📡 Calling get_talent_manager_jobs...")
    jobs = []
    base_url = "https://www.thetalentmanager.com/jobs?size=10&page={}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        for page in range(1, pages + 1):
            url = base_url.format(page)
            res = requests.get(url, headers=headers)
            print(f"🧪 TM page {page} status: {res.status_code}")
            soup = BeautifulSoup(res.text, "html.parser")
            job_cards = soup.select("div.job")
            print(f"🧪 Page {page}: Found {len(job_cards)} TM job cards")

            if not job_cards:
                print(f"📭 No jobs on TM page {page}, stopping.")
                break

            for card in job_cards:
                title_elem = card.select_one("a.job-title")
                company_elem = card.select_one(".company")
                location_elem = card.select_one(".location")

                title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                location = location_elem.get_text(strip=True) if location_elem else "Unknown"
                link = "https://www.thetalentmanager.com" + title_elem["href"] if title_elem else "#"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "date_posted": "recent",
                    "link": link
                })
    except Exception as e:
        print(f"❌ Talent Manager scrape failed: {e}")

    return jobs
