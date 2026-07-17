import json
import re

with open("data/raw_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

traders = []

phone_count = 0
email_count = 0
address_count = 0

for item in data:

    text = item.get("content", "")

    phones = list(set(re.findall(phone_pattern, text)))
    emails = list(set(re.findall(email_pattern, text)))

    if len(text) > 50:
        address_count += 1

    phone_count += len(phones)
    email_count += len(emails)

    traders.append({
        "name": item.get("title", ""),
        "url": item.get("url", ""),
        "address": text[:500],
        "phones": phones,
        "emails": emails
    })

with open("data/tea_traders.json", "w", encoding="utf-8") as f:
    json.dump(traders, f, indent=4, ensure_ascii=False)

print("========== RESULT ==========")
print("Total Traders :", len(traders))
print("Phones Found  :", phone_count)
print("Emails Found  :", email_count)
print("Addresses     :", address_count)
print("============================")