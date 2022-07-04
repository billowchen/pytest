import os
import json
from os import path
from qute_core.qute_excel.excelHandler import ExcelHandler
from qute_core.qute_excel import run_testcase
from qute_core.configparserHandler import ConfigparserHandler
from qute_core.redisHandler import RedisHandler
from qute_core.mysqlHandler import MysqlHandler


def run_excel(cur_path, testcase, env, mark):
    redisObj, mysqlObj, file_path, result_list, fail_case = {}, {}, [], [], []

    base_path = path.join(cur_path, 'excel_test', 'config')
    config_path = path.join(base_path, f'config_{env}.ini')
    redis_path = path.join(base_path, 'config_redis.ini')
    mysql_path = path.join(base_path, 'config_mysql.ini')
    result_path = path.join(cur_path, 'log', 'data.json')
    log_path = path.join(cur_path, 'log')

    if path.exists(log_path):
        if path.exists(path.join(cur_path, 'test.log')):
            os.remove(path.join(cur_path, 'test.log'))
        if path.exists(path.join(cur_path, 'data.json')):
            os.remove(path.join(cur_path, 'data.json'))
    else:
        os.mkdir(log_path)

    if path.exists(redis_path):
        conf = ConfigparserHandler(redis_path)
        sections = conf.get_sections()
        for section in sections:
            key = conf.get_data(section, 'name')
            redisObj[key] = RedisHandler(redis_path, section)

    if path.exists(mysql_path):
        conf = ConfigparserHandler(mysql_path)
        sections = conf.get_sections()
        for section in sections:
            key = conf.get_data(section, 'name')
            mysqlObj[key] = MysqlHandler(mysql_path, section)

    if path.exists(result_path):
        os.remove(result_path)

    if path.exists(config_path):
        os.remove(config_path)
    configObj = ConfigparserHandler(config_path)

    if testcase.startswith('excel_test') and (testcase.endswith('excel_test') or testcase.endswith('excel_test/')):
        testcase = path.join(cur_path, testcase, 'testcase')
        for file in os.listdir(testcase):
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path.append(path.join(cur_path, testcase, file))
        sheet_name = ''
    elif testcase.strip().endswith('.xlsx') or testcase.strip().endswith('.xls'):
        file = path.join(cur_path, testcase)
        file_path.append(file)
        sheet_name = ''
    else:
        testcase = testcase.strip().split('/')
        file_path.append(path.join(cur_path, 'excel_test', 'testcase', testcase[-2]))
        sheet_name = testcase[-1]

    for file in file_path:
        ex = ExcelHandler(file, configObj, sheet_name)
        file_name, file_data = ex.get_sheets_data()

        print('Excel文件名称：', file_name)
        print('Excel文件数据：', file_data)
        config_value = configObj.get_section_items(file_name)
        print('Excel文件配置信息：', config_value)

        t = run_testcase.RunTestcase(redisObj, mysqlObj, config_value, env, mark, file_data)
        result, fail = t.run_testcase()

        result_list.extend(result)
        fail_case.extend(fail)

    with open(result_path, 'w', encoding='utf-8') as fw:
        json.dump(result_list, fw, ensure_ascii=False, indent=4)

    print('执行失败用例名称如下：', fail_case) if fail_case else print('用例全部执行成功！')
