import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from database.database import db
from models.trader import Trader

INPUT = "data/final_verified_businesses.json"

with app.app_context():

    # Load JSON
    with open(INPUT, "r", encoding="utf-8") as f:
        traders = json.load(f)

    print("Deleting old database records...")

    Trader.query.delete()
    db.session.commit()

    imported = 0

    for t in traders:

        company = str(t.get("company_name", "")).strip()
        district = str(t.get("district", "")).strip()
        address = str(t.get("address", "")).strip()
        phone = str(t.get("phone", "")).strip()
        email = str(t.get("email", "")).strip()
        website = str(t.get("website", "")).strip()
        category = str(t.get("business_category", "")).strip()

        # Skip empty company names
        if not company:
            continue

        # Skip multiline garbage
        if "\n" in company:
            continue

        # Skip extremely long paragraphs
        if len(company) > 120:
            continue

        trader = Trader(
            company_name=company,
            district=district,
            address=address,
            phone=phone,
            email=email,
            website=website,
            business_category=category,
            verified=True
        )

        db.session.add(trader)
        imported += 1

    db.session.commit()

    print("=" * 50)
    print("Successfully Imported :", imported)
    print("=" * 50)