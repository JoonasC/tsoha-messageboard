from config.db import db_conn
from dto.message_chain import MessageChain


class MessageChainService:
    def __init__(self, db=db_conn):
        self._db = db

    def create_message_chain(self, message_chain):
        self._db.session.execute(
            "INSERT INTO message_chains (name, topic_id, user_id) VALUES (:name, :topic_id, :user_id)",
            {
                "name": message_chain.name,
                "topic_id": message_chain.topic_entity_id,
                "user_id": message_chain.user_entity_id
            }
        )
        self._db.session.commit()

    def get_all_message_chains_in_topic(self, topic_entity_id):
        query_result = self._db.session.execute(
            "SELECT id, name, topic_id, user_id FROM message_chains WHERE topic_id=:topic_id",
            {"topic_id": topic_entity_id}
        )
        message_chains = query_result.fetchall()

        return list(
            map(
                lambda message_chain: MessageChain(
                    message_chain.name,
                    message_chain.topic_id,
                    message_chain.user_id,
                    message_chain.id
                ),
                message_chains
            )
        )

    def get_message_chain(self, entity_id):
        query_result = self._db.session.execute(
            "SELECT id, name, topic_id, user_id FROM message_chains WHERE id=:id",
            {"id": entity_id}
        )
        message_chain = query_result.fetchone()

        if message_chain:
            return MessageChain(message_chain.name, message_chain.topic_id, message_chain.user_id, message_chain.id)
        else:
            return None

    def update_message_chain(self, message_chain):
        self._db.session.execute(
            "UPDATE message_chains SET name=:name WHERE id=:id",
            {"name": message_chain.name, "id": message_chain.entity_id}
        )
        self._db.session.commit()

    def delete_message_chain(self, entity_id):
        self._db.session.execute(
            "DELETE FROM message_chains WHERE id=:id",
            {"id": entity_id}
        )
        self._db.session.commit()
