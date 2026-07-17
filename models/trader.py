from database.database import db
from datetime import datetime


class Trader(db.Model):

    __tablename__ = "traders"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(250), nullable=False)

    owner_name = db.Column(db.String(150))

    district = db.Column(db.String(100), index=True)

    address = db.Column(db.Text)

    pin_code = db.Column(db.String(20))

    phone = db.Column(db.String(50))

    whatsapp = db.Column(db.String(50))

    email = db.Column(db.String(150))

    website = db.Column(db.String(250))

    tea_type = db.Column(db.String(100))

    business_type = db.Column(db.String(100))

    business_category = db.Column(db.String(100))

    products = db.Column(db.Text)

    gst_number = db.Column(db.String(50))

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    google_map = db.Column(db.String(500))

    verified = db.Column(db.Boolean, default=False)

    source = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )