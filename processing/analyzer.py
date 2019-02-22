from datetime import datetime


class Person:
    def __init__(self, id):
        self.id = id
        self.actions = []


class Analyzer:
    """
    A class for analyzing friends' data. Connects to DB through DAO, gets info, analyzes.
    """

    def __init__(self, spec):
        self.dal = spec.dal
        self.myself = Person(spec.info_list[0].info['uid'])
        self.friends_ids = []
        for friend in spec.info_list:
            self.friends_ids.append(friend.info['uid'])
        self.initialize_actions()

    def initialize_actions(self):
        self.myself.actions = self.dal.get_user_actions(self.myself.id)

    def get_friends_actions(self) -> list:
        actions = []
        for friend in self.friends_ids:
            actions += self.dal.get_user_actions(friend)
        return actions

    def day_activity(self, actions=None) -> dict:
        hour_activity = dict.fromkeys([i for i in range(24)], 0)
        if actions is None:
            actions = self.myself.actions
        for action in actions:
            dt_time = datetime.fromtimestamp(action.time)
            if dt_time.date() == datetime.today().date():
                hour_activity[dt_time.hour] += 1
        return hour_activity

    def week_activity(self, actions: list) -> list:
        pass

    def month_activity(self, actions: list) -> list:
        pass

    def some_period_activity(self, actions: list, period) -> list:
        pass

# def action_time(action):
