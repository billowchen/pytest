import hashlib
import base64
import json
import redis
from qute_core.requestHandler import RequestHandler


def sign(params, apikey):
    """
    :param params:字典类型
    :param apikey: key=6GRFEFfMy2ETEqjm
    :return:
    """
    params_original = sorted(params.items(), key=lambda asd: asd[0])

    sign_params = ''
    for item in params_original:
        try:
            sign_params = sign_params + str(item[0]) + '=' + str(item[1]) + '&'
        except:
            sign_params = sign_params + str(item[0].encode('utf8')) + '=' + str(item[1].encode('utf8')) + '&'

    sign_original = sign_params + apikey

    m1 = hashlib.md5()
    m1.update(sign_original.encode("utf-8"))
    sign = m1.hexdigest()
    return sign


#  AES加密
def aes_encrypt(msg, dtu=1):
    """
    :param msg: 字典类型或者json类型
    :param dtu:
    :return:
    """
    try:
        if dtu is None:
            dtu = 1
        else:
            dtu = int(dtu[-1])
    except:
        dtu = 1
    try:
        rs_aes = redis.Redis(host='47.104.187.154', port=8183)
        if isinstance(msg, dict):
            jsonp = json.dumps(msg)

        if dtu == 200:
            encrypt = rs_aes.hget('encrypt', 'h5.' + str('ab28c644-bc00-4f41-b34a-5a0e4f7410d1') + '.' + str(jsonp))
        elif dtu >= 100 and dtu < 300:
            encrypt = rs_aes.hget('encrypt', 'ios.' + str('ab28c644-bc00-4f41-b34a-5a0e4f7410d2') + '.' + str(jsonp))
        else:
            encrypt = rs_aes.hget('encrypt', 'android.' + str('ab28c644-bc00-4f41-b34a-5a0e4f7410d9') + '.' + str(jsonp))

        encodestr = base64.b64encode(encrypt).decode()
        params_aes = {"qdata": encodestr}
    except:
        return ''
    else:
        return params_aes


def loginV2(host, phone, pwd):
    if not host.startswith('http'):
        url = '/'.join(['http:/', host, 'member/loginV2'])
    else:
        url = '/'.join([host, 'member/loginV2'])

    data = {
        "telephone": phone,
        "password": pwd,
        "tk": "ACEy7wYVYL9NUIQYGFBHCefhk5PeSoUlLp40NzUxNDk1MDg5NTIyNQ",
        "tuid": "Mu8GFWC_TVCEGBhQRwnn4Q",
        "from": "normal",
        "brand": "HUAWEI",
        "manufacturer": "HUAWEI",
        "model": "HUAWEI CAZ-AL10",
        "distinct_id": "679b99b1c24af85e",
        "clipboard_extend": "",
        "deviceCode": "864590036193790",
        "version": "30942000",
        "OSVersion": "7.0",
        "dtu": "014",
        "lat": "0.0",
        "lon": "0.0",
        "network": "wifi",
        "time": "1568688647421",
        "uuid": "bdfae40d314849ae9742234fce008613",
        "versionName": "3.9.42.000.0911.0031",
        "is_pure": "0"
    }

    data = dict(data, **aes_encrypt(data))

    code, ret = RequestHandler(url, data).get()

    if code == 200:
        return ret['data']['token']
    else:
        return ''
