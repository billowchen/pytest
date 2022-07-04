from qute_core.const import _const
class _gateway_app(_const):
    def __init__(self):
        # 获取产品配置
        self.auditGetProduct = '/page/audit/getproduct'

        #数据概览统计
        self.auditStatistics= '/page/audit/statistics'

       #获取配置信息
        self.auditConfig = '/page/audit/config'

        #获取列表
        self.auditList = '/page/audit/list'

        #获取详情
        self.auditView = '/page/audit/view'

        #退出审核
        self.auditQuit = '/page/audit/quit'

        #审核提交
        self.auditAudit = '/page/audit/audit'

        # 审核记录产品配置
        self.authorityRecord = '/page/authority/record'

        # 获取审核记录配置信息
        self.recordConfig = '/page/record/config'

       #审核记录列表
        self.recordList = '/page/record/list'

        #审核记录详情
        self.recordView = '/page/record/view'

        # 审核记录提交
        self.recordAudit = '/page/record/audit'

        #获取审核操作记录
        self.recordOperation = '/page/record/operation'