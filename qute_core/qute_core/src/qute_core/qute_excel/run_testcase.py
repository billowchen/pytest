from qute_core.logHandler import LogHandler
from qute_core.qute_excel.common import *


class RunTestcase:
    def __init__(self, redisObj, mysqlObj, config_value, env, mark, file_data):
        self.redisObj = redisObj
        self.mysqlObj = mysqlObj
        self.config_value = config_value
        self.env = env
        self.file_data = file_data
        self.mark_list = [mark.lower() if mark.istitle() else mark.upper(), mark] if mark else []
        self.fail_case = []
        self.result_list = []
        self.start_time = ''
        self.end_time = ''
        self.logging = LogHandler().log()

    def run_testcase(self):
        for data in self.file_data:
            for sheet_name, case_list in data.items():
                for case in case_list:
                    if self.mark_list:
                        if case['tag'] in self.mark_list and case['execute'] == 1.0:
                            self.logging.info('当前执行的测试用例名称为：{}'.format(case["casename"]))
                            if 'before' in case.keys() and case['before']:
                                self.before_data(case['before'])
                        else:
                            continue
                    else:
                        if case['execute'] == 1.0:
                            self.logging.info('当前执行的测试用例名称为：{}'.format(case["casename"]))
                            if 'before' in case.keys() and case['before']:
                                self.before_data(case['before'])
                        else:
                            continue

                    url, host = get_url(case['host'], case['path'], self.config_value['host'])

                    header = self.body_handler(case['header']) if case['header'] else ''

                    method = case['method'].strip().lower()
                    params = self.body_handler(case['params']) if method == 'get' else self.body_handler(case['body'])

                    self.start_time = cur_time()
                    r = RequestHandler(url, params, header=header)
                    code, ret = request_run(r, method)

                    flag, err_msg = self.assert_result(ret, int(case['code']), case['check'])
                    self.end_time = cur_time()

                    self.fail_case.append(case["casename"]) if err_msg else ''

                    kv_dic = self.split_check(case['key-value']) if case['key-value'] else ''

                    self.kv_case(ret, kv_dic) if flag and kv_dic else ''

                    self.before_data(case['after'], ret) if case['after'] else ''

                    self.collect_result(case['owner'], case['path'], case['casename'], sheet_name, host, flag, err_msg)

                    sleep(case['sleep'])

        return self.result_list, self.fail_case

    def collect_result(self, owner, url, casename, sheet_name, host, result, err):
        result_dic = get_result(owner, url, casename, sheet_name, host, result, err)

        duration = self.end_time-self.start_time

        result_dic['duration'] = '%.2f' % (duration.microseconds/1000000 + duration.seconds)
        result_dic['start_time'] = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        result_dic['end_time'] = self.end_time.strftime("%Y-%m-%d %H:%M:%S")
        result_dic['env'] = self.env

        self.result_list.append(result_dic)

    def kv_case(self, ret, kv_dic):
        for key, value in kv_dic.items():
            if isinstance(value, str):
                value = k_v_check(value, self.redisObj, self.mysqlObj, ret)
            if isinstance(key, str):
                key = k_v_check(key, self.redisObj, self.mysqlObj, ret)
            self.config_value[key] = value

    def assert_result(self, ret, ex_code, check):
        flag, err_msg = True, ''
        check = self.replace_data(check)

        if isinstance(ret, dict):
            if ret.get('code') == ex_code:
                if check:
                    check_dic = self.split_check(check)

                    for key, value in check_dic.items():
                        if isinstance(value, str):
                            value = k_v_check(value, self.redisObj, self.mysqlObj, ret)
                        elif isinstance(value, list):
                            data = k_v_check(key, self.redisObj, self.mysqlObj, ret)
                            if data and eval('{0} in {1}'.format(data, value)):
                                continue
                            flag = False
                            err_msg = f'assert {key}获取结果:{data} != {value}'
                            break
                        if isinstance(key, str):
                            key = k_v_check(key, self.redisObj, self.mysqlObj, ret)

                        if key == value:
                            continue
                        else:
                            flag = False
                            err_msg = f'assert {key}获取结果:{key} != {value}'
                            break
            else:
                flag = False
                err_msg = f'请求结果返回code {ret["code"]} != {ex_code}'
        else:
            flag = False
            err_msg = '请求失败！'
        return flag, err_msg

    #前置/后置操作
    def before_data(self, data, ret=None):
        data = self.replace_data(data)

        data_list = data.split('\n')
        for i in data_list:
            data = i.split('=', 1)
            if len(data) == 2:
                dic = {data[0].strip(): data[1].strip()}
                self.kv_case(ret, dic)
            else:
                k_v_check(data[0], self.redisObj, self.mysqlObj, ret)

    #格式化 ${}格式
    def replace_data(self, data):
        res = re_findall(r"(\$\{[a-zA-Z\_][0-9a-zA-Z\_]*\})", data)

        if res:
            for i in res:
                k = i[2:-1].strip()
                value = self.config_value.get(k.lower())
                data = data.replace(i, str(value)) if value else data.replace(i, 'error')
        return data

    #params其他形式的格式化，格式如下： a:b, a:b\nc:d, a b, a空格b\nc空格d
    def split_params(self, data):
        dic = {}
        params = data.split('\n')
        for param in params:
            param = param.strip()
            if param:
                if param.startswith('start_time') or param.startswith('end_time'):
                    value = param.split(' ', 1)
                    dic[value[0].strip()] = value[1].strip() if len(value) == 2 else ''
                else:
                    value0 = param.split(':', 1) if ':' in param else param.split(' ', 1)
                    key = value0[0].strip()
                    value = value0[1].strip() if len(value0) == 2 else ''
                    dic[key] = json.dumps(eval(value)) if value.startswith('{') and value.endswith('}') else value
        return dic

    def body_handler(self, data):
        body = self.replace_data(data)
        body = random_phone(r"(\$random\((.*?)\))", body)
        body = body.replace('false', 'False').replace('true', 'True')
        if body.strip().startswith('qdata:$[{'):
            res = re_findall(r"\$\[(.*)\]", data, flags=re.S)
            dic = eval(res[0])
            return sign_data(dic) if 'sign' in dic.keys() else aes_encrypt(dic)
        else:
            dic = eval(data) if data.strip().startswith('{') and data.strip().endswith('}') else self.split_params(body)
            return sign_data(dic, flag=False) if 'sign' in dic.keys() else dic

    def split_check(self, data):
        item_list = []

        data = self.replace_data(data)
        param_list = data.split('\n')

        for param in param_list:
            k, v = param.strip().split('=', 1) if '=' in param else param.strip().split('IN', 1)
            if v.strip() == 'null':
                v = ''
            if 'redis' not in k:
                try:
                    v = eval(v.strip())
                except:
                    v = v.strip()
                item_list.append((k.strip(), v))
            else:
                item_list.append((k.strip(), v.strip()))
        return dict(item_list)
