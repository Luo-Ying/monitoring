#!/usr/bin/python3
import rrdtool
import time
import sqlite3
import os

# print("hi")

def creat(rrdFile):

    # create filename [--start|-b start time] [--step|-s step] [DS:ds-name:DST:heartbeat:min:max] [RRA:CF:xff:steps:rows]
    # filename创建的rrdtool数据库文件名，默认后缀为.rrd;
    # --start 指定rrdtool第一条记录的起始时间，必须是timestamp的格式；
    # --step 指定rrdtool每隔多长时间就收到一个值，默认为5分钟；
    # 数据写频率--step为300秒（即5分钟一个数据点）
    rrd = rrdtool.create(rrdFile, "--start=now-1800", "--step=1", 
    # 定义数据源 flow （数据量）; 类型都为 GAUGE（真实值）; 300秒为心跳值，
    # 其含义是300秒没有收到值，则用 UNKNOWN 代替；0为最小值；最大值用U代替，表示不确定 
        'DS:ds1:GAUGE:300:0:U',
        
        # RRA定义格式为[RRA：CF：xff：steps：rows]，CF定义了AVERAGE、MAX、MIN、LAST四种数据合并方式
        # xff定义为0.5,表示一个CDP中的PDP值如超过一半值为UNKNOWN，则该CDP的值就被标为UNKNOWN
        # 每隔5分钟（1*300秒）存一次数据的最新值，存600笔，即2.08天
        'RRA:LAST:0.5:1:600',
        'RRA:LAST:0.5:3:400',
        'RRA:LAST:0.5:6:300')

    if(not rrd):
        print(rrdtool.OperationalError())
        # print(rrdtool.ProgrammingError)





def fetch(rrdFile):

    rrd_result = rrdtool.fetch(rrdFile, "LAST", "--start=now-60", "--end=now")

    print(rrd_result)




# def graph(title, pngFile, rrdFile):

    # rrdtool.graph(pngFile, "--start=now-1800", "--end=now", 
    # "--width=600", "--height=200", "--title", title, 
    # "--vertical-label=G/used", 
    # "DEF:vtest",rrdFile)



def getDataSelected(dataSelected):

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()

    cu.execute(dataSelected)

    result = cu.fetchall()

    conn.commit()

    conn.close()

    return result





def graph(dataColor, infoColor, dataType, dataSelected, rrdFile, pngFile):

    data=getDataSelected(dataSelected)
    # creat(rrdFile)
    # print(data)

    # starttime = int(time.time())
    # fetch(rrdFile)
    for i in range(len(data)):
        # print("\033[1;%s;40m%s\033[0m"%(dataColor,data[i][0]))
        rrdtool.update(rrdFile, 'N:%s'%(str(data[i][0])))
        # 数据有几个DS， N后面就有几个value
        # starttime+=10

    title = dataType + time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # fetch(rrdFile)

    rrdtool.graph(pngFile, "--start=now-60", "--end=now", 
                "--width=600", "--height=200", "--title", title, 
                "--vertical-label=(%)/used", 
                "DEF:vtest={}:ds1:LAST".format(rrdFile), 
                "LINE:vtest%s:%s"%(infoColor,dataType))





bashCommand_listF = os.popen("ls /home/yingqi/Desktop/monitoring/server").read().strip('\n')
listF = bashCommand_listF.split()



# CPU
rrdFileCPU = 'usedCPU.rrd'
rrdFile_CPU = "/home/yingqi/Desktop/monitoring/server/usedCPU.rrd"
pngFile_CPU = "/home/yingqi/Desktop/monitoring/server/usedCPU.png"
dataSelected_CPU = " SELECT CPUutilisation FROM SystemDatas ORDER BY ReceiveDate DESC; "
dataType_CPU = "CPU utilisation"
dataColor_CPU = "31"
infoColor_CPU = "#ff0000"
if(rrdFileCPU not in listF):
    creat(rrdFile_CPU)
graph(dataColor_CPU , infoColor_CPU, dataType_CPU ,dataSelected_CPU,rrdFile_CPU,pngFile_CPU)


# HARDDISK
rrdFileHARDDISK = 'usedHARDDISK.rrd'
rrdFile_HARDDISK = "/home/yingqi/Desktop/monitoring/server/usedHARDDISK.rrd"
pngFile_HARDDISK = "/home/yingqi/Desktop/monitoring/server/usedHARDDISK.png"
dataSelected_HARDDISK = " SELECT HardDiskUsedSpace_percent FROM SystemDatas ORDER BY ReceiveDate DESC; "
dataType_HARDDISK = "HARD_DISK utilisation"
dataColor_HARDDISK = "33"
infoColor_HARDDISK = "#efc377"
if(rrdFileHARDDISK not in listF):
    creat(rrdFile_HARDDISK)
graph(dataColor_HARDDISK ,infoColor_HARDDISK, dataType_HARDDISK ,dataSelected_HARDDISK,rrdFile_HARDDISK,pngFile_HARDDISK)



# RAM
rrdFileRAM = 'usedRAM.rrd'
rrdFile_RAM = "/home/yingqi/Desktop/monitoring/server/usedRAM.rrd"
pngFile_RAM = "/home/yingqi/Desktop/monitoring/server/usedRAM.png"
dataSelected_RAM = " SELECT RAMusedSpace_percent FROM SystemDatas ORDER BY ReceiveDate DESC; "
dataType_RAM = "RAM utilisation"
dataColor_RAM = "35"
infoColor_RAM = "#e979fa"
if(rrdFileRAM not in listF):
    creat(rrdFile_RAM)
graph(dataColor_RAM ,infoColor_RAM, dataType_RAM ,dataSelected_RAM,rrdFile_RAM,pngFile_RAM)
