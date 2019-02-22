from db.postgres_dao import Postgres_dao


class Dal:
    def __init__(self):
        self.dao = Postgres_dao()

    def get_user_actions(self, id: int) -> list:
        info = self.dao.select_by_id(id)
        return info

    def insert_action(self, action=None):
        self.dao.insert_action(action)
