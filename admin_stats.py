from flask import render_template
from sqlalchemy import func

from models import GroceryItem, Purchase, User, db


def register_routes(app):
    @app.route("/admin/stats")
    def admin_stats():
        total_users = User.query.count()
        total_store_managers = User.query.filter_by(role="store_manager").count()
        total_admins = User.query.filter_by(role="admin").count()
        total_items = GroceryItem.query.count()
        total_purchases = Purchase.query.count()
        total_sales = db.session.query(func.sum(Purchase.total_price)).scalar() or 0
        total_quantity_sold = db.session.query(func.sum(Purchase.quantity)).scalar() or 0
        out_of_stock = GroceryItem.query.filter(GroceryItem.stock == 0).count()

        return render_template(
            "stats.html",
            total_users=total_users,
            total_store_managers=total_store_managers,
            total_admins=total_admins,
            total_items=total_items,
            total_purchases=total_purchases,
            total_sales=total_sales,
            total_quantity_sold=total_quantity_sold,
            out_of_stock=out_of_stock,
        )
