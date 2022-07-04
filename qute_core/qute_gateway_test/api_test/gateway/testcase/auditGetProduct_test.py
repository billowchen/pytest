import allure
import pytest
import time
from api_test.gateway.testdata import auditGetProduct_data
from qute_core.logHandler import LogHandler

logging = LogHandler().log()

def get_desc_as_test_id(fixture_value):
    """约定测试数据集第一个值为用例描述，把这个参数抽取出来作为test id的最后一部分
    """
    return fixture_value[0]

class TestAuditGetProduct(object):
    """中台-审核平台-获取产品配置 接口测试
    """
    @pytest.fixture(scope='class', autouse=True)
    def set_up(self, initialize):
        """对测试类进行初始化，可以用来初始化一些类公用测试资源
        把测试类中需要用到的辅助类提取出来：
        """
        global gateway_app_caller
        gateway_app_caller = initialize['gateway_app_caller']

    @pytest.fixture()
    def get_auditGetProduct_params(self):
        """作为test_auditGetProduct_success用例的测试数据集合输入
        """
        return auditGetProduct_data.getAuditGetProductData()

    @pytest.mark.P0
    @pytest.mark.owner_chenyoujin
    def test_auditGetProduct_success(self, request, get_auditGetProduct_params):
        """测试用例：获取产品配置
        """
        # 构造数据
        data = get_auditGetProduct_params
        # 发起请求
        ret, url = gateway_app_caller.auditGetProduct(data)
        setattr(request.node, 'url', url)
        # 校验返回码
        assert ret['code'] == 0
        assert ret['data']['list'][0]['genre'] == 'short_video'


