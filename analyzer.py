class Person:
    def __init__(self, id):
        self.id = id
        self.actions = []
        self.actions_rate = 0


class Analyzer:
    def __init__(self, spec):
        self.dao = spec.dao
        self.myself = Person(spec.info_list[0].info['uid'])
        self.friends_ids = []
        for friend in spec.info_list:
            self.friends_ids.append(friend.info['uid'])


