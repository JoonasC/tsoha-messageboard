from flask import session

from dto.user import User


def store_logged_in_user_into_session(logged_in_user):
    session["logged_in_user"] = vars(logged_in_user)


def fetch_id_of_logged_in_user_from_session():
    if "logged_in_user" not in session:
        return None

    return session["logged_in_user"]["entity_id"]


def fetch_logged_in_user_from_session():
    if "logged_in_user" not in session:
        return None

    logged_in_user_dict = session["logged_in_user"]
    return User(
        logged_in_user_dict["username"],
        logged_in_user_dict["is_administrator"],
        logged_in_user_dict["entity_id"]
    )


def clear_session():
    del session["logged_in_user"]
