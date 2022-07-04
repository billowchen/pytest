import json
import datetime
from qute_core.logHandler import LogHandler


logging = LogHandler().log()

class AuditMysql(object):
    """audit访问数据库的辅助类
    """
    def __init__(self, mysql):
        """构造audit dao对象
        Args:
            param: mysql, MysqlHandler对象，封装了对mysql数据库访问的方法
        """
        self.mysql = mysql

    def getrecord_id(self,table):
        sql = f"SELECT content_id,title,op_id FROM {table} order by create_time desc limit 2"
        content_id = self.mysql.select_db(sql)[0]['content_id']
        return content_id

    def getaction(self,table):
        sql = f"SELECT content_id,title,op_id，action FROM {table} where content_id={id} order by create_time "
        action = self.mysql.select_db(sql)[0]['content_id']
        return action


class AuditDao(object):
    """audit访问数据库的辅助类
    """
    def __init__(self, mongo):
        """构造audit dao对象
        Args:
            param: mysql, MysqlHandler对象，封装了对mysql数据库访问的方法
        """
        self.mongo = mongo

    def getAlbumddcontent_id(self):
        #set='dd_albumdd_audit_queue'
        #dic={'app_key':'albumdd'}
       #set=f"db.dd_albumdd_audit_queue.find({'app_key':'albumdd'}).sort({'content_id': -1}).limit(5)"
        data=self.mongo.find('audit','dd_albumdd_audit_queue',{'app_key':'albumdd'},sort_key='content_id',limit=5)[0]['content_id']
        return data

    def getvideollop_id(self,id):
        data=self.mongo.find('audit','audit_queue_ll',{'content_id':id})[0]['op_id']
        return data

    def getshortvideollop_id(self,id):
        data=self.mongo.find('audit','audit_queue_ll',{'content_id':id})[0]['op_id']
        return data

    def getShortarticlehfhop_id(self,id):
        #set='dd_albumdd_audit_queue'
        #dic={'app_key':'albumdd'}
       #set=f"db.dd_albumdd_audit_queue.find({'app_key':'albumdd'}).sort({'content_id': -1}).limit(5)"
        data=self.mongo.find('audit','hfh_shortarticlehfh_audit_queue',{'content_id':id})[0]['op_id']
        return data
































