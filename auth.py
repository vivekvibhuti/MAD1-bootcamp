from flask import redirect, render_template, request, session, url_for

from helpers import is_allowed_edit, is_loggedin
from models import GroceryItem, User


def register_routes(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session["user_id"] = user.id
                session["username"] = user.username
                session["role"] = user.role
                return redirect(url_for("dashboard"))
            return render_template("login.html")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    @app.route("/dashboard", methods=["GET"])
    def dashboard():
        if not is_loggedin():
            return redirect(url_for("login"))
        grocery_items = GroceryItem.query.all()
        return render_template(
            "dashboard.html",
            username=session["username"],
            grocery_items=grocery_items,
            allowed_to_edit=is_allowed_edit(),
        )
