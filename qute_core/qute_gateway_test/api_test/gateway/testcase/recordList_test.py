import allure
import pytest
import time
from api_test.gateway.testdata import recordList_data
from qute_core.logHandler import LogHandler

logging = LogHandler().log()

def get_desc_as_test_id(fixture_value):
    """约定测试数据集第一个值为用例描述，把这个参数抽取出来作为test id的最后一部分
    """
    return fixture_value[0]

class TestRecordList(object):
    """中台-审核平台-审核记录列表 接口测试
    """
    @pytest.fixture(scope='class', autouse=True)
    def set_up(self, initialize):
        """对测试类进行初始化，可以用来初始化一些类公用测试资源
        把测试类中需要用到的辅助类提取出来：
        """
        global gateway_app_caller
        gateway_app_caller = initialize['gateway_app_caller']
    @pytest.fixture()
    def get_recordList_params(self):

        return recordList_data.getRecordListData()

    @pytest.mark.P0
    @pytest.mark.owner_chenyoujin
   # @pytest.mark.dependency(depends=['TestauditView::test_auditView_success'])

    def test_recordList_success(self, request, get_recordList_params):
        """测试用例：审核记录列表
        """
        # 构造数据
        data = get_recordList_params
        # 发起请求
        ret, url = gateway_app_caller.recordList(data)
        setattr(request.node, 'url', url)
        # 校验返回码
        assert ret['code'] == 0


