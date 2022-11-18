class MessageChain:
    def __init__(self, name, topic_entity_id, user_entity_id, entity_id=None):
        self.name = name
        self.topic_entity_id = topic_entity_id
        self.user_entity_id = user_entity_id
        self.entity_id = entity_id
