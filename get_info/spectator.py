import datetime
import time

from db.dal import Dal
from db.postgres_dao import Action
from get_info.observant import Observant
from static.common import update_log
from static.filenames import online


class Spectator:
    def __init__(self, info, logging, friends=0):
        self.info = info
        self.friends = friends
        self.online = dict()
        self.last_online = self.info['last_seen']['time']
        self.info_list = [Observant(info=self.info, friends=self.friends)]
        self.logs = logging
        self.dal = Dal()

    def update_info(self, vk_api):
        self.info = vk_api.users.get(user_id=self.info['uid'], v=1, fields='online, last_seen')[0]
        updated_obses = []
        for i in range(len(self.info_list)):
            # print('info_list = {}'.format(self.info_list))
            if self.info_list[i].update_info(vk_api):
                updated_obses.append(self.info_list[i])
        return updated_obses

    def add_user(self, info, friends):
        self.info_list.append(Observant(info, friends))
        return self.info_list

    def spectate_friends(self, observant):
        for i in observant.friends:
            if 'deactivated' in i:
                pass
            else:
                self.add_user(info=i, friends=None)

    def actions_log(self, actions):
        file = open('actions.log', 'a')
        file.write(
            'At {} {} actions happened ({} {})\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), actions,
                                                         self.info_list[0].info['first_name'],
                                                         self.info_list[0].info['last_name']))
        print(
            'At {} {} actions happened ({} {})\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), actions,
                                                         self.info_list[0].info['first_name'],
                                                         self.info_list[0].info['last_name']))

    def start_polling(self, vk_api):
        fout = open(online, 'a')
        while True:
            try:
                upd_obses = self.update_info(vk_api)
                self.actions_log(len(upd_obses))
                for i in upd_obses:
                    update_log(i)
                    action = Action(i.info['uid'], i.info['first_name'], i.info['last_name'], int(time.time()))
                    print(action)
                    self.dal.insert_action(action)
                diff = []
                for i in self.info_list:
                    diff.append(int(time.time()) - i.info['last_seen']['time'])
                for i in range(len(diff)):
                    fout.close()
                    time.sleep(0.01)
            except Exception as e:
                time.sleep(1)
                print("Slept for 1 seconds. Exception handled")
                print(e)
