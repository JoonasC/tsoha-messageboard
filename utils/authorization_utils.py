from utils.session_utils import fetch_logged_in_user_from_session


def user_has_required_privileges(required_user_id, allow_administrator=True):
    logged_in_user = fetch_logged_in_user_from_session()

    return logged_in_user.entity_id == required_user_id or (allow_administrator and logged_in_user.is_administrator)


def user_is_administrator():
    return fetch_logged_in_user_from_session().is_administrator
