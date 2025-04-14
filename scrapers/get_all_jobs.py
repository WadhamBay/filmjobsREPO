import json
from scrapers.staffmeup_scraper import get_staffmeup_jobs
from scrapers.mandy_scraper import get_mandy_jobs
from scrapers.talentmanager_scraper import get_talent_manager_jobs
from scrapers.google_jobs import get_google_jobs

def get_all_jobs():
    all_jobs = []
    errors = []

    try:
        jobs = get_staffmeup_jobs()
        all_jobs.extend(jobs)
    except Exception as e:
        errors.append(f"StaffMeUp failed: {str(e)}")

    try:
        jobs = get_mandy_jobs()
        all_jobs.extend(jobs)
    except Exception as e:
        errors.append(f"Mandy failed: {str(e)}")

    try:
        jobs = get_talent_manager_jobs()
        all_jobs.extend(jobs)
    except Exception as e:
        errors.append(f"Talent Manager failed: {str(e)}")

    try:
        jobs = get_google_jobs()
        all_jobs.extend(jobs)
    except Exception as e:
        errors.append(f"Google Jobs failed: {str(e)}")

    print(f"✅ get_all_jobs() returning {len(all_jobs)} jobs with errors: {errors}")
    return {"jobs": all_jobs, "errors": errors}

if __name__ == "__main__":
    result = get_all_jobs()
    print(json.dumps(result, indent=2))
