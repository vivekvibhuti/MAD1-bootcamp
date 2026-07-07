from flask import redirect, render_template, request, session, url_for

from models import GroceryItem, User, db


def register_routes(app):
    @app.route("/grocery/create", methods=["GET", "POST"])
    def create_grocery_item():
        if request.method == "POST":
            name = request.form["name"]
            price = float(request.form["price"])
            description = request.form.get("description", "")
            stock = int(request.form.get("stock", 0))
            item = GroceryItem(
                name=name, price=price, description=description, stock=stock
            )
            db.session.add(item)
            db.session.commit()
            return redirect(url_for("dashboard"))
        return render_template("create_grocery_item.html")

    @app.route("/grocery/<int:item_id>/edit", methods=["GET", "POST"])
    def edit_grocery_item(item_id):
        item = GroceryItem.query.get(item_id)
        if not item:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            item.name = request.form["name"]
            item.price = float(request.form["price"])
            item.description = request.form.get("description", "")
            item.stock = int(request.form.get("stock", 0))
            db.session.commit()
            return redirect(url_for("dashboard"))
        return render_template("edit_grocery_item.html", item=item)

    @app.route("/grocery/<int:item_id>/delete", methods=["POST"])
    def delete_grocery_item(item_id):
        item = GroceryItem.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
        return redirect(url_for("dashboard"))

    @app.route("/profile/edit", methods=["GET", "POST"])
    def edit_profile():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if request.method == "POST":
            user.username = request.form["username"]
            user.password = request.form["password"]
            db.session.commit()
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        return render_template("profile_edit.html", user=user)

    @app.route("/history/<int:user_id>")
    def purchase_history(user_id):
        user = User.query.get(user_id)
        if not user:
            return redirect(url_for("dashboard"))
        return render_template("history.html", user=user)
