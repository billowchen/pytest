import pymongo
from qute_core.configparserHandler import ConfigparserHandler
from qute_core.logHandler import LogHandler


class MongoHandler(object):
    def __init__(self, config_file, key):
        self.config = ConfigparserHandler(config_file)
        self.host = self.config.get_data(key, 'host')
        self.port = self.config.get_data(key, 'port')
        self.user = self.config.get_data(key, 'username')
        self.psw = self.config.get_data(key, 'psw')
        self.logging = LogHandler().log()
        try:
            self.client = pymongo.MongoClient(self.host, int(self.port))
            if self.user and self.psw:
                db = self.client.admin
                db.authenticate(self.user, self.psw)
        except Exception as e:
            self.logging.exception(e)
            self.logging.info('{} mongo连接失败'.format(self.host))
        else:
            self.logging.info('{} mongo连接成功'.format(self.host))
        finally:
            exit() if not self.client else ''

    def find(self, my_db, set, dic, limit=None, skip=None, sort_key=None, order=-1):
        if sort_key:
            data = self.client[my_db][set].find(dic).sort(sort_key, order)
        else:
            data = self.client[my_db][set].find(dic)
        if skip:
            data = data.skip(skip)

        if limit:
            data = data.limit(limit)
        data_list = [i for i in data] if data else ''
        return data_list

    def insert(self, my_db, set, data):
        if isinstance(data, list):
            self.client[my_db][set].insert_many(data)
        elif isinstance(data, dict):
            self.client[my_db][set].insert_one(data)
        else:
            self.client[my_db][set].insert(data)

    def update(self, my_db, set, dic, newdic):
        self.client[my_db][set].update(dic, newdic)

    def remove(self, my_db, set, dic):
        self.client[my_db][set].remove(dic)
