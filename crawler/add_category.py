import json

INPUT = "data/final_verified_businesses.json"
OUTPUT = "data/final_verified_businesses.json"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0

for trader in data:

    text = (
        trader.get("company_name", "") + " " +
        trader.get("website", "")
    ).lower()

    category = "Tea Business"

    if "retail" in text or "store" in text or "shop" in text:
        category = "Tea Retail Shop"

    elif "trader" in text or "trading" in text:
        category = "Tea Trader"

    elif "wholesale" in text or "dealer" in text:
        category = "Tea Wholesaler"

    elif "export" in text:
        category = "Tea Exporter"

    elif "factory" in text or "manufacturing" in text:
        category = "Tea Manufacturer"

    elif "garden" in text or "estate" in text:
        category = "Tea Garden"

    elif "pack" in text or "packaging" in text:
        category = "Tea Packaging"

    trader["business_category"] = category
    count += 1

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Categories Assigned :", count)