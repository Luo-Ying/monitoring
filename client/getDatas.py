#!/usr/bin/python3.8
# -- coding: utf-8 -

# import array

import psutil

import socket

# import subprocess

import os

from uuid import getnode as get_mac

# import time

import json


DATAs = []
# date = {}
users_data = []         #用户信息存入表


# 获取时间/日期
# localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
# date["Local time"] = localtime 
    

def bytes2human(n):
    '''内存单位转换的方法'''
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n




def get_Data():

    # 获取mac地址
    mac = str(get_mac())
    
    # 获取主机名字
    hostName = socket.gethostname()

    # 获取在线用户
    bashCommand_usersConnecteCounter = os.popen("who | sort --key=1,1 --unique | wc --lines").read().strip('\n')

    # 获取在线用户名字列表
    bashCommand_userConnecteList = os.popen("who | awk '{print $1}'").read().strip('\n')
    bashCommand_allUserList = os.popen("cat /etc/passwd|grep -v nologin| awk -F ':' '$3 >= 1000{print $1}'").read().strip('\n')
    # 将用户存入用户数组
    # 在线用户
    userConnecteList = bashCommand_userConnecteList.split( )
    # 所有用户
    userAllList = bashCommand_allUserList.split( )      # 该数组从元素[1]开始后面的为用户，元素[0]是时间戳

    for i in range(len(userAllList)):
        user_data = {}
        user_data["userName"] = userAllList[i]
        if(userAllList[i] in userConnecteList):
            user_data["stat"] = "online"
            user_data["usedMem"] = "0"
        else:
            user_data["stat"] = "offline"
            user_data["usedMem"] = "0"
        users_data.append(user_data)        # 将信息添加进用户信息表

    # 获取系统cpu使用率
    cpu_count_phisique = psutil.cpu_count( logical=False )  #cpu物理数量
    #cpu逻辑数量
    bashCommand_treadsCounter = os.popen("cat /proc/cpuinfo | awk '/^processor/{print $3}' | wc -l").read().strip('\n')
    #nterval指定的是计算cpu使用率的时间间隔, percpu指定是选择总的使用率还是每个cpu的使用率
    # percpu为True的时候，会返回每一个CPU的使用率，而为False则是总使用率
    cpu_percent = psutil.cpu_percent( interval = 1 )    #该机返回两个值（双核）


    # 获取硬盘内存使用情况
    disk_usage = psutil.disk_usage('/')         
    disk_total = bytes2human(disk_usage.total)      #总内存
    disk_used = bytes2human(disk_usage.used)        #已用内存
    disk_percent = disk_usage.percent               #已用内存占百分比
    disk_free = bytes2human(disk_usage.free)        # 剩余内存

    # 获取RAM使用情况
    RAM_usage = psutil.virtual_memory()
    RAM_total = bytes2human(RAM_usage.total)      #总内存
    RAM_used = bytes2human(RAM_usage.used)        #已用内存
    RAM_percent = RAM_usage.percent               #已用内存占百分比
    RAM_free = bytes2human(RAM_usage.free)        # 剩余内存


    # 获取每个用户磁盘使用情况
    bashCommand_usedDiskbyUsers = os.popen("sudo du -sh /home/* | awk -F '/' '{print $1}'").read().strip('\n')
    bashCommand_user = os.popen("sudo du -sh /home/* | awk -F '/' '{print $3}'").read().strip('\n')
    # print(bashCommand_usedDiskbyUsers)
    usedDiskbyUsers = bashCommand_usedDiskbyUsers.split( )
    users = bashCommand_user.split( )
    for i in range(len(usedDiskbyUsers)):
        for j in range (len(users_data)):
            if(users[i] == users_data[j]["userName"]):
                users_data[j]["usedDisk"] = usedDiskbyUsers[i]
            

    # 获取每个用户内存使用情况
    bashCommand_usedMembyUsers = os.popen("/home/yingqi/Desktop/monitoring/client/mem.sh").read().strip('\n')
    bashCommand_usedMemUsers = os.popen("/home/yingqi/Desktop/monitoring/client/mem_nom.sh").read().strip('\n')
    usedMembyUsers = bashCommand_usedMembyUsers.split( )
    #print(usedMembyUsers)
    users = bashCommand_usedMemUsers.split( )
    #print(users,usedMembyUsers)
    
    for i in range (len(users)):
        for j in range (len(users_data)):
            if (users[i]==users_data[j]["userName"]):
                users_data[j]["usedMem"] = usedMembyUsers[i]  
                
        

    jsonDATAs = json.dumps(
    {
        "MacAdresse" : str(mac),
        "NameOfComputer" : str(hostName),
        "NumberOfUsersOnline" : int(bashCommand_usersConnecteCounter),
        "NumberOfPhisicalCPU" : int(cpu_count_phisique),
        "NumberOfLogicalCPU" : int(bashCommand_treadsCounter),
        "CPUutilisation" : int(cpu_percent),
        "HardDiskTotalSpace" : str(disk_total),
        "HardDiskUSedSpace" : str(disk_used),
        "HardDiskUsedSpace_percent" : int(disk_percent),
        "HardDiskAvailableSpace" : str(disk_free),
        "RAMtotalSpace" : str(RAM_total),
        "RAMusedSpace" : str(RAM_used),
        "RAMusedSpace_percent" : int(RAM_percent),
        "RAMavailableSpace" : str(RAM_free),
        "user":users_data
    }, indent=4, sort_keys=True)

    return jsonDATAs



# print(get_Data())
# print(psutil.net_io_counters())
# print(psutil.net_io_counters()[1])
# print(psutil.net_io_counters()[0])