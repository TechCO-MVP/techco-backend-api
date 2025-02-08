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

TOKEN_BRIGHTDATA = "03442ffe7ba98493f2294997d93c8984719ed8eb56b04ea35c1163a4303b466b"

RECORDS_LIMIT = 2
