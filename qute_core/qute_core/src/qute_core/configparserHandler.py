import configparser


class ConfigparserHandler(object):

    def __init__(self, file):
        self.file = file
        self.config = configparser.ConfigParser()
        self.config.read(file, encoding='utf-8')

    #获取所有节点
    def get_sections(self):
        return self.config.sections()

    #获取某一节点的所有值
    def get_section_items(self, key):
        return dict(self.config.items(key))

    #获取某一节点的某一值
    def get_data(self, key, name):
        return self.config.get(key, name)

    #设置值
    def set_data(self, key, name, value):
        self.config.set(key, name, value)
        with open(self.file, 'w') as f:
            self.config.write(f)

    #添加节点
    def check_section(self, section):
        if not self.config.has_section(section):
            self.config.add_section(section)
        return True

    #是否存在节点
    def has_section(self, section):
        if self.config.has_section(section):
            return True
        else:
            return False
