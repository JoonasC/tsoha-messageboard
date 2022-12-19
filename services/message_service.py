from config.db import db_conn
from dto.message import Message
from dto.user import User


class MessageService:
    def __init__(self, db=db_conn):
        self._db = db

    def create_message(self, message):
        message_insert_query_result = self._db.session.execute(
            """INSERT INTO messages (content, message_chain_id, user_id) VALUES (:content, :message_chain_id, :user_id)
            RETURNING id""",
            {
                "content": message.content,
                "message_chain_id": message.message_chain_entity_id,
                "user_id": message.user_entity_id
            }
        )
        if message.replied_message_entity_id:
            inserted_message_id = message_insert_query_result.fetchone()[0]
            self._db.session.execute(
                """INSERT INTO message_replies (message_id, replied_message_id)
                VALUES (:message_id, :replied_message_id)""",
                {"message_id": inserted_message_id, "replied_message_id": message.replied_message_entity_id}
            )
        self._db.session.commit()

    def get_all_messages_in_message_chain(self, message_chain_entity_id):
        query_result = self._db.session.execute(
            """SELECT messages.id, messages.content, messages.message_chain_id, messages.user_id,
            message_replies.replied_message_id
            FROM messages LEFT JOIN message_replies ON messages.id=message_replies.message_id
            WHERE messages.message_chain_id=:message_chain_id ORDER BY messages.id""",
            {"message_chain_id": message_chain_entity_id}
        )
        messages = query_result.fetchall()

        return list(
            map(
                lambda message: Message(
                    message.content,
                    message.message_chain_id,
                    message.user_id,
                    message.replied_message_id,
                    message.id
                ),
                messages
            )
        )

    def get_all_messages_and_associated_users_in_message_chain(self, message_chain_entity_id):
        query_result = self._db.session.execute(
            """SELECT messages.id, messages.content, messages.message_chain_id, messages.user_id,
            message_replies.replied_message_id, users.username, users.is_administrator
            FROM messages LEFT JOIN message_replies ON messages.id=message_replies.message_id
            INNER JOIN users ON messages.user_id=users.id WHERE messages.message_chain_id=:message_chain_id
            ORDER BY messages.id""",
            {"message_chain_id": message_chain_entity_id}
        )
        messages_and_associated_users = query_result.fetchall()

        return list(
            map(
                lambda message_and_associated_user: (
                    Message(
                        message_and_associated_user.content,
                        message_and_associated_user.message_chain_id,
                        message_and_associated_user.user_id,
                        message_and_associated_user.replied_message_id,
                        message_and_associated_user.id
                    ),
                    User(
                        message_and_associated_user.username,
                        message_and_associated_user.is_administrator,
                        message_and_associated_user.user_id
                    )
                ),
                messages_and_associated_users
            )
        )

    def get_message(self, entity_id):
        query_result = self._db.session.execute(
            """SELECT messages.id, messages.content, messages.message_chain_id, messages.user_id,
            message_replies.replied_message_id
            FROM messages LEFT JOIN message_replies ON messages.id=message_replies.message_id
            WHERE messages.id=:id""",
            {"id": entity_id}
        )
        message = query_result.fetchone()

        if message:
            return Message(
                message.content,
                message.message_chain_id,
                message.user_id,
                message.replied_message_id,
                message.id
            )
        else:
            return None

    def update_message(self, message):
        self._db.session.execute(
            "UPDATE messages SET content=:content WHERE id=:id",
            {"content": message.content, "id": message.entity_id}
        )
        self._db.session.commit()

    def delete_message(self, entity_id):
        self._db.session.execute(
            "DELETE FROM messages WHERE id=:id",
            {"id": entity_id}
        )
        self._db.session.commit()


message_service = MessageService()
