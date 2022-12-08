from flask import url_for, redirect, render_template, request, session

from app import app
from dto.ui_error import UiError
from services.user_service import user_service


@app.before_request
def verify_user_is_logged_in():
    if "logged_in_user" not in session and request.endpoint not in ["login_route", "login_submit_route", "static"]:
        return redirect(url_for("login_route"))


@app.get("/")
def home_route():
    return render_template("page/home.html")


@app.get("/login")
def login_route():
    return render_template("page/login.html")


@app.post("/login")
def login_submit_route():
    username = request.form["username"]
    password = request.form["password"]

    if not username:
        return render_template(
            "page/login.html",
            error=UiError("This field is required", "username_input"),
            form_values={
                "username_input": username,
                "password_input": password
            }
        )
    if not password:
        return render_template(
            "page/login.html",
            error=UiError("This field is required", "password_input"),
            form_values={
                "username_input": username,
                "password_input": password
            }
        )

    if user_service.verify_user_password(username, password):
        session["logged_in_user"] = user_service.get_user_by_username(username)
        return redirect(url_for("home_route"))
    else:
        return render_template(
            "page/login.html",
            error=UiError("Wrong username or password"),
            form_values={
                "username_input": username,
                "password_input": password
            }
        )
