import json
from tavily import TavilyClient
from config import DISTRICTS, SEARCH_QUERIES, OUTPUT_FILE

# ==========================
# ADD YOUR TAVILY API KEY
# ==========================

TAVILY_API_KEY = "YOUR_API_KEY"

client = TavilyClient(api_key=TAVILY_API_KEY)

results = []

for district in DISTRICTS:

    print(f"\n===== {district} =====")

    for query in SEARCH_QUERIES:

        search_query = f"{query} {district} Assam"

        print("Searching:", search_query)

        try:

            response = client.search(
                query=search_query,
                max_results=5
            )

            if "results" in response:

                for item in response["results"]:

                    results.append({

                        "district": district,
                        "query": query,
                        "title": item.get("title",""),
                        "url": item.get("url",""),
                        "content": item.get("content","")

                    })

        except Exception as e:

            print(e)

with open(OUTPUT_FILE,"w",encoding="utf-8") as f:

    json.dump(results,f,indent=4,ensure_ascii=False)

print("\nCollected",len(results),"pages.")