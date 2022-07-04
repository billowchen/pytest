from gateway_app.GatewayApp import _gateway_app
from qute_core.requestHandler import RequestHandler
from qute_core.logHandler import LogHandler

#日志收集器
logging = LogHandler().log()

class GatewayAppCaller(object):
    """
        审核平台
        http://km.qutoutiao.net/pages/viewpage.action?pageId=96769210
    """

    def __init__(self, host):
        self.host = host
        self.gatewayApp = _gateway_app()
        self.header = {"Content-Type": "application/json; charset=utf-8"}

    def auditGetProduct(self, param):
        """获取产品配置
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.auditGetProduct
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.auditGetProduct

    def auditStatistics(self, param):
        """数据概览统计
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.auditStatistics
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.auditStatistics

    def auditConfig(self, param):
        """获取配置信息
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.auditConfig
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.auditConfig

    def auditList(self, param):
        """列表记录
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.auditList
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.auditList

    def auditView(self, param):
        """获取详情
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.auditView
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.auditView

    def auditQuit(self, param):
        """退出审核
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.auditQuit
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.auditQuit

    def auditAudit(self, param):
        """审核提交
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.auditAudit
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.auditAudit

    def authorityRecord(self, param):
        """审核记录产品配置
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.authorityRecord
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.authorityRecord

    def recordConfig(self, param):
        """获取审核记录配置信息
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.recordConfig
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.recordConfig


    def recordList(self, param):
        """审核记录列表
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.recordList
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.recordList

    def recordView(self, param):
        """审核记录详情
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.recordView
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.recordView

    def recordAudit(self, param):
        """审核记录提交
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.recordAudit
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.recordAudit

    def recordOperation(self, param):
        """获取审核操作记录
        Args:
            param: Dictionary, list of tuples or bytes to send to service
        Returns:
            ret: 服务器返回对象
            url: 服务请求地址，不包含主机地址和协议
        """
        url = self.host + self.gatewayApp.recordOperation
        code, ret = RequestHandler(url, param).post_form()

        if code != 200:
            logging.warn("http response code is not 200!")

        return ret, self.gatewayApp.recordOperation