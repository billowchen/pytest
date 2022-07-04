import re
import time
import jsonpath
import datetime
import random
from qute_core.sign import *


# 生成sign值
def sign_data(data, flag=True):
    del data['sign']

    dtu = data.get('dtu')
    dtu = int(dtu) if dtu else 1

    apikey = '' if dtu == 200 else "key=5hZIUWKcfQnrykpu" if dtu >= 100 and dtu < 300 else "key=6GRFEFfMy2ETEqjm"

    data['sign'] = sign(data, apikey)

    if flag:
        data = aes_encrypt(data, dtu)

    return data


def cur_time():
    return datetime.datetime.now()


def format_time(format):
    try:
        value = cur_time().strftime(format)
    except:
        value = ''
    return value


def sleep(data):
    if data:
        duration = str(data) if isinstance(data, (int, float)) else data.strip().split('s')[0]
    else:
        duration = '1'
    return time.sleep(float(duration))


def re_findall(key, value, flags=None):
    data = re.findall(key, value, flags=flags) if flags else re.findall(key, value)
    return data if data else ''


def check_jsonpath(ret, key):
    data = jsonpath.jsonpath(ret, expr=key)
    return data[0] if isinstance(data, list) else ''


def get_url(host, path, config_host):
    if host:
        host = host if host.strip().startswith('http://') else 'http://' + host
    else:
        host = config_host
    url = ''.join([host, path])

    return url, host


def get_result(owner, url, casename, sheet_name, host, result, err):
    result_dic = {}

    result_dic['from'] = 'excel'
    result_dic['testlink_id'] = ''
    result_dic['url'] = url
    result_dic['case_full_path'] = ''
    result_dic['case_name'] = casename
    result_dic['app'] = sheet_name
    result_dic['host'] = host
    result_dic['owner'] = owner
    result_dic['result'] = result
    if result:
        result_dic['err_message'] = ''
    else:
        result_dic['err_message'] = err

    return result_dic


def redis_mysql_check(key, value, redisObj, mysqlObj):
    ret = ''
    data = re_findall(key, value)
    if data:
        if 'redis' in data[0][0]:
            if data[0][1] == 'delete':
                redisObj[data[0][0]].r_del(data[0][2])
            elif data[0][1] == 'get':
                ret = redisObj[data[0][0]].r_get(data[0][2])
        else:
            if data[0][1] == 'query':
                data = mysqlObj[data[0][0]].select_db(data[0][2].replace('"', ''))#[{'id':1}]
                ret = list(data[0].values())[0] if data else ''

    return ret if ret else ''


def k_v_check(data, redisObj, mysqlObj, ret):
    if data.startswith('$cur_datetime'):
        data = re_findall(r'\$cur_datetime\(\"(.*)\"\)', data)
        data = format_time(data[0]) if data else ''
    elif data.startswith('$.') and ('redis' in data or 'mysql' in data):
        data = redis_mysql_check(r'\$\.(.*?)\.(.*?)\((.*?)\)', data, redisObj, mysqlObj)
    elif data.startswith('$.'):
        data = check_jsonpath(ret, data)
        try:
            data = eval(data)
        except:
            data = data
    return data


def request_run(r, method):
    code, ret = r.get() if method == 'get' else r.post_json() if method == 'post/json' else r.post_form()
    return code, ret


def random_phone(key, value):
    data = re.findall(key, value)
    if data:
        k, v = data[0][0], data[0][1]
        v1, v2 = v.strip().split(',')
        phone_list = random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], int(v1)-len(v2))
        phone_list.insert(0, v2)
        phone = ''.join(phone_list)
        value = value.replace(k, phone)
    return value
