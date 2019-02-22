import datetime
import vk.utils
from db.postgres_dao import Postgres_dao
from get_info.observant import Observant
from get_info.spectator import Spectator
from processing.analyzer import Analyzer
from static.keys import *

session = vk.Session(session_key)
vk_api = vk.API(session)
id = my_id
user = vk_api.users.get(user_id=id, v=1, fields='online, last_seen')
friends = vk_api.friends.get(user_id=id, order='name', v=1, fields='domain, online, last_seen')
print(user[0]['last_name'] + ' ' + user[0]['first_name'])
print('last seen by the start of script')
print(datetime.datetime.fromtimestamp(user[0]['last_seen']['time']).strftime('%d-%m-%Y %H:%M'))
spec = Spectator(info=user[0], logging=True)
spec.spectate_friends(Observant(user[0], friends))
analyzer = Analyzer(spec)
pd = Postgres_dao()
print("Connected to dao {}".format(pd))
print("before select_all")
a = analyzer.get_friends_actions()
for action in a:
    print(action)
print(analyzer.some_period_activity_by_hours(3000))
