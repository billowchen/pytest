import copy
import json
import datetime
from qute_core.logHandler import LogHandler

#日志收集器
logging = LogHandler().log()
currtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')


#模板数据，为了避免污染数据，请使用深拷贝
data = {
            "token": "4df3UVHn_L6wMf-2m1RBjvQ1NTteuMMrOSlxRK4MqyE5phQznNTAbbXypyk11TrfijMochS8zhiindWXbgGXg4yOIIifo8rPWn_xyjl2aw",
            "dtu": "200",
            "product": "dd",
            "category": "first_audit",
            "contentId": "5555556",
            "genre": "short_video",
            "auditEnter": "queue",
             "action": "1"
            }

def getAuditAuditData():
    """
    Returns:
        testData: 可以作为图文入库接口json参数的对象
    """
    testData = copy.deepcopy(data)
  #  testData.update(contentId=contentid)
    return testData



