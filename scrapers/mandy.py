import requests
from bs4 import BeautifulSoup

def get_mandy_jobs(pages=5):
    print("📡 Calling get_mandy_jobs (Paginated)...")
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/112.0.0.0 Safari/537.36",
        "Referer": "https://www.mandy.com/"
    }
    for page in range(1, pages + 1):
        url = f"https://www.mandy.com/aa/jobs/?page={page}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            print(f"🧪 Mandy page {page} status: {res.status_code}")
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            listings = soup.select("a.card-job")
            print(f"🧪 Mandy page {page}: Found {len(listings)} job cards")
            if not listings:
                print(f"📭 No jobs on Mandy page {page}, ending pagination.")
                break
            for card in listings:
                try:
                    title_elem = card.select_one(".card-title")
                    company_elem = card.select_one(".card-subtitle")
                    location_elem = card.select_one(".card-location")
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                    location = location_elem.get_text(strip=True) if location_elem else "Unknown"
                    link = card.get("href")
                    full_link = "https://www.mandy.com" + link if link and link.startswith("/") else (link if link else url)
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "date_posted": "recent",
                        "link": full_link
                    })
                except Exception as inner_e:
                    print(f"❌ Error parsing a Mandy job on page {page}: {inner_e}")
        except Exception as e:
            print(f"❌ Mandy scrape failed on page {page}: {e}")
    return jobs
