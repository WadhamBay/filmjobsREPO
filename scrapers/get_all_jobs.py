import json
from scrapers.staffmeup_scraper import get_staffmeup_jobs
from scrapers.mandy_scraper import get_mandy_jobs
from scrapers.talentmanager_scraper import get_talent_manager_jobs
from scrapers.mandy_scraper import get_mandy_jobs

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

    # Save to jobs.json
    with open("jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    return {"jobs": all_jobs, "errors": errors}
