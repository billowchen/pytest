from setuptools import setup, find_packages

setup(
    name='qute_core',
    version='1.6.1',
    author='Wuyiqiang',
    author_email='wuyiqiang@qutoutiao.net',
    description='Qute core',
    url='https://git.qutoutiao.net/autotest/qute/qute_qute_core.git',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        '': ['*.conf'],
    }
)
