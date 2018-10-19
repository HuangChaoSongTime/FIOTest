#! /usr/bin/python
#! _*_ coding:UTF-8 _*_
'''
Created on 2018年4月17日

@author: XiangSun
'''
import os
import time
import datetime
import socket
import paramiko

#Global parameter
#Before running script,you may must allow user login Linux system by root

ip = '192.168.0.110'
username = 'root'
password = '123456'

#send command to linux system
def linux_command_send(command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for i in range(1,7):
            try:
                ssh.connect(ip, 22, username, password, timeout=5)
            except socket.timeout:
                print("Send command failed,reconnct")
                if i == 6 :
                    err = "connect to the host:%s timeout"%ip
                    print err
                    raise
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            stdin.write('Y')
            out = stdout.read()
            err = stderr.read()
            return out[:-1], err[:-1]
        except Exception, e:
            return e
        ssh.close()

#download file from linux to windows        
def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception, e:
        print e

def sys_time():
    now = datetime.datetime.now()    
    time_format = now.strftime("%Y-%m-%d-%H-%M-%S\n")
    return time_format

if __name__ == '__main__': 
    #check if '/home/result' exist
    unused_, err = linux_command_send('ls /home/result')
    if err == '':
        linux_command_send('mv /home/result /home/result_%s'%sys_time())
    elif err != '':
        linux_command_send('mkdir /home/result')
    linux_command_send('mkdir /home/result')
    # W/R model list
    w_list = ['write', 'read', 'randread', 'randwrite']
    # IO size list
    s_list = ['2048', '4096', '8192', '16384', '32768', '65536', '131072']
    for w in w_list:
        for s in s_list: 
            #check if 'D:\fio_result' exist
            out = os.path.exists('D:\\fio_result')
            if out == True:
                timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) 
                os.rename("D:\\fio_result", "D:\\fio_result_%s"%timestamp)
            elif out == False:
                os.mkdir('D:\\fio_result')  
            results, err = linux_command_send('cd /home/wx/Desktop/fio-2.1.13;./fio --filename=/dev/nvme0n1 --direct=1 -rw=%s -bs=%s -iodepth=32 --runtime=300 --time_based --numjobs=8 --group_reporting --name=test --thread --ioengine=libaio > /home/result/%s-%s.txt'%(w,s,w,s))
            iops, unused_ = linux_command_send("cat /home/result/%s-%s.txt |grep 'iops'|awk '{print $4}'"%(w,s))
            mb, unused_ = linux_command_send("cat /home/result/%s-%s.txt |grep 'aggrb'|awk '{print $3}'"%(w,s))
            mb = mb[:-1]
            #download the fio result from linux to windows
            sftp_down_file('/home/result/%s-%s.txt'%(w,s), 'D:\\fio_result\\%s-%s.txt'%(w,s))
            if err == '':
                result_flag = 'Pass'
                pass
            elif err != '':
                fo = open('D:\\fio_result\\%s-%s.txt'%(w,s), 'a+')
                fo.write("**********************************\n")
                fo.write('Error info:\n')
                fo.write(err)
                fo.close()
                result_flag = 'Fail'
            #create html report
            message = ''
            path = 'D:\\fio_result\\%s-%s.txt'%(w,s)
            fo = open("D:\\fio_result\\fio_report.html", 'a+')
            message = """<b>FIO Test result %s-%s:%s</b><br>'"""%(w,s,result_flag)
            if err == '':
                message = message + """IOPS:%sMB:%s"""%(iops, mb)
            else:
                pass
            message = message + '<a href="' + path + '"> click here to read fio report </a><br>'
            message = message + '<hr>'
            fo.write(message)
            fo.close()
            print ("%s-%s OK!"%(w,s))
