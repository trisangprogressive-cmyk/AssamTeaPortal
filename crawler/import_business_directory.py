import json
import csv
import os

OUTPUT = "data/master_traders.json"

traders = []

# Example importer for CSV exports
# Expected columns:
# Company Name, District, Phone, Address, Email, Website

CSV_FILE = "data/business_directory.csv"

if os.path.exists(CSV_FILE):

    with open(CSV_FILE, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            traders.append({

                "company_name": row.get("Company Name","").strip(),
                "district": row.get("District","").strip(),
                "phone": row.get("Phone","").strip(),
                "address": row.get("Address","").strip(),
                "email": row.get("Email","").strip(),
                "website": row.get("Website","").strip(),
                "verified": True

            })

with open(OUTPUT,"w",encoding="utf-8") as f:
    json.dump(traders,f,indent=4,ensure_ascii=False)

print("Imported:",len(traders))