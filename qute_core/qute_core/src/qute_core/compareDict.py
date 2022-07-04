from qute_core.jsonPath import JsonPath
from qute_core.logHandler import LogHandler


class CompareDict:
    def __init__(self, data1, data2):
        '''
        :param data1: 待校验的字典
        :param data2: 待比较的字典
        '''
        self.data1, self.data2 = data1, data2
        self.jp1, self.jp2 = JsonPath(data1), JsonPath(data2)
        self.path_list1, self.path_list2, self.diff_path_list = [], [], []#data1的所有路径,data2的所有路径 #不正确值的路径
        self.logging = LogHandler().log()

    #获取dict的所有路径
    def get_data_path(self):
        try:
            for key, value in self.data1.items():
                self.path_list1.extend(self.get_dict_path(value, [key], [])) if isinstance(value, (list, dict)) else self.path_list1.append(key)
            for key, value in self.data2.items():
                self.path_list2.extend(self.get_dict_path(value, [key], [])) if isinstance(value, (list, dict)) else self.path_list2.append(key)
        except Exception as e:
            self.logging.exception('请输入字典类型数据')

    #递归获取data的所有字典/列表类型的路径
    def get_dict_path(self, data, keys, result):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    keys.append(key)
                    self.get_dict_path(value, keys, result)
                elif isinstance(value, list):
                    for v in value:
                        if isinstance(v, (list, dict)):
                            keys.append(key)
                            self.get_dict_path(v, keys, result)
                        else:
                            keys.append(key)
                            result.append('.'.join(keys)) if '.'.join(keys) not in result else ''
                            keys.pop(-1)
                else:
                    keys.append(key)
                    result.append('.'.join(keys))
                    keys.pop(-1)
            keys.pop(-1)
        else:#list
            for v in data:
                if isinstance(v, (dict, list)):
                    self.get_dict_path(v, keys, result)
                else:
                    result.append('.'.join(keys)) if '.'.join(keys) not in result else ''

        return result

    #获取dict1和dict2共同的，新增的和移除的path
    def get_diff_path(self, data1, data2, flag=True):
        self.get_data_path() if flag else ''
        common_path = set(data1) & set(data2)
        add_path = set(data1) - set(data2)
        remove_path = set(data2) - set(data1)

        return {'common': list(common_path), 'add': list(add_path), 'remove': list(remove_path)}

    #校验data1,data2数据
    def check_data(self):
        path_list = self.get_diff_path(self.path_list1, self.path_list2)
        for category, paths in path_list.items():
            for path in paths:
                value1, value2 = self.jp1.get_param(f'{path}'), self.jp2.get_param(f'{path}')
                if category == 'common':
                    if isinstance(value1, list):
                        if isinstance(value2, list):
                            len1, len2 = len(value1), len(value2)
                            data_list = self.get_diff_path(value1, value2, flag=False)
                            if len1 == len2:
                                if len(data_list['common']) != len1:
                                    if len(set(value1)) != len1:#value1有数据重复
                                        self.logging.info(f'路径：{path},值为列表，且存在重复的值')
                                        self.diff_path_list.append(f'(repeat, {path}, ({value1},{value2}))')
                                    else:
                                        self.logging.info(f'路径：{path},值为列表，存在不匹配的值')
                                        self.diff_path_list.append(f'(change, {path}, ({data_list["add"]},{data_list["remove"]}))')
                            else:
                                mark = 'add' if len1 > len2 else 'remove'
                                self.logging.info(f'路径：{path},值为列表，存在不匹配的值')
                                self.diff_path_list.append(f'({mark}, {path}, ({data_list["add"]},{data_list["remove"]}))')
                        else:
                            self.logging.info(f'路径：{path}, 校验值不匹配')
                            self.diff_path_list.append(f'(change, {path}, ({value1}, {value2}))')
                    else:
                        if value1 != value2:
                            self.logging.info(f'路径：{path}, 校验值不匹配')
                            self.diff_path_list.append(f'(change, {path}, ({value1}, {value2}))')
                else:
                    info = f'路径：{path} 为新增项, ({value1}, {value2})' if type == 'add' else self.logging.info(f'路径：{path} 为移除项, ({value1}, {value2})')
                    self.logging.info(info)
                    self.diff_path_list.append(f'({category}, "", ({path}, {value1}{value2})')
        return self.diff_path_list
