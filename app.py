from flask import Flask, render_template, request

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

        return render_template("dashboard.html", username=username, password=password)
    return render_template("login.html")


# faulty code
@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if request.method == "POST":
        return render_template("dashboard.html")
    return render_template("dashboard.html", username=request.args.get("username"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
