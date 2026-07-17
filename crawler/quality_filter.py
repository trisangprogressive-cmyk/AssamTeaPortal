import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "businesses.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "verified_display_database.json")
PARTIAL_FILE = os.path.join(BASE_DIR, "data", "partial_database.json")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    traders = json.load(f)

verified = []
partial = []

BAD_NAMES = {
    "contact us",
    "skip to content",
    "shopping basket",
    "welcome",
    "home",
    "about us",
    "we'd love to hear from you"
}

missing_phone = 0
missing_email = 0
missing_address = 0

for trader in traders:

    company = trader.get("company_name", "").strip()
    phone = trader.get("phone", "").strip()
    email = trader.get("email", "").strip()
    address = trader.get("address", "").strip()
    website = trader.get("website", "").strip()

    if not phone:
        missing_phone += 1

    if not email:
        missing_email += 1

    if not address:
        missing_address += 1

    # Keep only high-quality records
    if (
    company
    and website
    and address
    and (phone or email)
    and company.lower() not in BAD_NAMES
    and not any(bad in company.lower() for bad in BAD_NAMES)
):
        verified.append(trader)
    else:
        partial.append(trader)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(verified, f, indent=4, ensure_ascii=False)

with open(PARTIAL_FILE, "w", encoding="utf-8") as f:
    json.dump(partial, f, indent=4, ensure_ascii=False)

print("=" * 50)
print("Total Records      :", len(traders))
print("Verified Records  :", len(verified))
print("Partial Records   :", len(partial))
print()
print("Missing Phone     :", missing_phone)
print("Missing Email     :", missing_email)
print("Missing Address   :", missing_address)
print("=" * 50)