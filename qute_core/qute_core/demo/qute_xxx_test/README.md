# qute_xxx_test

### xxx 自动化测试案例
#### 测试负责人：赵玲玲 zhaolingling@qutoutiao.net

---
**命令行运行方式:**

`python3 run.py --testcase='coupon/testcase' --env='test'`

或者将参数设置好以后直接运行 `sh runTest.sh`


**注：可传参数**
1. --testcase [*必填]: 测试用例路径

    - 运行1个案例
    - 运行1个文件中的所有案例（test class）
    - 运行某个子模块（coupon）的所有案例（ignore除外）（类似daily run）
    - 运行某个子模块的P0案例（类似冒烟）
    - 运行某个业务线的所有案例（跨子模块，类似回归）

    参考如下：
    - coupon/testcase/test_demo.py::TestAccount::test_saveCouponGroup
    - coupon/testcase/test_demo.py::TestAccount
    - coupon/testcase/
    - coupon/testcase/ -marker='P0'
    - **/testcase

2. --env [*必填]: 测试环境

    确保和配置文件保持一致

3. --mark [*选填, 默认值: None]: 测试用例标记，可根据此标记搜索用例

    mark='P0'

4. --report [*选填, 默认值: None]: 生成html测试报告

    report=True

5. --db [*选填, 默认值: False]: 测试结果保存入库

    db=True




















