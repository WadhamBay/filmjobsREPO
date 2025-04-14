import requests
from bs4 import BeautifulSoup

def get_productionhub_jobs():
    url = "https://www.productionhub.com/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch ProductionHUB jobs: {e}")

    soup = BeautifulSoup(res.text, "html.parser")
    jobs = []

    job_cards = soup.select(".job-card") or soup.select(".jobSearchResults .card")
    for card in job_cards:
        title_el = card.select_one(".job-title") or card.select_one("h2")
        company_el = card.select_one(".company-name")
        location_el = card.select_one(".job-location")
        date_el = card.select_one(".post-date") or card.select_one("time")
        link_el = card.select_one("a[href]")

        job = {
            "title": title_el.get_text(strip=True) if title_el else "Untitled",
            "company": company_el.get_text(strip=True) if company_el else "ProductionHUB",
            "location": location_el.get_text(strip=True) if location_el else "Unknown",
            "date_posted": date_el.get_text(strip=True) if date_el else "Recently",
            "link": f"https://www.productionhub.com{link_el['href']}" if link_el else url
        }
        jobs.append(job)

    return jobs
