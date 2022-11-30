from flask import render_template

from app import app


@app.route("/")
def home_route():
    return render_template("pages/home.html")
