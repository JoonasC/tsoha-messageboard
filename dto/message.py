class Message:
    def __init__(
            self,
            content,
            message_chain_entity_id,
            user_entity_id,
            replied_message_entity_id=None,
            entity_id=None
    ):
        self.content = content
        self.message_chain_entity_id = message_chain_entity_id
        self.user_entity_id = user_entity_id
        self.replied_message_entity_id = replied_message_entity_id
        self.entity_id = entity_id
