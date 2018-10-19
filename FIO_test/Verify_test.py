#!/usr/bin/env python
# coding:utf-8

"""
#Test Description:
#filename:Verify_test.py
# author: Huang Chaosong
# date: 2017.11.25
# verison:v1.0

#Function:
    1. auto run data integrity FIO test,
    2. then each case will generate a test result with named by YearMonthDayCaseName.txt.
    3. Extracted parameters automatically(Err/IOPS/BW) and fill to a final Testresult.txt.

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

#FIO verify Test Case:
1.	Verify test(single IO):                                                                                          \
    fio --filename=/dev/nvme0n1 -rw=randwrite --bsrange=512-128k -iodepth=1 --runtime=3600 --time_based              \
    --verify_pattern=0x12345678 --verify=crc32 --verify_fatal=1 --verify_dump=1 --verify_backlog=1
2.	Verify test(multiple IO):                                                                                        \
    fio --filename=/dev/nvme0n1 -rw=randwrite --bsrange=512-128k -iodepth=32 --runtime=3600 --time_based             \
    --verify_pattern=0x12345678 --verify=crc32 --verify_fatal=1 --verify_dump=1 --verify_backlog=1
3.	Verify test(multiple IOs for verify):                                                                            \
    fio --filename=/dev/nvme0n1 -rw=randwrite --bsrange=512-128k -iodepth=32 --runtime=72000 --time_based            \
     --verify_pattern=0x12345678 --verify=crc32 --verify_fatal=1 --verify_dump=1 --verify_backlog=32
"""

import os
import subprocess
from datetime import *
import Performance_test
import Verify_Result_Handle
import time
import shutil

# test case list
verify_list = ['fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_verify_RW1.fio', \
               'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_verify_RW32.fio', \
               'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_verifyRW32.fio']
# test case name
verify_filename = ['FIO_verify_RW1', 'FIO_verify_RW32', 'FIO_verifyRW32']
# test result of each test case
result_loc = Verify_Result_Handle.resultfilename + "Verify_Test_Result.txt"

def checkprocess(task, handle,resultfilename,test_list):
    while 1:
        # check the subprocess status
        ret = subprocess.Popen.poll(task)
        #print(ret)
        if ret == 0:
            print('the %s test case had finished' %test_list[handle])
            seq = str(task.stdout.read(),encoding='utf-8')
            for line in seq:
                # create a result file on "C:\\work\\" and Name the strings with time and extension strings
                f = open(resultfilename+verify_filename[handle] + '.txt',"a+")
                f.writelines(line)
                f.close()
                ret1 = 0
            break
        elif ret is None:
            print( "the %s test case is running" %test_list[handle])
            if test_list[handle] is 'fio C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\FIO_verifyRW32.fio':
                time.sleep(600 * 3)
            else:
                time.sleep(600)
                #continue
        else:
            print("the %s test case haven't create successfully" %test_list[handle])
            ret1 = -1
            exit(0)
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

def verify_test():
    # checkout the fio cmd & test case directory.
    if os.path.exists('D:'):
        os.chdir('D:')
        # clean the disk.
        emptytargetdisk()
    else:
        print("the disk D: is not existed.")
        exit(0)

    for handle in range(0, len(verify_list)):
        # create a FIO test process.
        verify_task = subprocess.Popen(verify_list[handle], stdout=subprocess .PIPE, shell=True)
        # check the process status
        retprocess = checkprocess(verify_task,handle,Verify_Result_Handle.resultfilename,verify_list)

        if retprocess == 0:
            # each task will gap 300s
            time.sleep(300)
        else:
            continue
    print("the performance test had finished")

def result_handle():
    # verify test case result path
    search_path = r'C:\\Users\\test\\Desktop\\FIO\\Log\\Verify'
    search_string = ['err']
    # fnmatch-Filter to match .txt test result
    # TBD TBD: we need handle the test file range more than 2 days.
    #file_filter = (str(datetime.now().strftime(Verify_Result_Handle.ISOTIMEFORMAT))+  "*.txt",)
    file_filter = "*.txt"
    # do verify test
    verify_test()
    # search the keyword string in each test result
    Performance_test.search(search_path, search_string[0], file_filter,result_loc)
    # TBD: if verify failed, we need print the expect value/ actual value

def main():
    result_handle()
    Verify_Result_Handle.main()

    print("the result_handle function had finished.")

if __name__ == '__main__':
    main()
