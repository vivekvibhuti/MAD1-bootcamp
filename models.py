from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_init(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')


class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grocery_item_id = db.Column(db.Integer, db.ForeignKey('grocery_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='purchases')
    grocery_item = db.relationship('GroceryItem', backref='purchases')
