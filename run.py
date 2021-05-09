#!/usr/bin/python3.8
# -- coding: utf-8 -
import json
import sys
import os,time
sys.path.append("/home/yingqi/Desktop/monitoring/client")
sys.path.append("/home/yingqi/Desktop/monitoring/server")
import saveDatas
import getDatas
import sendMailWarning

# print("hi")

# 创建数据库（打开数据库）
saveDatas.createTable()


# 更新数据库
data = json.loads(getDatas.get_Data())
saveDatas.saveDatas(data)



import graph
# 删除过老的数据
saveDatas.EraseOld()


# 监控系统发送警示邮件
sendMailWarning.DetectionWarning()


# graph
# while(True):
    # os.system('python3 /home/yingqi/Desktop/monitoringapp/graph.py')
    # time.sleep(5)



