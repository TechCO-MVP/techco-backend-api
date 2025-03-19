TRADUCTION_FILTERS_BRIGHTDATA = {
    "city": {"name": "city", "operator": "includes"},
    "country_code": {"name": "country_code", "operator": "="},
    "role": {"name": ["position", "experience"], "operator": "includes"},
    "languages": {"name": "languages", "operator": "includes"},
    "seniority": {"name": ["position", "experience"], "operator": "includes"},
    "skills": {
        "name": ["education", "courses", "certifications", "experience", "about"],
        "operator": "includes",
    },
}

BASE_URL_BRIGHTDATA = "https://api.brightdata.com/datasets"

URL_BRIGHTDATA = "https://api.brightdata.com/datasets/filter"

RECORDS_LIMIT = 100

BRIGHT_DATA_DATASET_ID = "gd_l1viktl72bvl7bjuj0"
