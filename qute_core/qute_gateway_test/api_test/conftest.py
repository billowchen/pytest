from os import path
from _pytest.runner import runtestprotocol
from qute_core.mysqlHandler import MysqlHandler
from gateway_app.GatewayAppCaller import GatewayAppCaller
from qute_core.redisHandler import RedisHandler
from qute_core.mongoHandler import MongoHandler
from qute_core.pytest_conftest import *

# 配置读取器
configParseHandler = ''
# 运行根目录
base_dir = path.dirname(path.dirname(__file__))
# 测试环境配置文件保存目录
test_env_dir = path.join(base_dir, 'config', 'env')
# 测试结果保存文件
test_result_file = path.join(base_dir, 'log', 'data.json')
# 一次运行的所有测试结果
test_results = []
# 单个用例的测试结果
test_case_result = {}
# 用例运行当前子系统
current_app = ''

def pytest_addoption(parser):
    """这个方法是pytest Initialization hooks中的一个，每个test run运行一次
    https://docs.pytest.org/en/latest/reference.html

    读取保存在env.ini中的命令行参数，并将命令行参数添加到option中，
    之后可以在request.config中读取
    """
    addoption(parser, test_env_dir)


@pytest.fixture(scope='session', autouse=True)
def initialize(request):
    """初始化一些整个test session都需要的对象
    整个测试运行过程中只执行一次
    """
    global configParseHandler
    container = {}
    allure_config()

    # 读取设定的测试环境
    env = request.config.getoption('--env')
    config_path = path.join(test_env_dir, f'config_{env}.ini')
    configParseHandler = ConfigparserHandler(config_path)
    # audit init
    #audit_host = configParseHandler.get_data('audit_host', 'host')
    #audit_app_caller = AuditAppCaller(audit_host)
    #audit_db_helper = MysqlHandler(config_path, 'audit_DB')

    # gateway init
    gateway_host = configParseHandler.get_data('gateway_host', 'host')
    gateway_app_caller = GatewayAppCaller(gateway_host)
    gateway_db_helper = MysqlHandler(config_path, 'gateway_DB')
    gateway_mongo_helper=MongoHandler(config_path, 'audit_MONGO')

   # fiction_redis_helper = RedisHandler(config_path, 'REDIS')

    # 将整个测试过程中需要的测试辅助对象放入容器中并返回
    # 审核侧
    container['gateway_app_caller'] = gateway_app_caller
    container['gateway_db_helper'] = gateway_db_helper
    container['gateway_mongo_helper'] = gateway_mongo_helper

    yield container
    logging.debug('用例执行完成，清除所有占用资源!')


@pytest.fixture(scope='function', autouse=True)
def collect_test_result(request):
    """收集用例信息
    """
    global test_case_result
    case_start_time = test_result_start(request)
    yield
    test_case_result = test_result_end(request, configParseHandler, current_app, case_start_time)


def pytest_runtest_protocol(item, nextitem):
    """pytest test running hooks, called for performing the main runtest loop (after collection finished)
    https://docs.pytest.org/en/latest/reference.html

    收集用例运行结果，并最终输出到文件
    """
    global current_app
    current_app = item.nodeid.split('/')[1]
    reports = runtestprotocol(item, nextitem=nextitem)

    run_protocol(nextitem, reports, test_results, test_case_result, test_result_file)
    return True
