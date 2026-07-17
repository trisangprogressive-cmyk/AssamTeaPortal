import json

KEYWORDS = [
    "tea trader",
    "tea traders",
    "tea wholesaler",
    "tea supplier",
    "tea exporter",
    "tea company",
    "tea auction",
    "tea dealer"
]

with open("data/tea_traders.json", "r", encoding="utf-8") as f:
    data = json.load(f)

filtered = []

for item in data:

    text = (
        item.get("name", "") + " " +
        item.get("address", "") + " " +
        item.get("url", "")
    ).lower()

    if any(k in text for k in KEYWORDS):
        filtered.append(item)

print("Original :", len(data))
print("Filtered :", len(filtered))

with open("data/verified_traders.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=4, ensure_ascii=False)

print("Saved verified_traders.json")