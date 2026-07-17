from flask import Blueprint, render_template, request
from sqlalchemy import or_
from flask import abort

from database.database import db
from models.trader import Trader

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
def search():

    q = request.args.get("q", "").strip()

    district = request.args.get("district", "").strip()

    category = request.args.get("category", "").strip()

    query = Trader.query

    # -----------------------
    # Keyword Search
    # -----------------------

    if q:

        query = query.filter(

            or_(

                Trader.company_name.ilike(f"%{q}%"),

                Trader.district.ilike(f"%{q}%"),

                Trader.address.ilike(f"%{q}%"),

                Trader.phone.ilike(f"%{q}%"),

                Trader.email.ilike(f"%{q}%"),

                Trader.website.ilike(f"%{q}%"),

                Trader.business_category.ilike(f"%{q}%")

            )

        )

    # -----------------------
    # District Filter
    # -----------------------

    if district:

        query = query.filter(

            Trader.district == district

        )

    # -----------------------
    # Category Filter
    # -----------------------

    if category:

        query = query.filter(

            Trader.business_category == category

        )

    # -----------------------
    # Results
    # -----------------------

    results = query.order_by(

        Trader.company_name.asc()

    ).all()

    # -----------------------
    # District Dropdown
    # -----------------------

    districts = [

        d[0]

        for d in db.session.query(

            Trader.district

        ).distinct().order_by(

            Trader.district

        ).all()

        if d[0]

    ]

    # -----------------------
    # Category Dropdown
    # -----------------------

    categories = [

        c[0]

        for c in db.session.query(

            Trader.business_category

        ).distinct().order_by(

            Trader.business_category

        ).all()

        if c[0]

    ]

    return render_template(

        "search.html",

        query=q,

        district=district,

        category=category,

        districts=districts,

        categories=categories,

        results=results

    )
@search_bp.route("/business/<int:business_id>")
def business_details(business_id):

    trader = Trader.query.get(business_id)

    if trader is None:
        abort(404)

    return render_template(
        "business_details.html",
        trader=trader
    )