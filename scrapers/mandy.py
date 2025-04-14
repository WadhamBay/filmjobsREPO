import requests
from bs4 import BeautifulSoup

def get_mandy_jobs():
    url = "https://www.mandy.com/uk/jobs/film-tv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch Mandy jobs: {e}")

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    listings = soup.select(".job-listing") or soup.select(".job-card")
    for card in listings:
        title = card.select_one(".job-title")
        link = card.get("href") or card.find("a", href=True)
        location = card.select_one(".job-location")
        posted = card.select_one(".job-posted-date") or card.select_one(".job-date")

        job = {
            "title": title.get_text(strip=True) if title else "Unknown",
            "company": "Mandy",
            "location": location.get_text(strip=True) if location else "Unknown",
            "date_posted": posted.get_text(strip=True) if posted else "Recently",
            "link": f"https://www.mandy.com{link if isinstance(link, str) else link['href']}" if link else url
        }
        jobs.append(job)

    return jobs
