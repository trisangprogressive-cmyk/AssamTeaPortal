from app import app
from database.database import db
from models.trader import Trader

BAD_WORDS = [
    "copyright",
    "all rights reserved",
    "government",
    "directorate",
    "privacy",
    "terms",
    "rebrewed",
    "caffeine",
    "authenticity",
    "guaranteed",
    "monitor",
    "stock",
    "bse",
    "products",
    "services",
    "offer",
    "offering",
    "web(",
    "www.",
    "http"
]

with app.app_context():

    traders = Trader.query.all()

    deleted = 0

    for t in traders:

        name = (t.company_name or "").lower()

        if len(name) > 60:
            db.session.delete(t)
            deleted += 1
            continue

        if any(word in name for word in BAD_WORDS):
            db.session.delete(t)
            deleted += 1
            continue

    db.session.commit()

    print("="*40)
    print("Deleted :", deleted)
    print("Remaining :", Trader.query.count())
    print("="*40)