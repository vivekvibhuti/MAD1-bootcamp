from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


# default location for our url
@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # check for correct credentials later on
        #
        #
        return redirect(url_for("dashboard", username=username))

        # if credentials are incorrect, render the login form again
        # return render_template("login.html")
    return render_template("login.html")


# faulty code
@app.route("/dashboard", methods=["GET"])
def dashboard():
    username = request.args.get("username")
    print(username)
    return render_template("dashboard.html", username=username)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
