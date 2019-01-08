import time

import datetime

from Spectator import to_integer, Spectator
from analyzer import Analyzer
# from main import vk_api
import vk.utils

from keys import session_key
from obervant import Observant
from postgres_dao import Postgres_dao

session = vk.Session(session_key)
vk_api = vk.API(session)
anna_zolotareva_id = 324643349
matvey_shilkin_id = 166301900
my_id = 159848901
rostislav_losev_id = 4748474
vlad_chersvov_id = 138606349
kupl_alena_id = 77558528
anton_sekerin_id = 339999710
chepush_andrew_id = 249838527
golod_id = 129010287
vasiliev_id = 53801999
sofia_id = 392847560
id = my_id
user = vk_api.users.get(user_id=id, v=1, fields='online, last_seen')
friends = vk_api.friends.get(user_id=id, order='name', v=1, fields='domain, online, last_seen')
# print(user[0]['online'])
print(user[0]['last_name'] + ' ' + user[0]['first_name'])
# print(friends[0])
print('last seen by the start of script')
print(datetime.datetime.fromtimestamp(user[0]['last_seen']['time']).strftime('%d-%m-%Y %H:%M'))

spec = Spectator(info=user[0], logging=True)
# print('last_online = ' + str(spec.last_online))
"""while True:
    fout = open('online.log', 'a')
    try:
        now_int = to_integer(datetime.datetime.now())
        spec.update_info(vk_api)
        now = datetime.datetime.now()
        last_seen = spec.info['last_seen']
        # print(last_seen['time'])
        diff = int(time.time()) - last_seen['time']
        if diff < 5:
            log_string = str(spec.info['first_name'] + ':' + spec.info['last_name'] + ':' + str(
                datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(
                datetime.datetime.now().second) + ':' + str(last_seen['platform']) + '\n')
            print(log_string)
            winsound.MessageBeep(winsound.MB_ICONHAND)
            fout.write(log_string)
            time.sleep(5)
        # print(spec.info['online'])
        spec.online[now_int] = spec.info['online']
        # print(spec.online)
        # print(to_integer(datetime.datetime.now()))
        fout.close()
        time.sleep(3)
    except requests.exceptions.Timeout:
        time.sleep(4)
        session = vk.Session('e0fe5598e0fe5598e0fe559812e099952cee0fee0fe5598bcda80a4b93b43bb2719c0df')
        vk_api = vk.API(session)
        print('Timeout error was handled')


"""
spec.spectate_friends(Observant(user[0], friends))
analyzer = Analyzer(spec)
print(analyzer.friends_ids)
pd = Postgres_dao()
for friend_id in analyzer.friends_ids:
    print('fid = {}'.format(friend_id))
    pd.select_by_id(friend_id)
    pd.print_all()
