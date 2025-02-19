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

TOKEN_BRIGHTDATA = "394d9748-a353-471c-8b4d-36b96c011662"

RECORDS_LIMIT = 100
