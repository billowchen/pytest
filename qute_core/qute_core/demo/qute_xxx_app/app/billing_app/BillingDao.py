
class BillingDao(object):
    """Billing访问数据库的辅助类
    """
    def __init__(self, mysql):
        """构造billing dao对象
        Args:
            param: mysql, MysqlHandler对象，封装了对mysql数据库访问的方法
        """
        self.mysql = mysql

    def getAccountsByUid(self, uid):
        """根据uid查询直播账户信息，一个uid可能有多个子账户
        http://km.qutoutiao.net/pages/viewpage.action?pageId=94011329
        http://km.qutoutiao.net/pages/viewpage.action?pageId=96780252
        Args:
            param: uid, user id

        Returns:
            返回数据库中uid对应的直播账户信息
        """
        sql = f"select * from account.accounts a where a.uid = '{uid}'"

        return self.mysql.select_db(sql)


    def getOneAccountInfo(self, accountNum):
        """根据子账户个数随机捞取一条直播账户信息

        Args:
            accountNum: 子账户个数

        Returns:
            返回一条直播账户数据
        """
        sql = f"select * from account.accounts a, \
(select uid, count(sub_type) account_num from account.accounts group by uid) t \
where t.account_num = {accountNum} and a.uid = t.uid and RAND() <= 0.1 limit 1"

        return self.mysql.select_db(sql)[0]
