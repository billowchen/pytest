import allure
import pytest
import time
from api_test.gateway.testdata import auditAudit_data
from qute_core.logHandler import LogHandler

logging = LogHandler().log()

def get_desc_as_test_id(fixture_value):
    """约定测试数据集第一个值为用例描述，把这个参数抽取出来作为test id的最后一部分
    """
    return fixture_value[0]

class TestAuditAudit(object):
    """中台-审核平台-审核提交 接口测试
    """
    @pytest.fixture(scope='class', autouse=True)
    def set_up(self, initialize):
        """对测试类进行初始化，可以用来初始化一些类公用测试资源
        把测试类中需要用到的辅助类提取出来：
        """
        global gateway_app_caller
        gateway_app_caller = initialize['gateway_app_caller']
    @pytest.fixture()
    def get_auditAudit_params(self):

        return auditAudit_data.getAuditAuditData()

    @pytest.mark.P0
    @pytest.mark.owner_chenyoujin
    @pytest.mark.dependency(depends=['TestauditView::test_auditView_success'])

    def test_auditAudit_success(self, request, get_auditAudit_params):
        """测试用例：审核提交
        """
        # 构造数据
        data = get_auditAudit_params
        # 发起请求
        ret, url = gateway_app_caller.auditAudit(data)
        setattr(request.node, 'url', url)
        # 校验返回码
        assert ret['code'] == 0


