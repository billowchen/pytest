
class _const:
    """
    该类定义了重新定义了一些内置方法,和一个异常ConstError, ConstError类继承
    自类TypeError.
    参考：https://www.malike.net.cn/blog/2013/11/03/python-constants/
    """
    class ConstError(TypeError):pass

    def __setattr__(self,name,value):
        """
        通过调用类自带的字典__dict__, 判断定义的常量是否包含在字典中。
        如果字典中包含此变量，将抛出异常，否则，给新创建的常量赋值。
        """
        if name in self.__dict__:
            raise self.ConstError(f"Can't rebind const '{name}'!")
        else:
            self.__dict__[name]=value

    def __delattr__(self, name):
        """
        定义删除属性的方法，若删除常量类的属性，则抛出异常
        """
        if name in self.__dict__:
            raise self.ConstError(f"Can't unbind const instance attribute '{name}'!")
        else:
            raise AttributeError(f"const instance has no attribute '{name}'!")

    def _setattr_impl(self, name, value):
        """
        定义一个禁止绑定属性的实现
        其原理为继承_const对象初始化完成后将__setattr__设置为禁止绑定属性的实现
        注意：若在_const类中实现__setattr__为禁止绑定属性，则__init__也将无法初始化（绑定）对象属性
        """
        if name in self.__dict__:
            raise self.ConstError(f"Can't rebind const '{name}'!")
        else:
            raise self.ConstError(f"Can't bind const instance new attribute '{name}'!")