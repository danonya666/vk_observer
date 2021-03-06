from postgres_dao import Action


class Person:
    def __init__(self, id):
        self.id = id
        self.actions = []
        self.actions_rate = 0


class Analyzer:
    """
    A class for analyzing friends' data. Connects to DB through DAO, gets info, analyzes.
    """

    def __init__(self, spec):
        self.dao = spec.dao
        self.myself = Person(spec.info_list[0].info['uid'])
        self.friends_ids = []
        for friend in spec.info_list:
            self.friends_ids.append(friend.info['uid'])

    def get_friends_actions(self):
        actions = []
        for friend in self.friends_ids:
            actions += self.dao.select_by_id(friend)
        return actions
