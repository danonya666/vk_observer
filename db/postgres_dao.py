from datetime import datetime
import psycopg2


class Postgres_dao:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='vk_observer', user='postgres',
                                     password='dancat666danon', host='localhost', port=8090)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

    def select_all(self):
        self.cursor.execute('SELECT * FROM actions')
        self.print_all()

    def print_all(self):
        for row in self.cursor:
            print(row)

    def select_by_id(self, friend_id: int) -> list:
        self.cursor.execute('SELECT * FROM actions WHERE uid = %s', [friend_id])
        actions = []
        for row in self.cursor:
            actions.append(Action(uid=row[0], fn=row[2], ln=row[3], time=row[4], id=row[1]))
        return actions

    def insert_action(self, action=None):
        try:
            self.cursor.execute("INSERT INTO actions(uid, first_name, last_name, time1) VALUES (%s, %s, %s, %s)",
                                (action.uid, action.first_name, action.last_name, action.time))
            self.conn.commit()
        except Exception as e:
            print(e)

    def truncate(self):
        self.cursor.execute('TRUNCATE actions')


class Action:
    def __init__(self, uid, fn, ln, time, id=-1):
        self.uid = uid
        self.id = id
        self.first_name = fn
        self.last_name = ln
        self.time = time

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name + ' ' + str(self.id) + ' ' + datetime.utcfromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(self.time)) + ' @Action'