import requests
from bs4 import BeautifulSoup
import datetime
import json

# -----------------------------------------
# CONFIG
# -----------------------------------------

KEYWORDS = [
    "machine learning intern",
    "Artificial Intelligence intern",
    "Data Science intern"
]

LOCATIONS = ["Delhi", "Noida", "Gurgaon", "Gurugram", "Delhi NCR"]

OUTPUT_FILE = "latest_jobs.json"

# -----------------------------------------
# FUNCTIONS
# -----------------------------------------

def fetch_linkedin():
    """Scrape LinkedIn job search results (public results only)."""
    jobs = []
    for kw in KEYWORDS:
        url = f"https://www.linkedin.com/jobs/search/?keywords={kw.replace(' ', '%20')}&location=Delhi%20NCR&f_E=1"
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")

        for job in soup.select(".base-card"):
            title = job.select_one(".base-search-card__title")
            company = job.select_one(".base-search-card__subtitle")
            location = job.select_one(".job-search-card__location")
            link = job.select_one("a")["href"]

            if title and company:
                jobs.append({
                    "source": "LinkedIn",
                    "title": title.text.strip(),
                    "company": company.text.strip(),
                    "location": location.text.strip() if location else "",
                    "link": link,
                })
    return jobs


def fetch_indeed():
    """Scrape Indeed for internships."""
    jobs = []
    for kw in KEYWORDS:
        url = f"https://in.indeed.com/jobs?q={kw.replace(' ', '+')}&l=Delhi+NCR&sc=0kf%3Ajt(internship)%3B"
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")

        for card in soup.select("div.job_seen_beacon"):
            title = card.select_one("h2.jobTitle span")
            company = card.select_one(".companyName")
            location = card.select_one(".companyLocation")
            link = "https://in.indeed.com" + card.select_one("a")["href"]

            if title:
                jobs.append({
                    "source": "Indeed",
                    "title": title.text.strip(),
                    "company": company.text.strip() if company else "",
                    "location": location.text.strip() if location else "",
                    "link": link
                })
    return jobs


def main():
    print("Running daily job search...")

    linkedin_jobs = fetch_linkedin()
    indeed_jobs = fetch_indeed()

    all_jobs = linkedin_jobs + indeed_jobs

    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=4)

    print(f"Saved {len(all_jobs)} jobs to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
