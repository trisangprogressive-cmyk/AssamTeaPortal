import json
import re

INPUT = "data/raw_results.json"
OUTPUT = "data/businesses.json"

PHONE_REGEX = r'(\+91[- ]?[6-9]\d{9}|[6-9]\d{9})'
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'

BAD_STARTS = [
    "we",
    "shipping",
    "buy",
    "email",
    "phone",
    "address",
    "contact",
    "welcome",
    "about",
    "privacy",
    "terms",
    "our",
    "thank",
    "copyright",
    "follow us"
]

BUSINESS_ENDINGS = [
    "tea estate",
    "tea garden",
    "tea traders",
    "tea trader",
    "tea company",
    "tea industries",
    "tea factory",
    "tea depot",
    "tea centre",
    "tea center",
    "tea shop",
    "tea exporter",
    "tea exports",
    "tea enterprise",
    "tea enterprises",
    "tea agency",
    "tea distributor",
    "tea distributors",
    "tea store"
]


def split_lines(text):
    text = text.replace("\r", "\n")

    lines = []

    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()

        if len(line) > 5:
            lines.append(line)

    return lines


def is_business(line):

    l = line.strip().lower()

    if len(l) < 4:
        return False

    if len(l) > 80:
        return False

    for bad in BAD_STARTS:
        if l.startswith(bad):
            return False

    for end in BUSINESS_ENDINGS:
        if l.endswith(end):
            return True

    return False


def extract_phone(text):

    phones = re.findall(PHONE_REGEX, text)

    if phones:
        return phones[0]

    return ""


def extract_email(text):

    emails = re.findall(EMAIL_REGEX, text)

    if emails:
        return emails[0]

    return ""


with open(INPUT, "r", encoding="utf-8") as f:
    pages = json.load(f)

businesses = []

for page in pages:

    url = page.get("url", "").lower()

    # Skip Tea Board PDFs
    if "teaboard.gov.in" in url and ".pdf" in url:
        continue

    content = page.get("content", "")

    lines = split_lines(content)

    for line in lines:

        if not is_business(line):
            continue

        businesses.append({

            "company_name": line.strip(),

            "district": "",

            "phone": extract_phone(content),

            "email": extract_email(content),

            "address": "",

            "website": page.get("url", ""),

            "verified": False

        })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(businesses, f, indent=4, ensure_ascii=False)

print("=" * 40)
print("Businesses Found :", len(businesses))
print("=" * 40)