from flask import Flask

from config import Config
from database.database import db
from routes.traders import trader_bp
from routes.search import search_bp
import os

from routes.home import home_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(trader_bp)
app.register_blueprint(search_bp)

with app.app_context():
    db.create_all()

with app.app_context():

    from models.trader import Trader

    traders = Trader.query.all()

    for t in traders:

        if len(t.company_name) > 60:

            print("=" * 80)
            print("ID :", t.id)
            print("Company :", t.company_name)
            print("=" * 80)    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)