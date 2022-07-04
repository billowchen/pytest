import requests
import urllib
import json
import textwrap
from qute_core.logHandler import LogHandler
from urllib3 import encode_multipart_formdata


class RequestHandler(object):
    """
    对requests进行封装使发起http请求更加简单方便
    上传文件操作时，确保files=True

    传参格式如下：
        KEY: file
        VALUE:(文件名称，(文件路径, 二进制格式))
    param['file'] = ('new_sidecar.jmx', open("/Users/xiaowuzi/Desktop/new_sidecar.jmx", "rb").read())
    """

    def __init__(
            self, url, param, method="GET",
            header=None, need_json_dump=False, ret_json_load=True, files=False):
        """Constructs RequestHandler

        Args:
            url: URL for the :class:`Request` object to be sent.
            param: Dictionary, list of tuples or bytes to send
                   in the body of the :class:`Request`.
            method: (optional) method for the new :class:`Request` object.
                    "GET" by default
            header:(optional) Dictionary of HTTP Headers
                to send with the :class:`Request`.
            need_json_dump: (optional) True or False if the param need to
                be dumped into string before send with the :class:`Request`,
                by default it is False, as the Content-Type: application/json
                requires a python object, however some APIs require json str.
            ret_json_load:(optional) True or False if the response will be
                loaded as json before return; by default it is True,
                response will be loaded as json before return;
                if the request need to return raw response, set it to False

        Returns:
            An object which could send http request

            example:
            url = self.host + self.CouponApp.SAVE_COUPON_GROUP
            code, ret = RequestHandler(url, param).post_json()
        """

        self.url = url
        self.param = param
        self.method = method
        self.header = header
        self.need_json_dump = need_json_dump
        self.ret_json_load = ret_json_load
        self.files = files
        self.logging = LogHandler().log()

        self.form_data = ''
        self.json_data = ''

    def get(self):
        """
        发送http get请求
        """
        try:
            if self.header:
                ret = requests.get(self.url, params=self.param, headers=self.header)
            else:
                ret = requests.get(self.url, params=self.param)
            # print the request info
            self.logging.info(RequestHandler.format_prepared_request(ret.request))

            # print the response info
            self.logging.info(RequestHandler.format_response(ret))

            code = ret.status_code
            ret.encoding = 'utf-8'
            jsonRes = json.loads(ret.text)
        except Exception as e:
            self.logging.exception(e)
            return '', ''
        else:
            self.logging.info('{} 请求成功'.format(self.url))
            return code, jsonRes

    def post_json(self):
        """
        以json的方式发送post请求，
        默认发送请求参数为可JSON序列化的Python对象
        如果参数need_json_dump=True，
        则将请求参数转化为Json字符串
        """
        self.method = 'POST'

        if not self.header:
            self.header = {'Content-Type': 'application/json'}
        else:
            self.header['Content-Type'] = 'application/json'

        # 如果接口要求接收json str，必须把对象转化一下
        if self.need_json_dump:
            self.json_data = json.dumps(self.param)
        else:
            self.json_data = self.param

        return self.run_request()

    def post_json_dump(self):
        """
        以'application/json'的方式发送post请求, 请求参数以json字符串的形式发送
        """
        self.method = 'POST'

        if not self.header:
            self.header = {'Content-Type': 'application/json'}
        else:
            self.header['Content-Type'] = 'application/json'

        # 使用这个接口会强制把请求参数转化为json字符串
        self.json_data = json.dumps(self.param)

        return self.run_request()

    def post_form(self):
        """
        以form的方式发送post请求
        """
        self.method = 'POST'

        if not self.header:
            self.header = {'Content-Type': 'application/x-www-form-urlencoded'}
        else:
            self.header['Content-Type'] = 'application/x-www-form-urlencoded'

        if self.files:
            encode_data = encode_multipart_formdata(self.param)
            self.form_data = encode_data[0]
            self.header['Content-Type'] = encode_data[1]
        else:
            self.form_data = self.param

        return self.run_request()

    def run_request(self):
        """对requests.request进行封装：
                打印request和response
                处理异常
                json格式化
        """
        if self.method.upper() == 'GET' and len(self.param):
            self.url = self.url + '?' + urllib.parse.urlencode(self.param)

        try:
            ret = requests.request(
                self.method,
                self.url,
                params='',
                data=self.form_data,
                json=self.json_data,
                headers=self.header)

            # print the request info
            self.logging.info(
                RequestHandler.format_prepared_request(ret.request))

            # print the response info
            self.logging.info(RequestHandler.format_response(ret))

            code = ret.status_code
            retRes = ''
            if self.ret_json_load:
                retRes = json.loads(ret.text)
            else:
                retRes = ret.text

        except Exception as e:
            self.logging.exception(e)
            return '', ''
        else:
            return code, retRes

    @staticmethod
    def format_prepared_request(req):
        """Pretty-format 'requests.PreparedRequest'

        Pay attention at the formatting used in
        this function because it is programmed to be pretty
        printed and may differ from the actual request.

        It will pretty-print JSON objects in the body as well,
        and it labels all parts of the request.

        Example:
            res = requests.post(...)
            print(format_prepared_request(res.request))

            req = requests.Request(...)
            req = req.prepare()
            print(format_prepared_request(res.request))
        """
        headers = '\n'.join(f'{k}: {v}' for k, v in req.headers.items())
        content_type = req.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                body = json.dumps(json.loads(req.body),
                                  sort_keys=True, indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                body = req.body
        else:
            body = req.body

        formatRequest = textwrap.dedent("""
            ----------------------------------REQUEST------------------------------------
            endpoint: {method} {url}
            headers:
            {headers}
            body:
            {body}
            ----------------------------------REQUEST------------------------------------
            """).strip()
        formatRequest = formatRequest.format(
            method=req.method,
            url=req.url,
            headers=textwrap.indent(headers, '  '),
            # body=(textwrap.indent(body, ' ')
            # body=(textwrap.indent(body, ' ') if body != None else 'get请求参考url')
            body=(textwrap.indent(body, ' ') if type(body) not in [type(None), type(b'')] else 'get请求参考url')
        )
        return "\n" + formatRequest

    @staticmethod
    def format_response(resp):
        """Pretty-format 'requests.Response'

        Pay attention at the formatting used in
        this function because it is programmed to be pretty
        printed and may differ from the actual response.

        It will pretty-print JSON objects in the body,
        and it labels all parts of the response.

        Example:
            res = requests.post(...)
            print(format_response(res))
        """
        headers = '\n'.join(f'{k}: {v}' for k, v in resp.headers.items())
        content_type = resp.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            try:
                body = json.dumps(json.loads(resp.text),
                                  sort_keys=True, indent=4, ensure_ascii=False)
            except Exception:
                body = resp.text
        else:
            body = resp.text

        # 目前对于body返回bytes的情况统一按照“utf-8”来转换，
        # 如果有发现新的编码，需要再想办法处理
        if type(body) == bytes:
            body = str(body, encoding="utf-8")

        formatResponse = textwrap.dedent("""
            ----------------------------------RESPONSE-----------------------------------
            status_code: {status_code}
            headers:
            {headers}
            body:
            {body}
            ----------------------------------RESPONSE-----------------------------------
            """).strip()

        formatResponse = formatResponse.format(
            status_code=resp.status_code,
            headers=textwrap.indent(headers, '  '),
            body=textwrap.indent(body, '  '),
        )
        return "\n" + formatResponse
