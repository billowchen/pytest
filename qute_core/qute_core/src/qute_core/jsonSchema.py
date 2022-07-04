from qute_core.logHandler import LogHandler
from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

#在线生成json schema
#https://jsonschema.net/#/editor

#json schema文档
#https://blog.csdn.net/silence_xiao/article/details/81303935
#https://www.cnblogs.com/ChangAn223/p/11234348.html

# demo参考：

# (1) key对应的值为 固定的值
# data = {
#           "a": 1,
#           "b": 2
#        }

# JsonSchema(data, *["a"], **{"a": {"type": "integer", "enum": [1]}}, ).verify()

# (2) key对应的值为 字典
# data = {
#           "a": {"b": 1},
#           "c": '2'
#        }
#
# check_rule = {
# 	"a": {
# 		"type": "object",
# 		"properties": {
# 			"b": {
# 				"type": "integer",
# 				"enum": [1]
# 			}
# 		},
# 		"required": ["b"]
# 	},
# 	"c": {
# 		"type": "string",
# 		"enum": ["2"]
# 	}
# }
#
# JsonSchema(data, *["a", "c"], **check_rule, ).verify()

# (3) key对应的值为 列表
# data = {
#           "a": {"b": [{"key": 1, 'name': 'qtt'}, {"key": 2, 'name': 'qtt'}]},
#           "c": '2'
#        }
#
# check_rule = {
# 	"a": {
# 		"type": "object",
# 		"properties": {
# 			"b": {
# 				"type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "key": {
#                             "type": "integer",
#                             "enum": [1, 2, 3]
#                         },
#                         "name": {
#                             "type": "string",
#                             "enum": ["qtt"]
#                         }
#                     },
#                     "required": ["key", 'name']
#                     }
#                 }
# 			},
#         "required": ["b"]
#     }
# }
#
# JsonSchema(data, *["a"], **check_rule, ).verify()

logging = LogHandler().log()


class JsonSchema:
    template = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'json schema template',
        'description': 'json schema template',
        'type': 'object',
        'properties': '',
        'required': []
    }

    def __init__(self, ret, *args, **kwargs):
        self.ret = ret
        self.flag = True
        self.template['properties'] = kwargs
        if self.template['required']:
            self.template['required'] = []
        self.template['required'].extend(args)

    def verify(self):
        try:
            validate(instance=self.ret, schema=self.template)
        except SchemaError as e:
            logging.exception("验证模式schema出错：\n出错位置：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
            self.flag = False
        except ValidationError as e:
            logging.exception("json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
            self.flag = False
        else:
            logging.info('验证成功！')
        finally:
            return self.flag
