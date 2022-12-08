from werkzeug.security import check_password_hash, generate_password_hash

from config.db import db_conn
from dto.user import User


class UserService:
    def __init__(self, db=db_conn):
        self._db = db

    def create_user(self, user, password):
        hashed_password = generate_password_hash(password)
        self._db.session.execute(
            """INSERT INTO users (username, password_hash, is_administrator)
            VALUES (:username, :password_hash, :is_administrator)""",
            {"username": user.username, "password_hash": hashed_password, "is_administrator": user.is_administrator}
        )
        self._db.session.commit()

    def get_all_users(self):
        query_result = self._db.session.execute("SELECT id, username, is_administrator FROM users")
        users = query_result.fetchall()

        return list(map(lambda user: User(user.username, user.is_administrator, user.id), users))

    def get_user(self, entity_id):
        query_result = self._db.session.execute(
            "SELECT id, username, is_administrator FROM users WHERE id=:id",
            {"id": entity_id}
        )
        user = query_result.fetchone()

        if user:
            return User(user.username, user.is_administrator, user.id)
        else:
            return None

    def get_user_by_username(self, username):
        query_result = self._db.session.execute(
            "SELECT id, username, is_administrator FROM users WHERE username=:username",
            {"username": username}
        )
        user = query_result.fetchone()

        if user:
            return User(user.username, user.is_administrator, user.id)
        else:
            return None

    def update_user(self, user, password=None):
        self._db.session.execute(
            "UPDATE users SET username=:username, is_administrator=:is_administrator WHERE id=:id",
            {"username": user.username, "is_administrator": user.is_administrator, "id": user.entity_id}
        )
        if password:
            hashed_password = generate_password_hash(password)
            self._db.session.execute(
                "UPDATE users SET password_hash=:password_hash WHERE id=:id",
                {"password_hash": hashed_password, "id": user.entity_id}
            )
        self._db.session.commit()

    def delete_user(self, entity_id):
        self._db.session.execute(
            "DELETE FROM users WHERE id=:id",
            {"id": entity_id}
        )
        self._db.session.commit()

    def verify_user_password(self, username, password):
        query_result = self._db.session.execute(
            "SELECT password_hash FROM users WHERE username=:username",
            {"username": username}
        )
        row = query_result.fetchone()

        if not row:
            return False

        return check_password_hash(row.password_hash, password)


user_service = UserService()
