from flask import Flask, redirect, render_template, request, url_for

from models import GroceryItem, Purchase, User, db, db_init

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bootcamp.db"

db_init(app)


# default location for our url
@app.route("/")
def home():
    return render_template("homepage.html")


# list examples
# mylist = [ a, b, c]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # check for correct credentials later on
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            print(user.username, user.password)
            return redirect(url_for("dashboard", username=username))
        else:
            return render_template("login.html")

        # if credentials are incorrect, render the login form again
        # return render_template("login.html")
    return render_template("login.html")


# faulty code
@app.route("/dashboard", methods=["GET"])
def dashboard():
    username = request.args.get("username")
    print(username)
    return render_template("dashboard.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


# TODO:
# 1 create a page to show all users
# 2. create endpoint/route/handler to show all the users
#
@app.route("/users")
def users():
    all_users = User.query.all()
    return render_template("allusers.html", users=all_users)


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


if __name__ == "__main__":
    app.run(debug=True, port=5001)
