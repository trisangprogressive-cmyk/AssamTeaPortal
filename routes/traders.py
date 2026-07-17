from flask import Blueprint, render_template, request, redirect, url_for
from models.trader import Trader
from database.database import db

trader_bp = Blueprint("trader", __name__, url_prefix="/traders")


@trader_bp.route("/")
def list_traders():
    traders = Trader.query.order_by(Trader.company_name).all()
    return render_template("traders/list.html", traders=traders)


@trader_bp.route("/add", methods=["GET", "POST"])
def add_trader():

    if request.method == "POST":

        trader = Trader(
            company_name=request.form["company_name"],
            district=request.form["district"],
            phone=request.form["phone"],
            address=request.form["address"],
            verified=False
        )

        db.session.add(trader)
        db.session.commit()

        return redirect(url_for("trader.list_traders"))

    return render_template("traders/add.html")