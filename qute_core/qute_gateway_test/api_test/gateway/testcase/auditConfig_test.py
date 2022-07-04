import allure
import pytest
import time
from api_test.gateway.testdata import auditConfig_data
from qute_core.logHandler import LogHandler

logging = LogHandler().log()

def get_desc_as_test_id(fixture_value):
    """约定测试数据集第一个值为用例描述，把这个参数抽取出来作为test id的最后一部分
    """
    return fixture_value[0]

class TestAuditConfig(object):
    """中台-审核平台-获取配置信息 接口测试
    """
    @pytest.fixture(scope='class', autouse=True)
    def set_up(self, initialize):
        """对测试类进行初始化，可以用来初始化一些类公用测试资源
        把测试类中需要用到的辅助类提取出来：
        """
        global gateway_app_caller
        gateway_app_caller = initialize['gateway_app_caller']

    @pytest.fixture()
    def get_auditConfig_params(self):
        return auditConfig_data.getAuditConfigData()

    @pytest.mark.P0
    @pytest.mark.owner_chenyoujin
    def test_auditConfig_success(self, request, get_auditConfig_params):
        """测试用例：获取配置信息
        """
        # 构造数据
        data = get_auditConfig_params
        # 发起请求
        ret, url = gateway_app_caller.auditConfig(data)
        setattr(request.node, 'url', url)
        # 校验返回码
        assert ret['code'] == 0
        assert ret['data']['options']['rejectReason']['value']['content_problem']['list'][0]['keyword']== "暂不收录"


