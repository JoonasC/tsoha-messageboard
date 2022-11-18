from config.db import db_conn
from dto.topic import Topic


class TopicService:
    def __init__(self, db=db_conn):
        self._db = db

    def create_topic(self, topic):
        self._db.session.execute(
            "INSERT INTO topics (name) VALUES (:name)",
            {"name": topic.name}
        )
        self._db.session.commit()

    def get_all_topics(self):
        query_result = self._db.session.execute("SELECT id, name FROM topics")
        topics = query_result.fetchall()

        return list(map(lambda topic: Topic(topic.name, topic.id), topics))

    def get_topic(self, entity_id):
        query_result = self._db.session.execute(
            "SELECT id, name FROM topics WHERE id=:id",
            {"id": entity_id}
        )
        topic = query_result.fetchone()

        if topic:
            return Topic(topic.name, topic.id)
        else:
            return None

    def update_topic(self, topic):
        self._db.session.execute(
            "UPDATE topics SET name=:name WHERE id=:id",
            {"name": topic.name, "id": topic.entity_id}
        )
        self._db.session.commit()

    def delete_topic(self, entity_id):
        self._db.session.execute(
            "DELETE FROM topics WHERE id=:id",
            {"id": entity_id}
        )
        self._db.session.commit()
