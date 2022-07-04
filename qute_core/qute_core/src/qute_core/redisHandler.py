import redis
from qute_core.logHandler import LogHandler
from qute_core.configparserHandler import ConfigparserHandler


class RedisHandler(object):

    def __init__(self, config_file, key):
        self.config = ConfigparserHandler(config_file)
        self.host = self.config.get_data(key, 'host')
        self.psw = self.config.get_data(key, 'psw')
        self.port = self.config.get_data(key, 'port')
        self.db = self.config.get_data(key, 'db')
        self.redis = None
        self.logging = LogHandler().log()
        self.connect_redis()

    def connect_redis(self):
        try:
            if self.psw:
                pool = redis.ConnectionPool(host=self.host, password=self.psw, port=self.port, db=self.db,
                                            decode_responses=True)
            else:
                pool = redis.ConnectionPool(host=self.host, port=int(self.port), db=self.db,
                                            decode_responses=True)
            self.redis = redis.Redis(connection_pool=pool)
        except Exception as e:
            self.logging.exception(e)
        else:
            self.logging.info('{}redis连接成功'.format(self.host))

    def r_get(self, key):
        return self.redis.get(key)

    def r_set(self, key, value, expire_time):
        self.redis.set(key, value)
        if expire_time:
            self.redis.expire(key, expire_time)
        return True

    def r_del(self, key):
        self.redis.delete(key)

    def r_hset(self, name, key, value):
        self.redis.hset(name, key, value)
        return True

    def r_hget(self, name, key):
        return self.redis.hget(name, key)

    def r_hdel(self, name, key):
        self.redis.hdel(name, key)
        return True

    def r_hgetall(self, name):
        return self.redis.hgetall(name)

    def r_setbit(self, name, offset, value):
        self.redis.setbit(name, offset, value)
        return True

    def r_getbit(self, name, offset):
        return self.redis.getbit(name, offset)

    def r_bitcount(self, name, start, end):
        return self.redis.bitcount(name, start=start, end=end)

    def r_bitops(self, name, offset, value):
        return self.redis.bitpos(name, value, offset)
