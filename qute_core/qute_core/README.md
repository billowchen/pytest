Qute Core模块封装安装包

简介：
封装了Python的request方法,logging方法,mysql方法,configparser方法,random方法和datetime方法。


安装操作：
（1）命令行运行 `python3 setup.py install`
（2）脚本运行的同级目录下新建log文件夹


打包操作：
（1）修改setup.py文件，新增修改项
（2）命令行运行 python3 setup.py bdist_egg
（3）切换到dist文件夹，unzip core-xxx.egg 查看是否新增项打包成功