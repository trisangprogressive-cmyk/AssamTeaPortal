import requests
import json
import time

API_KEY = "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"

districts = [
    "Jorhat",
    "Dibrugarh",
    "Tinsukia",
    "Golaghat",
    "Sivasagar",
    "Sonitpur",
    "Nagaon",
    "Kamrup Metro",
    "Cachar",
    "Udalguri",
    "Biswanath",
    "Lakhimpur"
]

categories = [
    "Tea Trader",
    "Tea Estate",
    "Tea Garden",
    "Tea Retail Shop",
    "Tea Exporter"
]

businesses = []

for district in districts:
    for category in categories:

        query = f"{district} Assam {category} phone email address"

        print("Searching:", query)

        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": 10
            }
        )

        print(response.status_code)
        print(response.text)

        data = response.json()

        for r in data.get("results", []):

            businesses.append({
                "company_name": r.get("title", ""),
                "district": district,
                "address": "",
                "phone": "",
                "email": "",
                "website": r.get("url", ""),
                "business_category": category,
                "verified": True
            })

        time.sleep(1)

with open("data/clean_businesses.json", "w", encoding="utf-8") as f:
    json.dump(businesses, f, indent=4)

print("Businesses Collected:", len(businesses))