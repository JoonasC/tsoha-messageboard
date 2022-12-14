from flask import request

from utils.csrf_util import generate_csrf_token
from utils.session_utils import fetch_id_of_logged_in_user_from_session


class CsrfTokenService:
    def __init__(self):
        self.__csrf_tokens_for_users = {}

    def get_csrf_token(self):
        id_of_logged_in_user = fetch_id_of_logged_in_user_from_session()

        if id_of_logged_in_user not in self.__csrf_tokens_for_users:
            self.__csrf_tokens_for_users[id_of_logged_in_user] = generate_csrf_token()

        return self.__csrf_tokens_for_users[id_of_logged_in_user]

    def __rotate_csrf_token(self, id_of_logged_in_user):
        self.__csrf_tokens_for_users[id_of_logged_in_user] = generate_csrf_token()

    def verify_request(self):
        id_of_logged_in_user = fetch_id_of_logged_in_user_from_session()

        if not request.args.get("csrf_token") and "csrf_token" not in request.form:
            return True

        request_csrf_token = \
            request.args.get("csrf_token") if request.args.get("csrf_token") else request.form["csrf_token"]
        if request_csrf_token != self.__csrf_tokens_for_users[id_of_logged_in_user]:
            self.__rotate_csrf_token(id_of_logged_in_user)
            return False

        self.__rotate_csrf_token(id_of_logged_in_user)
        return True

    def clear_csrf_token(self):
        id_of_logged_in_user = fetch_id_of_logged_in_user_from_session()

        if id_of_logged_in_user in self.__csrf_tokens_for_users:
            del self.__csrf_tokens_for_users[id_of_logged_in_user]


csrf_token_service = CsrfTokenService()
