from config.db import db_conn
from dto.message import Message


class MessageService:
    def __init__(self, db=db_conn):
        self._db = db

    def create_message(self, message):
        self._db.session.execute(
            "INSERT INTO messages (content, message_chain_id, user_id) VALUES (:content, :message_chain_id, :user_id)",
            {
                "content": message.content,
                "message_chain_id": message.message_chain_entity_id,
                "user_id": message.user_entity_id
            }
        )
        self._db.session.commit()

    def get_all_messages_in_message_chain(self, message_chain_entity_id):
        query_result = self._db.session.execute(
            "SELECT id, content, message_chain_id, user_id FROM messages WHERE message_chain_id=:message_chain_id",
            {"message_chain_id": message_chain_entity_id}
        )
        messages = query_result.fetchall()

        return list(
            map(
                lambda message: Message(message.content, message.message_chain_id, message.user_id, message.id),
                messages
            )
        )

    def get_message(self, entity_id):
        query_result = self._db.session.execute(
            "SELECT id, content, message_chain_id, user_id FROM messages WHERE id=:id",
            {"id": entity_id}
        )
        message = query_result.fetchone()

        if message:
            return Message(message.content, message.message_chain_id, message.user_id, message.id)
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
