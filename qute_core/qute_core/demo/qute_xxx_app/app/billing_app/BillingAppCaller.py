from billing_app.BillingApp import _billing_app
from qute_core.requestHandler import RequestHandler
from qute_core.logHandler import LogHandler

#日志收集器
logging = LogHandler().log()

class BillingAppCaller(object):
    """账户交易
    http://km.qutoutiao.net/pages/viewpage.action?pageId=94009989
    """

    def __init__(self, host):
        self.host = host
        self.billingApp = _billing_app()

    def trade(self, param):
        """账户充值接口
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.billingApp.TRADE
        code, ret = RequestHandler(url, param).post_json()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.billingApp.TRADE

    def balance(self, param):
        """余额查询接口
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.billingApp.BALANCE
        code, ret = RequestHandler(url, param).post_json()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.billingApp.BALANCE


    def query(self, param):
        """流水查询接口
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.billingApp.QUERY
        code, ret = RequestHandler(url, param).post_json()

        if code == 200:
            logging.warn("http response code is not 200!")

        return ret, self.billingApp.QUERY

