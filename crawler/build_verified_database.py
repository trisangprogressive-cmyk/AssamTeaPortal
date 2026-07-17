import json
import re

# Assam Districts
DISTRICTS = [
    "Baksa","Barpeta","Biswanath","Bongaigaon","Cachar","Charaideo",
    "Chirang","Darrang","Dhemaji","Dhubri","Dibrugarh","Dima Hasao",
    "Goalpara","Golaghat","Hailakandi","Hojai","Jorhat","Kamrup",
    "Kamrup Metro","Karbi Anglong","Karimganj","Kokrajhar",
    "Lakhimpur","Majuli","Morigaon","Nagaon","Nalbari",
    "Sivasagar","Sonitpur","South Salmara","Tamulpur",
    "Tinsukia","Udalguri","West Karbi Anglong"
]

PHONE_REGEX = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'

with open("data/raw_results.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

verified = []
seen = set()

for page in pages:

    title = page.get("title", "").strip()
    url = page.get("url", "")
    content = page.get("content", "")

    # Skip pages with almost no content
    if len(content) < 150:
        continue

    # Skip obvious non-business pages
    bad_words = [
        "wikipedia",
        "facebook",
        "instagram",
        "youtube",
        "linkedin",
        "pdf",
        "news",
        "article",
        "blog"
    ]

    if any(word in url.lower() for word in bad_words):
        continue

    # Find district
    district = "Unknown"

    for d in DISTRICTS:
        if d.lower() in (title + " " + content).lower():
            district = d
            break

    phones = sorted(set(re.findall(PHONE_REGEX, content)))
    emails = sorted(set(re.findall(EMAIL_REGEX, content)))

    address = ""

    # Try to extract address
    for line in content.split("\n"):
        line = line.strip()

        if district.lower() in line.lower():
            address = line
            break

    company = title.split("|")[0].split("-")[0].strip()

    key = (company.lower(), url)

    if key in seen:
        continue

    seen.add(key)

    verified.append({

        "company_name": company,
        "district": district,
        "phone": ", ".join(phones),
        "email": ", ".join(emails),
        "address": address,
        "website": url,
        "verified": True

    })

with open("data/verified_database.json", "w", encoding="utf-8") as f:
    json.dump(verified, f, indent=4, ensure_ascii=False)

print("=" * 50)
print("Verified Traders :", len(verified))
print("Saved : data/verified_database.json")
print("=" * 50)