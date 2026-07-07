from flask import redirect, render_template, request, session, url_for

from helpers import is_admin
from models import User, db


def register_routes(app):
    @app.route("/admin/approvals")
    def admin_approvals():
        if not is_admin():
            return redirect(url_for("dashboard"))
        pending = User.query.filter_by(role="store_manager", approved=False).all()
        return render_template("approvals.html", pending=pending)

    @app.route("/admin/approve/<int:user_id>", methods=["POST"])
    def approve_user(user_id):
        if not is_admin():
            return redirect(url_for("dashboard"))
        user = db.session.get(User, user_id)
        if user and user.role == "store_manager":
            user.approved = True
            db.session.commit()
        return redirect(url_for("admin_approvals"))

    @app.route("/admin/reject/<int:user_id>", methods=["POST"])
    def reject_user(user_id):
        if not is_admin():
            return redirect(url_for("dashboard"))
        user = db.session.get(User, user_id)
        if user and user.role == "store_manager":
            db.session.delete(user)
            db.session.commit()
        return redirect(url_for("admin_approvals"))
