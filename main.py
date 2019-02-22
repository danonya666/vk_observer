import vk.utils
from get_info.spectator import *
from static.keys import session_key
from static.keys import *
session = vk.Session(session_key)
vk_api = vk.API(session)
id = anna_zolotareva_id
user = vk_api.users.get(user_id=id, v=1, fields='online, last_seen')
friends = vk_api.friends.get(user_id=id, order='name', v=1, fields='domain, online, last_seen')
print(user[0]['last_name'] + ' ' + user[0]['first_name'])
print('last seen by the start of script')
print(datetime.datetime.fromtimestamp(user[0]['last_seen']['time']).strftime('%d-%m-%Y %H:%M'))
spec = Spectator(info=user[0], logging=True)
spec.spectate_friends(Observant(user[0], friends))
print(spec)
spec.start_polling(vk_api)
