import json
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "raw_results.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "businesses.json")

PHONE_REGEX = r'(\+91[\-\s]?\d{10}|\d{10})'
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'

BAD_NAMES = {
    "contact us",
    "home",
    "about",
    "about us",
    "privacy policy",
    "login",
    "register",
    "welcome",
    "read more",
    "index"
     "contact us",
    "get in touch",
    "we'd love to hear from you",
    "we would love to hear from you",
    "shopping basket",
    "skip to content",
    "home",
    "welcome",
    "about us",
    "our products",
    "our story"

}


def extract_company(page):

    # 1. Try title first
    title = page.get("title", "").strip()

    if title:
        title = title.split("|")[0]
        title = title.split("-")[0]
        title = title.strip()

        if len(title) > 3 and title.lower() not in BAD_NAMES:
            return title

    # 2. Fall back to content
    text = page.get("content", "")

    for line in text.split("\n"):

        line = line.strip()

        if len(line) < 4:
            continue

        if line.lower() in BAD_NAMES:
            continue

        if any(word in line.lower() for word in [

            "tea",
            "trader",
            "traders",
            "shop",
            "estate",
            "garden",
            "company",
            "exports",
            "supplier",
            "agency",
            "distributor"

        ]):

            return line

    return ""
def extract_phone(text):

    text = text.replace("-", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")

    phones = []

    # Find Indian mobile numbers
    matches = re.findall(r'(?:\+91\s*|91\s*)?([6-9]\d{9})', text)

    for number in matches:

        # Skip repeated digits
        if len(set(number)) == 1:
            continue

        # Skip obvious fake numbers
        if number in {
            "9999999999",
            "8888888888",
            "7777777777",
            "6666666666",
            "1234567890",
            "0987654321"
        }:
            continue

        if number not in phones:
            phones.append(number)

    if phones:
        return ", ".join(phones)

    return ""

def extract_email(text):

    emails = re.findall(EMAIL_REGEX, text)

    if emails:
        return emails[0]

    return ""

def extract_address(text):

    lines = text.split("\n")

    for line in lines:

        line = line.replace("######", "").strip()

        if len(line) < 10:
            continue

        low = line.lower()

        # Skip unwanted lines
        if (
            "email" in low or
            "phone" in low or
            "shopping basket" in low or
            "skip to content" in low or
            "contact us" in low or
            "assam tea store" == low or
            "welcome" in low or
            "usd $" in low or
            "indian rupees" in low or
            "mon" in low or
            "sat" in low
        ):
            continue

        # Must look like a real postal address
        if (
            ("road" in low or
             "street" in low or
             "lane" in low or
             "near" in low or
             "market" in low or
             "bazar" in low or
             "paltan" in low or
             "assam" in low or
             "guwahati" in low)
            and re.search(r"\b\d{6}\b", line)
        ):
            return line

    return ""
DISTRICT_MAP = {

    "guwahati": "Kamrup Metro",
    "kamrup": "Kamrup",
    "jorhat": "Jorhat",
    "dibrugarh": "Dibrugarh",
    "tinsukia": "Tinsukia",
    "golaghat": "Golaghat",
    "sivasagar": "Sivasagar",
    "nagaon": "Nagaon",
    "sonitpur": "Sonitpur",
    "tezpur": "Sonitpur",
    "silchar": "Cachar",
    "cachar": "Cachar",
    "barpeta": "Barpeta",
    "nalbari": "Nalbari",
    "karimganj": "Karimganj",
    "lakhimpur": "Lakhimpur",
    "morigaon": "Morigaon",
    "hojai": "Hojai",
    "goalpara": "Goalpara",
    "kokrajhar": "Kokrajhar",
    "dhemaji": "Dhemaji",
    "biswanath": "Biswanath",
    "udalguri": "Udalguri",
    "bongaigaon": "Bongaigaon",
    "chirang": "Chirang",
    "baksa": "Baksa"
}

def extract_district(address, text):

    combined = (address + " " + text).lower()

    for key, value in DISTRICT_MAP.items():

        if key in combined:
            return value

    return ""


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    pages = json.load(f)

businesses = []

for page in pages:

    text = page.get("content", "")

    company = extract_company(page)

    if not company:
        continue

    phone = extract_phone(text)
    email = extract_email(text)
    address = extract_address(text)

    businesses.append({

        "company_name": company,
        "district": extract_district(address, text),
        "phone": phone,
        "email": email,
        "address": address,
        "website": page.get("url", ""),
        "verified": bool(phone and address)

    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(businesses, f, indent=4, ensure_ascii=False)

print("Businesses Found:", len(businesses))
print("Saved:", OUTPUT_FILE)