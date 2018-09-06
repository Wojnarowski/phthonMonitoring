#!/usr/bin/python
#coding=utf8
import paramiko
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
def getlinuxcpu(ssh):
    result=[] 
    #这里我们使用sar命令来获取CPU的使用率
    #exec_command可有三个变量可使用
    #stdin代表标准输入
    #stdout为标准输出，即命令输出的结果
    #stderr为错误输出，即执行该命令的错误信息
    stdin,stdout,stderr=ssh.exec_command('sar 2 3 |awk \'END {print 100-$NF}\'')
    #我们首先判断有无错误，如果没有则读出命令结果
    err=stderr.readlines() 
    if len(err) != 0:
        print (err)
        return False
    else:
        stdout_content=stdout.readlines()
    result= stdout_content
    #读出输出的结果后判断是否正确，有时由于超时等原因可能不会返回正确的数值
    try:
        if  len(result) !=0:
            return round(float(result[0].strip()),2)
        else:
            print ('There is something wrong when execute sar command')
    except Exception as e:
        print (e)

mail_host = "smtp.exmail.qq.com"
# 收件人
rec_user = ["zhangxianqing@czb365.com","guozhizhong@czb365.com","zhangmeng@czb365.com","kongshengmin@czb365.com","lishulei@czb365.com","jianghongwei@czb365.com","dongjixing@czb365.com","leiwenwei@czb365.com","baiguangbin@czb365.com","zhangding@czb365.com","liyueguang@czb365.com","hujiangfeng@czb365.com","tangshuai@czb365.com"]

# 发件人密码
mail_pass = "GZZasd123"
# 发件人
sender = "guozhizhong@czb365.com"
message = MIMEMultipart()
message['From'] = formataddr(["Python", sender])
message['To'] = formataddr(["Me", rec_user])
message['Subject'] = "**** 硬盘预警邮件 ****"

def send_text_to_email(msg):
    """
    发送纯文本格式邮件
    warning: 这个方法不能与发送html方法共用，如果共用以先执行的方法发送，后执行的方法无效
    :param msg:  type(str)
    """
    message.attach(MIMEText(msg, 'plain'))
    _send_email()


def _send_email():
    try:
        smtp_obj = SMTP_SSL(mail_host)
        smtp_obj.login(sender, mail_pass)
        smtp_obj.sendmail(sender, rec_user, message.as_string())
        print("邮件发送成功")
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        print ("Error: 无法发送邮件, {}".format(e))
        raise e


def getlinuxmem(ssh):
        result=[]
        stdin,stdout,stderr=ssh.exec_command('free -m |awk \' NR==2 {print (($3 - $6 - $7)/$2)*100}\'')
        err=stderr.readlines()
        if len(err) != 0:
            print (err)
            return False
        else:
            stdout_content=stdout.readlines()
        result= stdout_content
        try:
            if  len(result) !=0:
                return round(float(result[0].strip()),2)
            else:
                print ('There is something wrong when execute free command')
        except Exception as e:
            print (e)

def getlinuxspace(ssh):
        result=[]
        stdin,stdout,stderr=ssh.exec_command('df -h |awk \' NR>1 {if ($1==$NF){printf $1}else{print $0}}\'')
        err=stderr.readlines()
        if len(err) != 0:
            print (err)
            return False
        else:
            stdout_content=stdout.readlines()
        result= stdout_content
        try:
            if  len(result) !=0:
                return result
            else:
                print ('There is something wrong when execute df command')
        except Exception as e:
            print (e)


if __name__ == '__main__':
    hostname=['59.110.173.47','172.17.194.156','172.17.194.158','172.17.194.181','172.17.194.182','172.17.194.183','172.17.194.184','47.94.128.247']
    #hostname = ['59.110.173.47']
    username='deploy'
    password='czb2017'
    try:
        sysout=''
        for ip in hostname:
            #使用SSHClient方法定义ssh变量
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #连接目标服务器
            ssh.connect(hostname=ip,port=22,username=username,password=password)
            #调用getlinuxcpu函数获得服务器CPU使用率
            result=getlinuxspace(ssh)
            ssh.close()
            if result:
                #for i in result:
                    j=result[0].split()
                    #print ('The disk usage of '+j[5]+' on '+ip+' is '+j[4][0:-1]+'% Used')
                    sysout=sysout+'The disk usage of '+j[5]+' on '+ip+' is '+j[4][0:-1]+'% Used'+'\n\r'
        print(sysout)  
        send_text_to_email(sysout)          
    except Exception as e:
        print (hostname+' '+str(e))



