from qute_core.const import _const
class _billing_app(_const):
    def __init__(self):
        #创建交易
        self.TRADE = '/record/v1/trade'
        #流水查询
        self.QUERY = '/record/v1/query'
        #余额查询
        self.BALANCE = '/account/v1/balance'