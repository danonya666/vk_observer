class Observant:
    def __init__(self, info, friends):
        self.info = info
        self.friends = friends
        self.last_action = self.info['last_seen']['time']

    def update_info(self, vk_api):
        self.info = vk_api.users.get(user_id=self.info['uid'], v=1, fields='online, last_seen')[0]
        if self.last_action == self.info['last_seen']['time']:
            return False
        else:
            self.last_action = self.info['last_seen']['time']
            return True

    def toString(self):
        return str(self.info)
