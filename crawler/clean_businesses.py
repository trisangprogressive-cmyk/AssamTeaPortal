import json

INPUT = "data/final_businesses.json"
OUTPUT = "data/final_verified_businesses.json"

BAD_NAMES = {
    "contact us",
    "home",
    "about",
    "privacy policy",
    "login",
    "register",
    "welcome",
    "read more",
    "index"
}

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

clean = []
seen = set()

for b in data:

    company = b.get("company_name", "").strip()

    if not company:
        continue

    if company.lower() in BAD_NAMES:
        continue

    key = company.lower()

    if key in seen:
        continue

    seen.add(key)

    clean.append(b)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(clean, f, indent=4, ensure_ascii=False)

print("=" * 40)
print("Original :", len(data))
print("Clean    :", len(clean))
print("=" * 40)