import copy
from billing_app.BillingDao import BillingDao

#模板数据，为了避免污染数据，请使用深拷贝
balance = {
    "app_id": "bu2qqw21rszf",
    "uid": "100042",
    "sub_type": [
    ]
}

def getOneAccountInfo(mysql):
    """从数据库中捞取一条直播账号信息作为测试数据

    Returns:
        testData: 可以作为余额查询接口json参数的对象
        accountInfo: 直播账号的详情，可以用来做校验

    """
    testData = copy.deepcopy(balance)

    accountInfo = BillingDao(mysql).getOneAccountInfo(1)
    testData["uid"] = accountInfo["uid"]
    testData["sub_type"].append(accountInfo["sub_type"])

    return testData, accountInfo

def getQueryData(mysql, sub_account_num):
    """根据子账户个数从数据库中随机获取一个用户的账号信息并封装成测试数据返回

    Returns: 一个元组，包含两个元素：
        第一个元素可以作为余额查询接口json参数的对象
        第二个元素是一个字典，包含了用户所有子账户的账号类型和余额对
    """
    testData = copy.deepcopy(balance)
    uid = BillingDao(mysql).getOneAccountInfo(sub_account_num)["uid"]
    accountInfos = BillingDao(mysql).getAccountsByUid(uid)
    testData["uid"] = uid
    balanceInfos = {}

    for accountInfo in accountInfos:
        testData["sub_type"].append(accountInfo["sub_type"])
        balanceInfos[accountInfo["sub_type"]] = accountInfo["balance"]

    return (testData, balanceInfos)

def getWrongParams():
    """ 获取查询参数错误的测试数据列表，每条数据包含三个部分：
    1. 案例描述，将作为test id的一部分
    2. 余额查询参数
    3. 期望的返回码
    """
    empty_uid = copy.deepcopy(balance)
    empty_uid["uid"] = ""

    nonexist_id = copy.deepcopy(balance)
    nonexist_id["uid"] = "-1"

    return [
    ("empty_uid", empty_uid, 0),
    ("nonexist_uid", nonexist_id, 0)
    ]

