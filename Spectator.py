import datetime
import time

import winsound

from obervant import Observant
from postgres_dao import Postgres_dao, Action


def to_integer(dt_time):
    return 100000000 * dt_time.year + 1000000 * dt_time.month + 10000 * dt_time.day + 100 * dt_time.hour + dt_time.minute


def format_seconds(seconds):
    minutes = seconds // 60
    seconds = seconds - minutes * 60
    hours = minutes // 60
    minutes = minutes - hours * 60
    days = hours // 24
    hours = hours - days * 24
    result = {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds}
    return result


def update_log(obs):
    log_string = str(
        obs.info['first_name'] + ':' + obs.info['last_name'] + ':' + str(
            datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(
            datetime.datetime.now().second) + ':' + str(
            obs.info['last_seen']['platform']) + '\n')
    print(log_string)
    # winsound.MessageBeep(winsound.MB_ICONHAND)
    fout = open('online.log', 'a')
    fout.write(log_string)


class Spectator:
    def __init__(self, info, logging, friends=0):
        self.info = info
        self.friends = friends
        self.online = dict()
        self.last_online = self.info['last_seen']['time']
        self.info_list = [Observant(info=self.info, friends=self.friends)]
        self.logs = logging
        self.dao = Postgres_dao()

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
        fout = open('online.log', 'a')
        while True:
            try:
                now_int = to_integer(datetime.datetime.now())
                upd_obses = self.update_info(vk_api)
                self.actions_log(len(upd_obses))
                for i in upd_obses:
                    update_log(i)
                    print('i: {}', i.info)
                    action = Action(i.info['uid'], i.info['first_name'], i.info['last_name'], int(time.time()))
                    print(action)
                    self.dao.insert_action(action)
                now = datetime.datetime.now()
                last_seen = self.info['last_seen']
                # diff = int(time.time()) - last_seen['time']
                diff = []
                for i in self.info_list:
                    diff.append(int(time.time()) - i.info['last_seen']['time'])
                for i in range(len(diff)):
                    formatted_diff = format_seconds(diff[i])
                    print('{} {} last action {} days {} hours {} minutes {} seconds ago'.format(
                        self.info_list[i].info['first_name'], self.info_list[i].info['last_name'],
                        formatted_diff['days'],
                        formatted_diff['hours'], formatted_diff['minutes'], formatted_diff['seconds']))
                    """
                    if diff[i] < 5:
                        log_string = str(
                            self.info_list[i].info['first_name'] + ':' + self.info_list[i].info['last_name'] + ':' + str(
                                datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(
                                datetime.datetime.now().second) + ':' + str(
                                self.info_list[i].info['last_seen']['platform']) + '\n')
                        print(log_string)
                        winsound.MessageBeep(winsound.MB_ICONHAND)
                        fout = open('online.log', 'a')
                        fout.write(log_string)
                        # time.sleep(5)
                    """
                    # print(spec.info['online'])
                    # self.online[now_int] = self.info['online']
                    # print(spec.online)
                    # print(to_integer(datetime.datetime.now()))
                    fout.close()
                    time.sleep(0.01)
            except Exception as e:
                time.sleep(1)
                print("Slept for 1 seconds. Exception handled")
                print(e)
#    [365][24][60]
