from tavily import TavilyClient
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

DISTRICTS = [
    "Baksa",
    "Barpeta",
    "Biswanath",
    "Bongaigaon",
    "Cachar",
    "Charaideo",
    "Chirang",
    "Darrang",
    "Dhemaji",
    "Dhubri",
    "Dibrugarh",
    "Dima Hasao",
    "Goalpara",
    "Golaghat",
    "Hailakandi",
    "Hojai",
    "Jorhat",
    "Kamrup",
    "Kamrup Metro",
    "Karbi Anglong",
    "Karimganj",
    "Kokrajhar",
    "Lakhimpur",
    "Majuli",
    "Morigaon",
    "Nagaon",
    "Nalbari",
    "Sivasagar",
    "Sonitpur",
    "South Salmara",
    "Tamulpur",
    "Tinsukia",
    "Udalguri",
    "West Karbi Anglong"
]

SEARCHES = [

    "tea shop",
    "tea store",
    "tea retailer",
    "tea outlet",
    "tea seller",
    "tea dealer",
    "tea showroom",
    "tea boutique",
    "Assam tea shop",
    "Assam tea retailer",
    "Assam tea store",
    "buy Assam tea",
    "premium tea shop",
    "organic tea shop",
    "green tea shop"

]

GOOD_SITES = [

    "contact",
    "contact-us",
    "shop",
    "store",
    "retailer",
    "dealer",
    "supplier",
    "indiamart",
    "tradeindia",
    "justdial",
    "exportersindia"

]

BAD_SITES = [

    "facebook",
    "instagram",
    "youtube",
    "linkedin",
    "twitter",
    "x.com",
    "reddit",
    "quora",
    "wikipedia"

]

OUTPUT = "data/raw_results.json"

all_results = []
seen_urls = set()

for district in DISTRICTS:

    print(f"\n========== {district} ==========")

    for keyword in SEARCHES:

        query = f"{keyword} in {district} Assam contact number address"

        print("Searching :", query)

        try:

            result = client.search(
                query=query,
                search_depth="advanced",
                max_results=15
            )

            for item in result.get("results", []):

                url = item.get("url", "").strip()

                if not url:
                    continue

                url_lower = url.lower()

                if any(bad in url_lower for bad in BAD_SITES):
                    continue

                if not any(good in url_lower for good in GOOD_SITES):
                    continue

                if url in seen_urls:
                    continue

                seen_urls.add(url)

                all_results.append({
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0),
                    "raw_content": item.get("raw_content", "")
                })

            print("Collected :", len(all_results))

            time.sleep(1)

        except Exception as e:

            print("ERROR :", e)

os.makedirs("data", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:

    json.dump(all_results, f, indent=4, ensure_ascii=False)

print("\n===============================")
print("TOTAL UNIQUE PAGES :", len(all_results))
print("Saved to :", OUTPUT)
print("===============================")