from tavily import TavilyClient
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

DISTRICTS = [
     "Jorhat",
    "Dibrugarh",
    "Tinsukia",
    "Golaghat",
    "Sivasagar"
]

SOURCES = [
    "site:indiamart.com",
    "site:tradeindia.com",
    "site:justdial.com",
    "site:exportersindia.com"
]

KEYWORDS = [
    "tea trader",
    "tea supplier",
    "tea wholesaler",
    "tea exporter",
    "tea company",
    "tea manufacturer"
]

results = []
seen = set()

for district in DISTRICTS:

    print(f"\n========== {district} ==========")

    for source in SOURCES:

        for keyword in KEYWORDS:

            query = f"{source} {district} Assam {keyword}"

            print(query)

            try:

                response = client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=5
                )

                for item in response["results"]:

                    url = item.get("url","")

                    if url in seen:
                        continue

                    seen.add(url)

                    results.append(item)

                print("Collected:",len(results))

                time.sleep(1)

            except Exception as e:
                print(e)

with open("data/business_results.json","w",encoding="utf-8") as f:

    json.dump(results,f,indent=4,ensure_ascii=False)

print("\n=================================")
print("TOTAL BUSINESS PAGES :",len(results))
print("=================================")