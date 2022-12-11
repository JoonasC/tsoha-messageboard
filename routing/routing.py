from re import search

from flask import url_for, redirect, render_template, request, session
from sqlalchemy.exc import IntegrityError

from app import app
from dto.ui_error import UiError
from dto.user import User
from services.user_service import user_service
from utils.session_utils import store_logged_in_user_into_session


@app.before_request
def verify_user_is_logged_in():
    if "logged_in_user" not in session and request.endpoint not in [
        "login_route",
        "login_submit_route",
        "register_route",
        "register_submit_route",
        "static"
    ]:
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
        store_logged_in_user_into_session(user_service.get_user_by_username(username))
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


@app.get("/register")
def register_route():
    return render_template("page/register.html")


@app.post("/register")
def register_submit_route():
    username = request.form["username"]
    password = request.form["password"]

    if not username:
        return render_template(
            "page/register.html",
            error=UiError("This field is required", "username_input"),
            form_values={
                "username_input": username,
                "password_input": password
            }
        )
    if not password:
        return render_template(
            "page/register.html",
            error=UiError("This field is required", "password_input"),
            form_values={
                "username_input": username,
                "password_input": password
            }
        )
    if len(password) < 5:
        return render_template(
            "page/register.html",
            error=UiError("The password should be at least five characters long", "password_input"),
            form_values={
                "username_input": username,
                "password_input": password
            }
        )
    if search(r"\w", password) is None or search(r"\W", password) is None:
        return render_template(
            "page/register.html",
            error=UiError(
                "The password should contain at least one letter, number and special character",
                "password_input"
            ),
            form_values={
                "username_input": username,
                "password_input": password
            }
        )

    try:
        user_service.create_user(User(username, False), password)
    except IntegrityError as exc:
        raise exc

    return redirect(url_for("login_route"))
