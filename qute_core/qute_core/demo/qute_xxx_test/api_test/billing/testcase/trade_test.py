# import allure
# import pytest
# import json
# from api_test.accountsystem.testdata import trade_data
# from qute_core.logHandler import LogHandler
# from accountsystem_app.AccountSystemAppCaller import AccountSystemAppCaller

# #from coupon_app.CouponDao import CouponDao

# logging = LogHandler().log()


# @allure.feature('账号交易')
# class TestTrade(object):
#     """账户交易
#     http://km.qutoutiao.net/pages/viewpage.action?pageId=94009989
#     """

#     @pytest.mark.P1
#     @pytest.mark.owner_zhaolingling
#     @allure.story('账号交易')
#     def ntest_Trade_success(self, request, check_ret):
#         #构造数据
#         data = trade_data.trade
#         #获取accountsystemappcaller和MysqlHandler对象
#         host, mysql_check = check_ret
#         accountSystemAppCaller = AccountSystemAppCaller(host)
#         #发起请求
#         ret, url =accountSystemAppCaller.trade(data)
#         setattr(request.node, 'url', url)

#         #校验返回码
#         assert ret['code'] == 0


#         # #获取数据库数据
#         # couponGroupId = ret['data']['coupon_group_id']
#         # newCouponGroup = CouponDao(mysql_check).getCouponGroupByGroupId(couponGroupId)
#         #
#         # #校验数据库数据
#         # assert newCouponGroup['status'] == 1
#         # assert newCouponGroup['coupon_group_id'] == couponGroupId
#         # assert newCouponGroup['memo'] == data['memo']
#         # assert newCouponGroup['price_limit'] == data['price_limit']
