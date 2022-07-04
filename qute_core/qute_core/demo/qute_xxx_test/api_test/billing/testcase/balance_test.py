import allure
import pytest
from api_test.billing.testdata import balance_data
from qute_core.logHandler import LogHandler
from billing_app.BillingAppCaller import BillingAppCaller

logging = LogHandler().log()

def get_desc_as_test_id(fixture_value):
    """约定测试数据集第一个值为用例描述，把这个参数抽取出来作为test id的最后一部分
    """
    return fixture_value[0]

class TestBalance(object):
    """收入线-直播账号-余额查询 接口测试
    http://km.qutoutiao.net/pages/viewpage.action?pageId=94010746
    """

    @pytest.fixture(scope='class', autouse=True)
    def set_up(self, initialize):
        """对测试类进行初始化，可以用来初始化一些类公用测试资源
        把测试类中需要用到的辅助类提取出来：
        billing_app_caller, 封装了billing微服务的接口调用
        billing_db_helper, 封装了对billing数据的访问，用于获取测试数据库的数据
        """
        global billing_app_caller, billing_db_helper

        #billing app caller和billing数据库连接对象
        billing_db_helper = initialize['billing_db_helper']
        billing_app_caller = initialize['billing_app_caller']

    @pytest.fixture(params = [
        ("user_has_1_sub_account", 1),
        ("user_has_3_sub_account", 3)
        ], ids = get_desc_as_test_id)
    def get_query_success_params(self, request):
        """作为test_query_success用例的测试数据集合输入
        """
        sub_account_num = request.param[1]

        return balance_data.getQueryData(billing_db_helper, sub_account_num)

    @pytest.mark.P0
    @pytest.mark.owner_yangyuanyuan
    def test_query_success(self, request, get_query_success_params):
        """测试用例：流水查询成功
        """
        #构造数据
        data = get_query_success_params[0]
        db_balance_infos = get_query_success_params[1]

        # 发起请求
        ret, url = billing_app_caller.balance(data)
        setattr(request.node, 'url', url)

        # 校验返回码
        assert ret['code'] == 0

        # #校验数据库数据
        for balance_info in ret['data']['infos']:
            logging.info(f"balance_info: {balance_info}")
            assert balance_info["balance"] == db_balance_infos[balance_info["sub_type"]]


    @pytest.fixture(params = balance_data.getWrongParams(), ids = get_desc_as_test_id)
    def get_query_wrong_params(self, request):
        """作为test_query_wrong_param用例的测试集合输入，并指定test id的最后一部分
        """
        return request.param

    @pytest.mark.P1
    @pytest.mark.owner_yangyuanyuan
    def test_query_wrong_param(self, request, get_query_wrong_params):
        """测试流水查询接口在参数错误的情况下的返回
        get_query_wrong_params包含一组测试数据，每条测试数据包含以下部分：
            1. 案例描述，将作为test id的一部分
            2. 查询参数
            3. 期望返回码
        """

        #发起请求
        ret, url = billing_app_caller.balance(get_query_wrong_params[1])
        # 保存url信息用来和测试结果一起保存
        setattr(request.node, 'url', url)

        #校验返回码
        #TODO：参数错误的情况下还是返回0，不良设计
        assert ret['code'] == get_query_wrong_params[2]
        #由于参数错误，返回的数据集必然是空的
        assert len(ret['data']['infos']) == 0
