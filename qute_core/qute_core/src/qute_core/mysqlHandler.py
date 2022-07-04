import pymysql
import pymysql.cursors
import textwrap
from qute_core.logHandler import LogHandler
from qute_core.configparserHandler import ConfigparserHandler


class MysqlHandler(object):
    def __init__(self, config_file, key):
        self.config = ConfigparserHandler(config_file)
        self.host = self.config.get_data(key, 'host')
        self.user = self.config.get_data(key, 'username')
        self.psd = self.config.get_data(key, 'password')
        self.db = self.config.get_data(key, 'database')
        self.port = self.config.get_data(key, 'port')
        self.conn = None
        self.cur = None
        self.logging = LogHandler().log()
        self.connect_mysql()

    def connect_mysql(self):
        try:
            self.conn = pymysql.connect(self.host, self.user, self.psd, self.db, int(self.port),
                                        cursorclass=pymysql.cursors.DictCursor, autocommit=True, charset='utf8')
        except Exception as e:
            self.logging.exception(e)
        else:
            self.cur = self.conn.cursor()
            self.logging.info('{}数据库连接成功'.format(self.host))

    def close_mysql(self):
        if self.conn and self.cur:
            self.conn.close()
            self.logging.info('{}数据库关闭成功'.format(self.host))

    def select_db(self, sql):
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            self.conn.commit()
        except Exception as e:
            self.logging.exception(e)
            return ''
        else:
            sql = textwrap.dedent(sql)
            self.logging.info(f'{sql} 数据库查询成功')
            return data

    def insert_db(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.logging.exception(e)
            self.conn.rollback()
            return False
        else:
            self.logging.info('{}数据库插入成功'.format(sql))
            return True

    def delete_db(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.logging.exception(e)
            self.conn.rollback()
            return False
        else:
            self.logging.info('{}数据库删除成功'.format(sql))
            return True

    def update_db(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.logging.exception(e)
            self.conn.rollback()
            return False
        else:
            self.logging.info('{}数据库更新成功'.format(sql))
            return True
