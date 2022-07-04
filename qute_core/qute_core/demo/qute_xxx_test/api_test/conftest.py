import datetime
import json
import os
from os import path
import allure
import pytest
from _pytest.runner import runtestprotocol
from qute_core.configparserHandler import ConfigparserHandler
from qute_core.logHandler import LogHandler
from qute_core.mysqlHandler import MysqlHandler
from coupon_app.CouponAppCaller import CouponAppCaller
from billing_app.BillingAppCaller import BillingAppCaller

#日志收集器
logging = LogHandler().log()
#配置读取器
configParseHandler = ''
#运行根目录
base_dir = path.dirname(path.dirname(__file__))
#测试环境配置文件保存目录
test_env_dir = path.join(base_dir, 'config', 'env')
#测试结果保存文件
test_result_file = path.join(base_dir, 'log', 'data.json')
#一次运行的所有测试结果
test_results = []
#单个用例的测试结果
test_case_result = {}
#用例运行当前子系统
current_app = ''


def allure_config():
    allure.environment(python_version='3.6.4')
    allure.environment(pytest_version='5.0.1')
    allure.environment(allure_version='2.8.1')
    allure.environment(JDK='1.8.0')


def pytest_addoption(parser):
    """这个方法是pytest Initialization hooks中的一个，每个test run运行一次
    https://docs.pytest.org/en/latest/reference.html

    读取保存在env.ini中的命令行参数，并将命令行参数添加到option中，
    之后可以在request.config中读取
    """
    config = ConfigparserHandler(path.join(test_env_dir, 'env.ini'))
    env = config.get_data('env', 'env')
    db = config.get_data('db', 'db')

    #Options can later be accessed through the config object
    parser.addoption("--env", action='store', default=env, help='获取测试环境')
    parser.addoption("--db", action='store', default=db, help='测试结果是否入库')


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
    #coupon init
    coupon_host = configParseHandler.get_data('coupon_host', 'host')
    coupon_db_helper = MysqlHandler(config_path, 'coupon_DB')
    coupon_app_caller = CouponAppCaller(coupon_host)

    #payment init
    payment_host = configParseHandler.get_data('payment_host', 'host')
    payment_db_helper = MysqlHandler(config_path, 'payment_DB')
    payment_app_caller = CouponAppCaller(payment_host)

    #billing init
    billing_host = configParseHandler.get_data('billing_host', 'host')
    billing_db_helper = MysqlHandler(config_path, 'billing_DB')
    billing_app_caller = BillingAppCaller(billing_host)

    #将整个测试过程中需要的测试辅助对象放入容器中并返回
    container['coupon_db_helper']   = coupon_db_helper
    container['coupon_app_caller']  = coupon_app_caller
    container['payment_db_helper']  = payment_db_helper
    container['payment_app_caller'] = payment_app_caller
    container['billing_db_helper']  = billing_db_helper
    container['billing_app_caller'] = billing_app_caller

    yield container
    coupon_db_helper.close_mysql()
    payment_db_helper.close_mysql()
    billing_db_helper.close_mysql()
    logging.debug('用例执行完成，清除所有占用资源!')


@pytest.fixture(scope='function', autouse=True)
def collect_test_result(request):
    """收集用例信息
    """
    global test_case_result
    case_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Test case: {request.node.nodeid} start!")

    yield
    case_end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if test_case_result:
        test_case_result = {}

    test_case_result['start_time'] = case_start_time
    test_case_result['end_time'] = case_end_time
    test_case_result['case_name'] = request.node.name

    try:
        test_case_result['url'] = request.node.url
    except:
        test_case_result['url'] = ''

    test_case_result['case_full_path'] = request.node.nodeid
    test_case_result['app'] = current_app
    test_case_result['host'] = 'host'

    owner = [i.name.split('_')[1] for i in request.node.own_markers if i.name.startswith('owner')]
    test_case_result['owner'] = owner[0] if owner else ''
    logging.info(f"Test case: {request.node.nodeid} end!")


def pytest_runtest_protocol(item, nextitem):
    """pytest test running hooks, called for performing the main runtest loop (after collection finished)
    https://docs.pytest.org/en/latest/reference.html

    收集用例运行结果，并最终输出到文件
    """
    global current_app
    current_app = item.nodeid.split('/')[1]

    reports = runtestprotocol(item, nextitem=nextitem)

    for report in reports:
        if report.when == 'call':
            if report.passed:
                test_case_result['result'] = 'Pass'
                test_case_result['err_message'] = ''
            else:
                test_case_result['result'] = 'Fail'
                test_case_result['err_message'] = report.longrepr.reprcrash.message
            test_case_result['duration'] = '%.2f' % report.duration
            test_results.append(test_case_result)
            break

    if nextitem == None:
        if pytest.config.getoption('--db').upper() == 'TRUE':
            if os.path.exists(test_result_file):
                os.remove(test_result_file)
            fw = open(test_result_file, 'a', encoding='utf-8')
            json.dump(test_results, fw, ensure_ascii=False, indent=4)
            fw.close()
    return True
