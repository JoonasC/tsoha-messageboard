from secrets import token_hex


def generate_csrf_token():
    return token_hex(16)
