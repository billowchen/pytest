from setuptools import setup, find_packages

setup(
    name='qute_gateway_app',
    version='1.6.1',
    author='laochenshu',
    author_email='chenyoujin@qutoutiao.net',
    description='Qute content 内容中台 相关接口封装',
    url='https://git.qutoutiao.net/autotest/qute/qute_gateway_app.git',
    packages=find_packages('app'),
    package_dir={'': 'app'}
)
