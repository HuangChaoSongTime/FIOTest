#!/usr/bin/env python
# coding:utf-8

# filename: Verify_Result_Handle.py
# author: Huang Chaosong
# date: 2017.11.22
# verison:1.0

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
# Feature Performance data integrity.
# Default value is Feature.
# TestObjective: Feature

import re

# define dict structure for ecah test case
FIO_verify_RW1 = {"err":0}
FIO_verify_RW32 = {"err":0}
FIO_verifyRW32 = {"err":0}

# define FIO test list to fill plt xlable.
FIOTestList = [FIO_verify_RW1, FIO_verify_RW32, FIO_verifyRW32]
# define the time formate to generate each test case result file.
ISOTIMEFORMAT = '%Y%m%d'
#define the string that we want to search
err_str = 'err='

#resultfilename = 'C:\\work\\log\\Verify\\' + str(datetime.now().strftime(Performance_Result_Handle.ISOTIMEFORMAT))
resultfilename = 'C:\\Users\\test\\Desktop\\FIO\\Log\\Verify\\'

def result_fill(fo):
    while True:
        line=fo.readline()
        line = ",".join(line.replace(' ', '').split(':'))
        if line:
            #search the string in line
            if line.find('FIO_verify_RW1') > 0:
                if line.find(err_str) > 0 :
                    #find the string index in line
                    indexStr = line.find(err_str)
                    #cut out the string and get the value for string
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str) + 4])

                    #fill it into current test case result dict
                    FIO_verify_RW1["err"] = value.replace(',', '')
                    if int(FIO_verify_RW1["err"]) > 0:
                        print("the case FIO_verify_RW1 had Failed!")

            # search the string in line
            elif line.find('FIO_verify_RW32') > 0:
                if line.find(err_str) > 0 :
                    #find the string index in line
                    indexStr = line.find(err_str)
                    #cut out the string and get the value for string
                    value = re.sub("\D","",line[indexStr+len(err_str): indexStr+len(err_str) + 4])

                    #fill it into current test case result dict
                    FIO_verify_RW32["err"] = value.replace(',', '')
                    if int(FIO_verify_RW32["err"]) > 0:
                        print("the case FIO_verify_RW32 had Failed!")

            elif line.find('FIO_verifyRW32') > 0:
                if line.find(err_str) > 0 :
                    indexStr = line.find(err_str)
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str)+4])

                    FIO_verifyRW32["err"] = value.replace(',', '')
                    if int(FIO_verifyRW32["err"]) > 0:
                        print("the case FIO_verifyRW32 had Failed!")

            else:
                pass
        else:
            break

def main():
    # open the test result
    fo = open(resultfilename + 'Verify_Test_Result.txt', 'r')
    result_fill(fo)
    

if __name__ == '__main__':
    main()

