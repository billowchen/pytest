import json
import jsonpath
from qute_core.logHandler import LogHandler
#Demo参考
"""
data = {
    "lemon": {
        "teachers": [
            {
                "id": "101",
                "name": "华华",
                "age": 25,
                "addr": "sh"
            },
            {
                "id": "102",
                "name": "韬哥",
                "age": 28,
                "addr": "sh2"
            }
        ],
        "salesmans": [
            {
                "id": "105",
                "name": "毛毛",
                "age": 17
            },
            {
                "id": "106",
                "name": "大树",
                "age": 27
            }
        ]
    },
    "avg": 25
}
获取lemon/teachers下所有的name
print(JsonPath(data).get_param('$.lemon.teachers.[*].name'))
获取所有的name
print(JsonPath(data).get_param('$..name'))
获取所有lemon
print(JsonPath(data).get_param('$.lemon.*'))
获取所有lemon的age
print(JsonPath(data).get_param('$.lemon..age'))
获取lemon下第二个索引的teachers
print(JsonPath(data).get_param('$.lemon.teachers[1]'))
获取lemon/teachers下addr='sh'的age
print(JsonPath(data).get_param('$.lemon.teachers[?(@.addr=="sh")].age'))
获取lemon/teachers下age>20
print(JsonPath(data).get_param('$.lemon.teachers[?(@.age>20)]'))
"""


class JsonPath:
    def __init__(self, ret):
        self.logging = LogHandler().log()
        if not isinstance(ret, dict):
            try:
                ret = json.loads(ret)
            except Exception as e:
                self.logging.info('请输入字典或者json类型数据')
        self.ret = ret

    def get_param(self, command):
        value = jsonpath.jsonpath(self.ret, command)
        return value[0] if isinstance(value, list) else ''
