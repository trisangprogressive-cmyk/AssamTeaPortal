from flask import Blueprint, render_template
from models.trader import Trader

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():

    total = Trader.query.count()

    return render_template(
        "index.html",
        total_traders=total
    )