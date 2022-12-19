from re import search

from flask import url_for, abort, redirect, render_template, request, session
from sqlalchemy.exc import IntegrityError

from app import app
from dto.message import Message
from dto.message_chain import MessageChain
from dto.ui_error import UiError
from dto.user import User
from services.csrf_token_service import csrf_token_service
from services.message_chain_service import message_chain_service
from services.message_service import message_service
from services.topic_service import topic_service
from services.user_service import user_service
from utils.authorization_utils import user_has_required_privileges
from utils.session_utils import fetch_id_of_logged_in_user_from_session, store_logged_in_user_into_session


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
    if not csrf_token_service.verify_request():
        abort(403)

    if request.args.get("topic_name_search_filter") and request.args.get("topic_name_search_filter") != "":
        topic_name_search_filter = request.args.get("topic_name_search_filter")
        topics = topic_service.search_for_topics_by_name(topic_name_search_filter)
    else:
        topic_name_search_filter = ""
        topics = topic_service.get_all_topics()

    return render_template(
        "page/home.html",
        topics=topics,
        form_values={"topic_name_search_input": topic_name_search_filter},
        csrf_token=csrf_token_service.get_csrf_token()
    )


@app.get("/topic/<int:topic_id>")
def message_chain_list_route(topic_id):
    if not csrf_token_service.verify_request():
        abort(403)

    if request.args.get("message_chain_name_search_filter") \
            and request.args.get("message_chain_name_search_filter") != "":
        message_chain_name_search_filter = request.args.get("message_chain_name_search_filter")
        message_chains = message_chain_service.search_for_message_chains_by_name_in_topic(
            topic_id,
            message_chain_name_search_filter
        )
    else:
        message_chain_name_search_filter = ""
        message_chains = message_chain_service.get_all_message_chains_in_topic(topic_id)

    return render_template(
        "page/message_chain_list.html",
        topic_id=topic_id,
        message_chains=message_chains,
        form_values={"message_chain_name_search_input": message_chain_name_search_filter},
        csrf_token=csrf_token_service.get_csrf_token()
    )


@app.get("/topic/<int:topic_id>/message_chain/new")
def create_new_message_chain_route(topic_id):
    return render_template(
        "page/create_new_message_chain.html",
        topic_id=topic_id,
        csrf_token=csrf_token_service.get_csrf_token()
    )


@app.post("/topic/<int:topic_id>/message_chain/new")
def create_new_message_chain_submit_route(topic_id):
    if not csrf_token_service.verify_request():
        abort(403)

    name = request.form["name"]

    if not name:
        return render_template(
            "page/create_new_message_chain.html",
            topic_id=topic_id,
            error=UiError("This field is required", "name_input"),
            form_values={
                "name_input": name
            },
            csrf_token=csrf_token_service.get_csrf_token()
        )

    try:
        message_chain_service.create_message_chain(
            MessageChain(name, topic_id, fetch_id_of_logged_in_user_from_session())
        )
    except IntegrityError as exc:
        if "name" in exc.orig.args[0] and "already exists" in exc.orig.args[0]:
            return render_template(
                "page/create_new_message_chain.html",
                topic_id=topic_id,
                error=UiError("A message chain with this name already exists", "name_input"),
                form_values={
                    "name_input": name
                },
                csrf_token=csrf_token_service.get_csrf_token()
            )

        raise exc

    return redirect(url_for("message_chain_list_route", topic_id=topic_id))


@app.get("/message_chain/<int:message_chain_id>/edit")
def edit_message_chain_route(message_chain_id):
    message_chain = message_chain_service.get_message_chain(message_chain_id)

    if not user_has_required_privileges(message_chain.user_entity_id, False):
        abort(403)

    return render_template(
        "page/edit_message_chain.html",
        message_chain_id=message_chain_id,
        topic_id=message_chain.topic_entity_id,
        form_values={
            "name_input": message_chain.name
        },
        csrf_token=csrf_token_service.get_csrf_token()
    )


@app.post("/message_chain/<int:message_chain_id>/edit")
def edit_message_chain_submit_route(message_chain_id):
    message_chain = message_chain_service.get_message_chain(message_chain_id)

    if not user_has_required_privileges(message_chain.user_entity_id, False):
        abort(403)
    if not csrf_token_service.verify_request():
        abort(403)

    name = request.form["name"]

    if not name:
        return render_template(
            "page/edit_message_chain.html",
            message_chain_id=message_chain_id,
            topic_id=message_chain.topic_entity_id,
            error=UiError("This field is required", "name_input"),
            form_values={
                "name_input": name
            },
            csrf_token=csrf_token_service.get_csrf_token()
        )

    try:
        message_chain_service.update_message_chain(
            MessageChain(name, message_chain.topic_entity_id, message_chain.user_entity_id, message_chain_id)
        )
    except IntegrityError as exc:
        if "name" in exc.orig.args[0] and "already exists" in exc.orig.args[0]:
            return render_template(
                "page/edit_message_chain.html",
                message_chain_id=message_chain_id,
                topic_id=message_chain.topic_entity_id,
                error=UiError("A message chain with this name already exists", "name_input"),
                form_values={
                    "name_input": name
                },
                csrf_token=csrf_token_service.get_csrf_token()
            )

        raise exc

    return redirect(url_for("message_chain_list_route", topic_id=message_chain.topic_entity_id))


@app.post("/message_chain/<int:message_chain_id>/delete")
def delete_message_chain_route(message_chain_id):
    message_chain = message_chain_service.get_message_chain(message_chain_id)

    if not user_has_required_privileges(message_chain.user_entity_id):
        abort(403)

    message_chain_service.delete_message_chain(message_chain_id)

    return redirect(url_for("message_chain_list_route", topic_id=message_chain.topic_entity_id))


@app.get("/message_chain/<int:message_chain_id>/view")
def view_message_chain_route(message_chain_id):
    message_chain = message_chain_service.get_message_chain(message_chain_id)

    messages_and_associated_users = \
        message_service.get_all_messages_and_associated_users_in_message_chain(message_chain_id)

    messages = {}
    users = {}

    for message_and_associated_user in messages_and_associated_users:
        messages[message_and_associated_user[0].entity_id] = message_and_associated_user[0]

        if message_and_associated_user[1].entity_id not in users:
            users[message_and_associated_user[1].entity_id] = message_and_associated_user[1]

    return render_template(
        "page/view_message_chain.html",
        message_chain=message_chain,
        messages=messages,
        users=users
    )


@app.get("/message_chain/<int:message_chain_id>/reply")
@app.get("/message_chain/<int:message_chain_id>/reply/<int:replied_message_id>")
def reply_to_message_chain_route(message_chain_id, replied_message_id=None):
    if replied_message_id and not message_service.get_message(replied_message_id):
        abort(500)

    return render_template(
        "page/reply_to_message_chain.html",
        message_chain_id=message_chain_id,
        replied_message_id=replied_message_id,
        csrf_token=csrf_token_service.get_csrf_token()
    )


@app.post("/message_chain/<int:message_chain_id>/reply")
@app.post("/message_chain/<int:message_chain_id>/reply/<int:replied_message_id>")
def reply_to_message_chain_submit_route(message_chain_id, replied_message_id=None):
    if replied_message_id and not message_service.get_message(replied_message_id):
        abort(500)

    if not csrf_token_service.verify_request():
        abort(403)

    content = request.form["content"]

    if not content:
        return render_template(
            "page/reply_to_message_chain.html",
            message_chain_id=message_chain_id,
            replied_message_id=replied_message_id,
            error=UiError("This field is required", "content_input"),
            form_values={
                "content_input": content
            },
            csrf_token=csrf_token_service.get_csrf_token()
        )

    message_service.create_message(
        Message(content, message_chain_id, fetch_id_of_logged_in_user_from_session(), replied_message_id)
    )

    return redirect(url_for("view_message_chain_route", message_chain_id=message_chain_id))


@app.post("/message/<int:message_id>/delete")
def delete_message_route(message_id):
    message = message_service.get_message(message_id)

    if not user_has_required_privileges(message.user_entity_id):
        abort(403)

    message_service.delete_message(message_id)

    return redirect(url_for("view_message_chain_route", message_chain_id=message.message_chain_entity_id))


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
        if "username" in exc.orig.args[0] and "already exists" in exc.orig.args[0]:
            return render_template(
                "page/register.html",
                error=UiError("This username is already taken", "username_input"),
                form_values={
                    "username_input": username,
                    "password_input": password
                }
            )

        raise exc

    return redirect(url_for("login_route"))
