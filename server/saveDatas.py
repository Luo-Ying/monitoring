#!/usr/bin/python3.8
# -- coding: utf-8 -
import sqlite3
import json
import datetime
import sys
sys.path.append("/home/yingqi/Desktop/monitoring/client")
import getDatas

def createTable():

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')     # 创建数据库（打开数据库）
    # 要使用这个模块，必须先创建一个Connection对象，它代表数据库，将数据存储在'datasHistory.db'文件中

    cu = conn.cursor()
    # 有了Connection对象后，创建一个Cursor游标对象，然后调用它的execute（）方法执行SQL语句

    try:
        create_tb_cmd = '''CREATE TABLE SystemDatas(
            MacAdresse text,
            ReceiveDate date,
            NameOfComputer text,
            NumberOfUsersOnline int,
            NumberOfPhisicalCPU int,
            NumberOfLogicalCPU int,
            CPUutilisation int,
            HardDiskTotalSpace text,
            HardDiskUSedSpace text,
            HardDiskUsedSpace_percent int,
            HardDiskAvailableSpace text,
            RAMtotalSpace text,
            RAMusedSpace text,
            RAMusedSpace_percent int,
            RAMavailableSpace text);'''

        # 创建表
        cu.execute(create_tb_cmd)
    
    except:
        # print("Create table failed, table already exist")
        return False

    try:
        create_tb_cmd = '''CREATE TABLE usersData(
            macAdresse text,
            receiveDate date,
            userName text,
            stat text,
            usedDisk text,
            usedMem text);'''

        cu.execute(create_tb_cmd)

    except:
        # print("Create table failed, table already exist")
        return False

    conn.commit()   # save (commit) the changes

    # We can also clode the connection if we are done with it
    # Just be sure any changes have been committed or they will be lost
    conn.close()




def saveDatas(JsonIn):

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()


    cu.execute(""" INSERT INTO SystemDatas VALUES (
            :MacAdresse,
            :ReceiveDate,
            :NameOfComputer,
            :NumberOfUsersOnline,
            :NumberOfPhisicalCPU,
            :NumberOfLogicalCPU,
            :CPUutilisation,
            :HardDiskTotalSpace,
            :HardDiskUSedSpace,
            :HardDiskUsedSpace_percent,
            :HardDiskAvailableSpace,
            :RAMtotalSpace,
            :RAMusedSpace,
            :RAMusedSpace_percent,
            :RAMavailableSpace) """,{
                'MacAdresse' : JsonIn['MacAdresse'],
                'ReceiveDate' : datetime.datetime.now(),
                'NameOfComputer' : JsonIn['NameOfComputer'],
                'NumberOfUsersOnline' : JsonIn['NumberOfUsersOnline'],
                'NumberOfPhisicalCPU' : JsonIn['NumberOfPhisicalCPU'],
                'NumberOfLogicalCPU' : JsonIn['NumberOfLogicalCPU'],
                'CPUutilisation' : JsonIn['CPUutilisation'],
                'HardDiskTotalSpace' : JsonIn['HardDiskTotalSpace'],
                'HardDiskUSedSpace' : JsonIn['HardDiskUSedSpace'],
                'HardDiskUsedSpace_percent' : JsonIn['HardDiskUsedSpace_percent'],
                'HardDiskAvailableSpace' : JsonIn['HardDiskAvailableSpace'],
                'RAMtotalSpace' : JsonIn['RAMtotalSpace'],
                'RAMusedSpace' : JsonIn['RAMusedSpace'],
                'RAMusedSpace_percent' : JsonIn['RAMusedSpace_percent'],
                'RAMavailableSpace' : JsonIn['RAMavailableSpace']
            })
    
    for i in range(len(JsonIn['user'])):
        cu.execute(""" INSERT INTO usersData VALUES (
                :macAdresse,
                :receiveDate,
                :userName,
                :stat,
                :usedDisk,
                :usedMem) """,{
                    'macAdresse' : JsonIn['MacAdresse'],
                    'receiveDate' : datetime.datetime.now(),
                    'userName' : JsonIn['user'][i]['userName'],
                    'stat' : JsonIn['user'][i]['stat'],
                    'usedDisk' : JsonIn['user'][i]['usedDisk'],
                    'usedMem' : JsonIn['user'][i]['usedMem'],
                })
    
    conn.commit()

    conn.close()





def dropTable():

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()

    cu.execute(''' DROP TABLE  SystemDatas ''')     # 删除表

    cu.execute(''' DROP TABLE  usersData ''')

    conn.commit()

    conn.close()



def getTable():

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()

    cu.execute("SELECT * from SystemDatas")

    result = cu.fetchall()  # 返回多个元组，即返回多条记录（rows），如果没有结果，则返回（）

    cu.execute("SELECT * from usersData")

    result += cu.fetchall()  # 返回多个元组，即返回多条记录（rows），如果没有结果，则返回（）


    conn.commit()

    conn.close()
    
    return result




def getComputers():

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()

    cu.execute(''' SELECT DISTINCT
                        MacAdresse,
                        NameOfComputer,
                        NumberOfUsersOnline,
                        NumberOfPhisicalCPU,
                        NumberOfLogicalCPU,
                        HardDiskTotalSpace,
                        RAMtotalSpace 
                    FROM SystemDatas 
                    ORDER BY ReceiveDate DESC; ''')

    result = cu.fetchall()

    conn.commit()

    conn.close()

    return result



def getUsers():

    data = json.loads(getDatas.get_Data())

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()

    for i in range(len(data['user'])):
        cu.execute(''' SELECT DISTINCT
                            macAdresse,
                            receiveDate,
                            userName,
                            stat,
                            usedDisk,
                            usedMem
                        FROM usersData 
                        ORDER BY ReceiveDate DESC; ''')

    result = cu.fetchall()

    conn.commit()

    conn.close()

    return result





def showTable():

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()

    cu.execute("SELECT * FROM SystemDatas")

    print(json.dumps(cu.fetchall(), indent=4, sort_keys=True))

    cu.execute("SELECT * FROM usersData")

    print(json.dumps(cu.fetchall(), indent=4, sort_keys=True))

    conn.commit()

    conn.close()





def EraseOld():

    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')

    cu = conn.cursor()

    cu.execute(''' DELETE 
                FROM
                    SystemDatas
                WHERE
                    ReceiveDate <= DATE('now', '-7 day'); ''')

    cu.execute(''' DELETE 
                FROM
                    usersData
                WHERE
                    ReceiveDate <= DATE('now', '-7 day'); ''')
                
    conn.commit()

    conn.close()




# dropTable()
# createTable()
# data = json.loads(getDatas.get_Data())
# saveDatas(data)
# showTable()
# print(getTable())
# showTable()
# print(getComputers()[0][0])
# print(getUsers())
# print(getUsers()[0])
# print(getUsers()[1])
# print(getUsers()[2][2])
