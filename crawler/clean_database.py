import json
import re

INPUT = "data/final_traders.json"
OUTPUT = "data/verified_database.json"

BAD_NAMES = {
    "contact us",
    "home",
    "about",
    "about us",
    "privacy policy",
    "terms",
    "login",
    "register",
    "welcome",
    "index",
    "read more",
    "click here",
    "contact",
    "tea association"
}


def valid_phone(phone):
    if not phone:
        return False

    digits = re.sub(r"\D", "", phone)

    return len(digits) >= 10


with open(INPUT, "r", encoding="utf-8") as f:
    traders = json.load(f)

verified = []

seen_company = set()
seen_phone = set()

for t in traders:

    company = t.get("company_name", "").strip()
    phone = t.get("phone", "").strip()
    address = t.get("address", "").strip()

    if not company:
        continue

    if company.lower() in BAD_NAMES:
        continue

    # Company is mandatory
    if not company:
        continue

# Keep if it has EITHER a phone OR an address
    has_phone = valid_phone(phone)
    has_address = len(address.strip()) >= 5

    if not (has_phone or has_address):
       continue

    company_key = company.lower()
    phone_key = re.sub(r"\D", "", phone)

    if company_key in seen_company:
        continue

    if phone_key in seen_phone:
        continue

    seen_company.add(company_key)
    seen_phone.add(phone_key)

    verified.append(t)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(verified, f, indent=4, ensure_ascii=False)

print("=" * 40)
print("Original :", len(traders))
print("Verified :", len(verified))
print("=" * 40)