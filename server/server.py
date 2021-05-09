from flask import Flask, render_template
from saveDatas import *

app = Flask(__name__)


conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')
cu = conn.cursor()
cu.execute(""" SELECT COUNT(*) AS 'Requests',
            strftime('%d', ReceiveDate) AS 'Day',
            strftime('%m', ReceiveDate) AS 'Month',
            strftime('%Y', ReceiveDate) AS 'Year'
            FROM SystemDatas
            GROUP BY 'Year', 'Month', 'Day'
            Limit 7; """)

requete1 = cu.fetchall()

cu.execute("SELECT DISTINCT userName FROM usersData")

requete2 = cu.fetchall()

conn.close()

nbrUsers = len(requete2)

# values = []

# for i in range(len(requete1)):
#     date = requete1[i][1] + "/" + requete1[i][2] + "/" + requete1[i][3]
#     # date.encode("utf-8")
#     values.append(requete1[i])

data = {
        "NameOfComputer" : getComputers()[0][1],
        "MACComputer" : getComputers()[0][0],
        "NumberOfPhisicalCPU" : getComputers()[0][3],
        "NumberOfLogicalCPU" : getComputers()[0][4],
        "HardDiskTotalSpace" : getComputers()[0][5],
        "RAMtotalSpace" : getComputers()[0][6],
        "nombreUsers" : nbrUsers,
        "value" : requete1
}



@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')
    cu = conn.cursor()

    cu.execute("SELECT NumberOfUsersOnline FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 20")

    requete3 = cu.fetchall()

    cu.execute("SELECT CPUutilisation FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 20")

    requete4 = cu.fetchall()

    cu.execute("SELECT HardDiskUSedSpace FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 20")

    requete5 = cu.fetchall()

    cu.execute("SELECT RAMusedSpace FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 20")

    requete6 = cu.fetchall()

    cu.execute("SELECT ReceiveDate FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 20")

    requete7 = cu.fetchall()

    conn.close()


    NumberOfUsersOnline=requete3
    CPUutilisation=requete4
    HardDiskUSedSpace=requete5
    RAMusedSpace=requete6
    ReceiveDate=requete7

    history = {
        "NumberOfUsersOnline" : NumberOfUsersOnline,
        "CPUutilisation" : CPUutilisation,
        "HardDiskUSedSpace" : HardDiskUSedSpace,
        "RAMusedSpace" : RAMusedSpace,
        "ReceiveDate" : ReceiveDate
    }


    return render_template('index.html.j2', data=data, history=history)


@app.route('/USERS', methods=['GET'])
def USERs():
    USER = []
    for i in range (0,nbrUsers):
        dataUser = {
            "userName" : getUsers()[i][2],
            "stat" : getUsers()[i][3],
            "usedDisk" : getUsers()[i][4],
            "usedMem" : getUsers()[i][5]
        }
        USER.append(dataUser)   
    return render_template('USERS.html.j2' , data=data, nbrUsers=nbrUsers, USER=USER)



@app.route('/CPU', methods=['GET'])
def CPUutilisation():
    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')
    cu = conn.cursor()

    cu.execute("SELECT CPUutilisation FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 10")

    requeteCPU = cu.fetchall()

    cu.execute("SELECT ReceiveDate FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 10")

    requeteDate = cu.fetchall()

    dataCPU = {
        "CPUutilisation" : requeteCPU,
        "ReceiveDate" : requeteDate
    }

    return render_template('CPUutilisation.html.j2', dataCPU=dataCPU , data=data)


@app.route('/RAM', methods=['GET'])
def RAMutilisation():
    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')
    cu = conn.cursor()

    cu.execute("SELECT RAMusedSpace_percent FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 10")

    requeteRAM = cu.fetchall()

    cu.execute("SELECT ReceiveDate FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 10")

    requeteDate = cu.fetchall()

    dataRAM = {
        "RAMusedSpace" : requeteRAM,
        "ReceiveDate" : requeteDate
    }

    return render_template('RAMutilisation.html.j2', dataRAM=dataRAM , data=data)


@app.route('/HARDDISK', methods=['GET'])
def HARDDISKutilisation():
    conn = sqlite3.connect('/home/yingqi/Desktop/monitoring/server/datasHistory.db')
    cu = conn.cursor()

    cu.execute("SELECT HardDiskUsedSpace_percent FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 10")

    requeteHARDDISK = cu.fetchall()

    cu.execute("SELECT ReceiveDate FROM SystemDatas ORDER BY ReceiveDate DESC LIMIT 10")

    requeteDate = cu.fetchall()

    dataHARDDISK = {
        "HARDDISKusedSpace" : requeteHARDDISK,
        "ReceiveDate" : requeteDate
    }

    return render_template('HARDDISKutilisation.html.j2', dataHARDDISK=dataHARDDISK , data=data)


if __name__ == '__main__':
    app.run(debug=True)
