import requests
from bs4 import BeautifulSoup

def get_mandy_jobs(pages=5):
    print("📡 Calling get_mandy_jobs...")
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        for page in range(1, pages + 1):
            url = f"https://www.mandy.com/aa/jobs/?page={page}"
            response = requests.get(url, headers=headers)
            print(f"🧪 Mandy page {page} status: {response.status_code}")
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select("a.card-job")
            print(f"🧪 Page {page}: Found {len(listings)} Mandy job cards")

            if not listings:
                print(f"📭 No jobs on Mandy page {page}, stopping.")
                break

            for card in listings:
                title = card.select_one(".card-title").get_text(strip=True) if card.select_one(".card-title") else "Unknown"
                company = card.select_one(".card-subtitle").get_text(strip=True) if card.select_one(".card-subtitle") else "Unknown"
                location = card.select_one(".card-location").get_text(strip=True) if card.select_one(".card-location") else "Unknown"
                link = "https://www.mandy.com" + card["href"]
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "date_posted": "recent",
                    "link": link
                })
    except Exception as e:
        print(f"❌ Mandy scrape failed: {e}")
    return jobs
