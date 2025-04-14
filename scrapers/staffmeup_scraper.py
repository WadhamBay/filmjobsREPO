import requests
from bs4 import BeautifulSoup

def get_staffmeup_jobs():
    print("📡 Calling get_staffmeup_jobs...")
    jobs = []
    try:
        url = "https://staffmeup.com/jobs"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/111.0.0.0 Safari/537.36",
            "Referer": "https://staffmeup.com/"
        }
        res = requests.get(url, headers=headers, timeout=10)
        print(f"🧪 StaffMeUp status code: {res.status_code}")
        soup = BeautifulSoup(res.text, "html.parser")
        # Updated selector: trying both .job-listing and .job-card
        listings = soup.select(".job-listing") or soup.select(".job-card")
        print(f"🧪 Found {len(listings)} job listings on StaffMeUp")
        for job in listings:
            try:
                title_elem = job.select_one(".job-title")
                company_elem = job.select_one(".company")
                location_elem = job.select_one(".location")
                link_elem = job.find("a", href=True)
                title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                location = location_elem.get_text(strip=True) if location_elem else "Unknown"
                link = "https://staffmeup.com" + link_elem["href"] if link_elem and "href" in link_elem.attrs else url
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "date_posted": "unknown",
                    "link": link
                })
            except Exception as inner_e:
                print(f"❌ Error parsing a StaffMeUp job: {inner_e}")
    except Exception as e:
        print(f"❌ StaffMeUp scrape failed: {e}")
    return jobs
