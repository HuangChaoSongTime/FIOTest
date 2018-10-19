#!/usr/bin/env python
# coding:utf-8
"""
#Test Description:
# filename: Performance_test.py
# author: Huang Chaosong
# date: 2017.11.16
# verison: v1.0

#Function:
    1. auto run Performance FIO test.
    2. then each case will generate a test result with named by YearMonthDayCaseName.txt.
    3. Extracted parameters automatically(Err/IOPS/BW) and fill to a final test_result.txt.

# %AutoSetup: Is the setup of the script automatic or does the tester
# need to perform the setup manually.  Valid values are 'Y' or 'N'
# AutoSetup: Y

# %AutoScript: The approximate percentage that the script is automated.
# 0 = manual test (script only displays test step instructions)
# 100 = fully automated test.
# AutoScript: 100

# %AutoAnalysis: Is the analysis automated or does the user need to
# manually analyze the results to detrmine a pass/fail status.
# AutoAnalysis: Y

# %TestObjective: Add any of the following options separated by a semicolon:
# Feature Performance; data integrity.
# Default value is Feature.
# TestObjective: Feature

FIO test cases:
1.	Sequential write(single IO):  fio --filename=/dev/nvme0n1 -rw=write  --bs=128k  -iodepth=1 --runtime=600
2.	Sequential read(single IO):  fio --filename=/dev/nvme0n1 -rw=read  --bs=128k  -iodepth=1 --runtime=600
3.	Sequential write(multiple IOs):  fio --filename=/dev/nvme0n1 -rw=write  --bs=128k  -iodepth=32 --runtime=600
4.	Sequential read(multiple IOs):  fio --filename=/dev/nvme0n1 -rw=read  --bs=128k  -iodepth=32 --runtime=600
5.	Random read(single IO):  fio --filename=/dev/nvme0n1 -rw=randread  --bs=4k  -iodepth=1 --runtime=600
6.	Random read(multiple IO):  fio --filename=/dev/nvme0n1 -rw=randread  --bs=4k  -iodepth=32 --runtime=600
7.	Random write(single IO):  fio --filename=/dev/nvme0n1 -rw=randwrite  --bs=4k  -iodepth=1 --runtime=600
8.	Random write(multiple IO):  fio --filename=/dev/nvme0n1 -rw=randwrite  --bs=4k  -iodepth=32 --runtime=600
"""

from datetime import *
import os
import subprocess
import time
import fnmatch
import Performance_Result_Handle
import shutil

#keyword content field extract length.
content_extract = 30  # max string context
max_cutouts = 1  # max cutout string context

# create a task list
performance_test_list = ['fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_FF.fio', \
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_SW1.fio',\
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_SW32.fio',\
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_SR1.fio',\
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_SR32.fio',\
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_RW1.fio',\
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_RW32.fio',\
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_RR1.fio',\
                         'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_RR32.fio']

#create a list then one to one correspondence to name test result
filename = ['FIO_FF','FIO_SW1','FIO_SW32', 'FIO_SR1', 'FIO_SR32', 'FIO_RR1', 'FIO_RR32', 'FIO_RW1','FIO_RW32']

#the test case file location
testcase_location = "C:\\Users\\test\\Desktop\\FIO\\FIO_Test"
# the final test result location
testresult_location = Performance_Result_Handle.resultfilename +"Performace_Test_Result.txt"

# search the string in log directory.
class search:
    # define a initialize method,which path/ keyword / file format you want to search
    def __init__(self, path, search_string, file_filter,result_loc):
        self.search_path = path
        self.search_string = search_string
        self.file_filter = file_filter
        self.result_loc = result_loc
        # traversal current directory
        file_count = self.walk()

    def walk(self):
        for root, dirlist, filelist in os.walk(self.search_path,followlinks=True):
            # traversal current directory
            for filename in filelist:
                for file_filter in self.file_filter:
                    if fnmatch.fnmatch(filename, file_filter):
                        self.search_file(os.path.join(root, filename))

    # search the keyword in file
    def search_file(self, filepath):
        f = open(filepath, "r")
        # read the file content
        content = f.read()
        f.close()
        # if the keyword found, fill the filepath into final test result file.
        if self.search_string in content:
            print(filepath)
            #create finally test result file
            fo = open(self.result_loc, 'a+')
            # write the filepath in finally test result.
            fo.writelines(filepath+',')
            fo.close()
            # search the content.
            self.cutout_content(content)

    def cutout_content(self, content):
        # the keyword current position.
        current_pos = 0
        # open the finally test result and fill the keywords field.
        fo = open(self.result_loc, 'a+')
        for i in range(max_cutouts):
            try:
                pos = content.index(self.search_string, current_pos)
            except ValueError:
                break
            # handle the content string.
            content_window = content[pos: pos + content_extract]
            content_window = "".join(content_window.split(' '))
            # write the result into result file
            fo.writelines(content_window+' \n')
            continue
        fo.close()

# check the process task status
def checkprocess(task, handle,resultfilename,test_list):
    while 1:
        # check the subprocess status
        ret = subprocess.Popen.poll(task)
        if ret == 0:
            print( "the %s test case is finished" %test_list[handle])
            seq = str(task.stdout.read(),encoding='utf-8')
            for line in seq:
                # create a result file on "C:\\work\\" and Name the strings with time and extension strings
                f = open(resultfilename+filename[handle] + '.txt',"a+")
                f.writelines(line)
                f.close()
                ret1 = 0
            break
        elif ret is None:
            print( "the %s test case is running" %test_list[handle])
            if test_list[handle] is 'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_SR1.fio':
                time.sleep(600 * 3)
            else:
                time.sleep(600)
        else:
            print("the %s test case haven't create successfully" %test_list[handle])
            break
    return ret1

# empty the target disk to make sure the disk has enough free disk.
def emptytargetdisk():
    delList = []
    delDir = 'D:'
    delList = os.listdir(delDir)
    # loop in delList to remove the file.
    for f in delList:
        filePath = os.path.join(delDir, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
            print(filePath + ' was removed!')
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)
        print("Directory:" + filePath + " was removed!") 

# performace test, call the test case to run.
def performance_test():
    # checkout the fio cmd & test case directory.
    if os.path.exists('D:'):
        os.chdir('D:')
        # clean the disk.
        emptytargetdisk()
    else:
        print("the disk D: is not existed.")
        exit(0)

    for handle in range(0, len(performance_test_list)):
        # create a FIO test process.
        performance_task = subprocess.Popen(performance_test_list[handle], stdout=subprocess .PIPE, shell=True)
        # check the process status
        retprocess = checkprocess(performance_task,handle,Performance_Result_Handle.resultfilename,performance_test_list)

        if retprocess == 0:
            # each task will gap 300s
            time.sleep(300)
        else:
            continue
    print("the performance test had finished")

# handle the each test result, search the keyword to generate the finally test result.
def result_handle():
    # performance test case result path
    search_path = r"C:\\Users\\test\\Desktop\\FIO\\Log\\Performance"
    # fnmatch-Filter to match .txt test result
    file_filter = (str(datetime.now().strftime(Performance_Result_Handle.ISOTIMEFORMAT))+  "*.txt",)
    # the keyword which we want to search
    search_string = ['err', 'IOPS']
    # Do performance test
    performance_test()
    # search the keyword string in each test result
    search(search_path, search_string[0], file_filter, testresult_location)
    search(search_path, search_string[1], file_filter, testresult_location)

    print("the result handle function had finished.")

def main():
    result_handle()
    Performance_Result_Handle.main()

if __name__ == '__main__':
    main()
