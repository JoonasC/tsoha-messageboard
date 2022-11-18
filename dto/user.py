class User:
    def __init__(self, username, is_administrator, entity_id=None):
        self.username = username
        self.is_administrator = is_administrator
        self.entity_id = entity_id
