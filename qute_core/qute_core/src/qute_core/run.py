from qute_core.subprocessHandler import SubprocessHandler
from qute_core.configparserHandler import ConfigparserHandler
from os import path
import os
import pytest


def run(cur_path, testcase, env, mark, report, db):
    """
    接口测试入口方法，获取命令行的参数值并初始化等
    :param cur_path:
    :param testcase:
    :param env:
    :param mark:
    :param report:
    :param db:
    :return:
    """

    args = ['-W ignore::UserWarning', '-v']

    if path.exists(path.join(cur_path, 'log')):
        if path.exists(path.join(cur_path, 'log', 'test.log')):
            os.remove(path.join(cur_path, 'log', 'test.log'))
        if path.exists(path.join(cur_path, 'log', 'data.json')):
            os.remove(path.join(cur_path, 'log', 'data.json'))
    else:
        os.mkdir(path.join(cur_path, 'log'))

    if report:
        if not path.exists(path.join(cur_path, 'report')):
            os.makedirs(path.join(cur_path, 'report', 'xml'))
            os.makedirs(path.join(cur_path, 'report', 'html'))

        args.insert(0, '--alluredir')
        args.insert(1, path.join(cur_path, 'report', 'xml'))
        args.insert(2, path.join(cur_path, 'api_test', testcase))
    else:
        args.insert(0, path.join(cur_path, 'api_test', testcase))

    if mark:
        if 'or' in mark or 'and' in mark:
            args.append('-m={}'.format(mark))
        else:
            args.append('-m={}'.format(' or '.join([mark.lower() if mark.istitle() else mark.upper(), mark])))

    configparserHandler = ConfigparserHandler(path.join(cur_path, 'config', 'env', 'env.ini'))
    configparserHandler.set_data('env', 'env', env)
    configparserHandler.set_data('db', 'db', db)

    pytest.main(args)

    if report:
        command = 'allure generate %s -o %s --clean' % (cur_path+'/report/xml', cur_path+'/report/html')
        try:
            SubprocessHandler().popen(command)
            print('生成html报告成功')
        except Exception:
            print('执行用例失败，请检查环境配置')
            raise
