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

URL_BRIGHTDATA = "https://api.brightdata.com/datasets/filter"

TOKEN_BRIGHTDATA = "d5e9d50a4e6c947a95c2781c643249210494d0e309f76ad3fdd8aa42cbbebb71"

RECORDS_LIMIT = 2
