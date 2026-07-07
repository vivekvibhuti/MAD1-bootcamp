from flask import Flask, redirect, render_template, request, session, url_for

from admin_stats import register_routes as register_stats
from approval import register_routes as register_approval
from auth import register_routes as register_auth
from grocery import register_routes as register_grocery
from helpers import (
    current_user,
    is_admin,
    is_allowed_edit,
    is_loggedin,
    is_store_manager,
    login_required,
)
from models import GroceryItem, Purchase, User, db, seed_admin
from seed_data import seed_data

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bootcamp.db"
app.secret_key = "replace_with_a_random_secret_key"

db.init_app(app)

register_stats(app)
register_approval(app)
register_auth(app)
register_grocery(app)


# default location for our url
@app.route("/")
def home():
    # return render_template("homepage.html")
    return render_template("homepage.html", is_loggedin=is_loggedin())


# list examples
# mylist = [ a, b, c]


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         # check for correct credentials later on
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             print(user.username, user.password)
#             return redirect(url_for("dashboard", username=username))
#         else:
#             return render_template("login.html")

#         # if credentials are incorrect, render the login form again
#         # return render_template("login.html")
#     return render_template("login.html")


# faulty code
# @app.route("/dashboard", methods=["GET"])
# def dashboard():
#     username = request.args.get("username")
#     print(username)
#     grocery_items = GroceryItem.query.all()
#     return render_template(
#         "dashboard.html", username=username, grocery_items=grocery_items
#     )


# proper dashboard with helpers and session — uncomment and comment out the original:
# @app.route("/dashboard", methods=["GET"])
# def dashboard():
#     if not is_loggedin():
#         return redirect(url_for("login"))
#     grocery_items = GroceryItem.query.all()
#     return render_template("dashboard.html", username=session["username"], grocery_items=grocery_items, allowed_to_edit=is_allowed_edit())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form.get("role", "user")

        approved = role == "user"
        user = User(username=username, password=password, role=role, approved=approved)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


# TODO:
# 1 create a page to show all users
# 2. create endpoint/route/handler to show all the users
#
# @app.route("/users")
# def users():
#     all_users = User.query.all()
#     return render_template("allusers.html", users=all_users)


# proper version with search — uncomment and comment out the original:
@app.route("/users")
def users():
    search = request.args.get("search", "")
    if search:
        all_users = User.query.filter(User.username.contains(search)).all()
    else:
        all_users = User.query.all()
    return render_template("allusers.html", users=all_users, query=search)


# dynamic route now:
@app.route("/user/<int:user_id>")
def user(user_id):
    user = User.query.get(user_id)
    return render_template("user_profile.html", user=user)


# delete route
@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("users"))


# proper version with admin check — uncomment and comment out the original:
# @app.route("/delete_user/<int:user_id>", methods=["POST"])
# def delete_user(user_id):
#     if not is_admin():
#         return redirect(url_for("dashboard"))
#     user = db.session.get(User, user_id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#     return redirect(url_for("users"))


# Session-based auth routes moved to auth.py — uncomment in imports and register calls to use.
# Grocery CRUD routes moved to grocery.py — uncomment in imports and register calls to use.
# Helper functions moved to helpers.py — uncomment the import to use.


"""
Helper functions — move to app.py (or uncomment from helpers import ... at the top).

from flask import session
from models import User

def is_loggedin():
    return "user_id" in session

def current_user():
    user_id = session.get("user_id")
    if user_id:
        return User.query.get(user_id)

def is_admin():
    return session.get("role") == "admin"

def is_store_manager():
    return session.get("role") == "store_manager"

def is_allowed_edit():
    return session.get("role") in ("admin", "store_manager")

def login_required():
    return is_loggedin()
"""

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_admin()
    app.run(debug=True, port=5001)
