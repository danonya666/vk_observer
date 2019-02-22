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

    def some_period_activity_by_hours(self, period, actions=None) -> dict:  # Period in hours
        """How many actions were made by a user during some period"""
        hour_activity = dict.fromkeys([i for i in range(period)], 0)
        if actions is None:
            actions = self.myself.actions
        for action in actions:
            dt_time = datetime.fromtimestamp(action.time)
            diff = datetime.now() - dt_time
            hour_diff = int(diff.total_seconds() / 3600)
            if hour_diff < period:
                hour_activity[hour_diff] += 1
        return hour_activity

    def week_activity(self, actions=None) -> list:
        pass

    def month_activity(self, actions: list) -> list:
        pass

    def some_period_activity_by_days(self, period, actions=None) -> list:
        day_activity = dict.fromkeys([i for i in range(period)], 0)
        if actions is None:
            actions = self.myself.actions
        for action in actions:
            dt_time = datetime.fromtimestamp(action.time)
            today = datetime.today()
            diff = datetime(today.year, today.month, today.day + 1, 0, 0) - dt_time
            day_diff = int(diff.total_seconds() / 86400)
            if day_diff < period:
                day_activity[day_diff] += 1
        return day_activity
