from setuptools import setup, find_packages

setup(
    name='qute_xxx_app',
    version='1.0',
    author='Wuyiqiang',
    author_email='wuyiqiang@qutoutiao.net',
    description='Qute xxx app xxx 相关微服务接口封装',
    url='https://git.qutoutiao.net/autotest/qute/qute_xxx_app.git',
    packages=find_packages('app'),
    package_dir={'': 'app'}
)
