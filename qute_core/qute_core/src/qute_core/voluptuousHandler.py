from voluptuous import Schema, MultipleInvalid, Required, All, Range
from qute_core.logHandler import LogHandler

#参考文档
#http://ddrv.cn/a/159185/

#demo
# schema = {
#     'q': All(str),
#     Required('page'): Schema({"page": All(int, 1)}),
#     Required('list'): Schema({"list": All(list, [1, 2, 3]), 'page': All(int, Range(1, 10))})
# }
#
# data = {'q': 'hello', 'page': {"page": 1}, 'list': {"list": [1, 2, 3], 'page': 11}}
#
# schema(data)

logging = LogHandler().log()


class VoluptuousHandler:
    def __init__(self, ret, **kwargs):
        self.ret = ret
        self.schema = Schema(kwargs)

    def check(self):
        try:
            self.schema(self.ret)
        except MultipleInvalid as e:
            logging.exception('/'.join([str(i) for i in e.path]), e.error_message)
        else:
            logging.info('校验成功')



