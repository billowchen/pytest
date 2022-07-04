import os
import re
import json
import allure
import datetime
import pytest
from qute_core.logHandler import LogHandler
from qute_core.configparserHandler import ConfigparserHandler

logging = LogHandler().log()


def get_desc_as_test_id(fixtrue_value):
    """对于使用参数化的测试方法，
    约定参数列表的第一个参数是测试案例的描述，
    把这个参数抽取出来作为test id的最后一部分
    """
    return fixtrue_value[0]


def allure_config():
    """
    allure报告显示的环境信息
    :return:
    """
    allure.environment(python_version='3.6.4')
    allure.environment(pytest_version='5.0.1')
    allure.environment(allure_version='2.8.1')
    allure.environment(JDK='1.8.0')


def addoption(parser, test_env_dir):
    """这个方法是pytest Initialization hooks中的一个，每个test run运行一次
    https://docs.pytest.org/en/latest/reference.html

    读取保存在env.ini中的命令行参数，并将命令行参数添加到option中，
    之后可以在request.config中读取
    """
    config = ConfigparserHandler(os.path.join(test_env_dir, 'env.ini'))
    env = config.get_data('env', 'env')
    db = config.get_data('db', 'db')

    parser.addoption("--env", action='store', default=env, help='获取测试环境')
    parser.addoption("--db", action='store', default=db, help='测试结果是否入库')


def test_result_start(request):
    """收集用例信息
    """
    case_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Test case: {request.node.nodeid} start!")
    return case_start_time


def test_result_end(request, configParseHandler, current_app, case_start_time):
    test_case_result = {}
    case_end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if test_case_result:
        test_case_result = {}

    test_case_result['start_time'] = case_start_time
    test_case_result['end_time'] = case_end_time
    test_case_result['env'] = request.config.getoption('--env')

    try:
        test_case_result['url'] = request.node.url
    except:
        test_case_result['url'] = ''

    case_full_path = request.node.nodeid
    if '[' in case_full_path and '\\' in case_full_path:
        ret = re.findall(r'\[(.*)\]$', case_full_path)
        case_full_path1 = ret[0].encode('utf-8').decode("unicode_escape")
        test_case_result['case_full_path'] = case_full_path.replace(ret[0], case_full_path1)
    else:
        test_case_result['case_full_path'] = request.node.nodeid

    test_case_result['case_name'] = test_case_result['case_full_path'].split('::')[-1]

    test_case_result['app'] = current_app
    test_case_result['host'] = configParseHandler.get_data(f'{current_app}_host', 'host')

    mark_list = [mark.name for mark in request.node.own_markers]

    case_from = 'scenario' if 'dependency' in mark_list else ''
    owner, test_link = '', ''
    for mark in mark_list:
        if case_from and mark.startswith('testlink'):
            test_link = mark.split('_')[1]
        if not owner and mark.startswith('owner'):
            owner = mark.split('_')[1]

    test_case_result['owner'] = owner
    test_case_result['test_link_id'] = test_link
    test_case_result['from'] = case_from if case_from else 'qute'
    logging.info(f"Test case: {request.node.nodeid} end!")
    return test_case_result


def run_protocol(nextitem, reports, test_results, test_case_result, test_result_file):
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
            fw = open(test_result_file, 'a', encoding='utf-8')
            json.dump(test_results, fw, ensure_ascii=False, indent=4)
            fw.close()
