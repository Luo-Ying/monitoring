#!/usr/bin/python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import sys
sys.path.append("/home/yingqi/Desktop/client/monitoringapp")
import getDatas




def DetectionWarning():

    data = json.loads(getDatas.get_Data())

    if(data['HardDiskUsedSpace_percent']>85 or data['RAMusedSpace_percent']>85 or data['CPUutilisation']>85):
        if(data['HardDiskUsedSpace_percent']>85 and data['RAMusedSpace_percent']>85 and data['CPUutilisation']>85):
            # print('3')
            sendMailWrning("The CPU , HARD DISK and RAM utilization exceeds 85% !", "WARNING for HARD DISK and RAM espace !")
        elif(data['HardDiskUsedSpace_percent']>85):
            # print("1")
            sendMailWrning("The HARD DISK utilization exceeds 85% !", "WARNING for the HARD DISK")
        elif(data['RAMusedSpace_percent']>85):
            # print('2')
            sendMailWrning("The Ram utilization exceeds 85% !", "WARNING for RAM espace !")
        elif(data['CPUutilisation']>85):
            # print('2')
            sendMailWrning("The CPU utilization exceeds 85% !", "WARNING for CPU espace !")
    else:
        return 0


def sendMailWrning(Mail_content, Mail_subject):        # text: 邮件内容

    sender = 'luoyingqifr@gmail.com'     # 发件人邮箱帐号
    sender_pass = 'lyq123lyq000.'       # 发件人邮箱密码
    destination = 'yingqi.luo@alumni.univ-avignon.fr'       #收件人邮箱帐号

    # try:
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = destination
    msg['Subject'] = Mail_subject

    msg.attach(MIMEText(Mail_content, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)   # 发件人邮箱中的SMTP服务器，端口是25
    server.starttls()
    server.login(sender, sender_pass)
    server.sendmail(sender, destination, msg.as_string())    # 括号内对应的是发件人邮箱帐号、收件人邮箱帐号、发送邮件

    server.quit()   # 关闭链接

    # except Exception:   # 如果try中的语句没有执行，则会执行下面的语句
    #     print(' - Mail send failed - ')

    




# DetectionWarning()