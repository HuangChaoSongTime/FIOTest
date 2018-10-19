#!/usr/bin/env python
# coding:utf-8

# filename: Performance_Result_Handle.py
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

import matplotlib.pyplot as plt
import numpy as np
import re
from datetime import *

# define dict structure for ecah test case
FIO_SW1 = {"err":0, "IOPS":0, "BW":0}
FIO_SR1 = {"err":0, "IOPS":0, "BW":0}
FIO_SW32 = {"err":0, "IOPS":0, "BW":0}
FIO_SR32 = {"err":0, "IOPS":0, "BW":0}
FIO_RW1 = {"err":0, "IOPS":0, "BW":0}
FIO_RR1 = {"err":0, "IOPS":0, "BW":0}
FIO_RW32 = {"err":0, "IOPS":0, "BW":0}
FIO_RR32 = {"err":0, "IOPS":0, "BW":0}
# define FIO test list to fill plt xlable.
FIOTestList = [ FIO_SR1, FIO_SW1, FIO_SR32, FIO_SW32 , FIO_RR1, FIO_RW1, FIO_RR32, FIO_RW32]
# define a BWvalue & IOPSvalue list
BWValueList = []
IOPSValueList = []
# define the time formate to generate each test case result file.
ISOTIMEFORMAT = '%Y%m%d'
#define the string that we want to search
err_str = 'err='
IOPS_str = 'IOPS='
BW_str = 'BW='
resultfilename = 'C:\\Users\\test\\Desktop\\FIO\\Log\\Performance\\' + str(datetime.now().strftime(ISOTIMEFORMAT))

def result_fill(fo):
    while True:
        line=fo.readline()
        line = ",".join(line.replace(' ', '').split(':'))
        if line:
            #search the string in line
            if line.find('FIO_SW1') > 0:
                if line.find(err_str) > 0 :
                    #find the string index in line
                    indexStr = line.find(err_str)
                    #cut out the string and get the value for string
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str) + 4])
                    #fill it into current test case result dict
                    FIO_SW1["err"] = value.replace(',', '')

                # search the string in line
                if line.find(IOPS_str) > 0:
                    #find the string index in line
                    indexStr = line.find(IOPS_str)
                    #cut out the string and get the value for string
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    #fill it into current test case result dict
                    FIO_SW1["IOPS"] = value.replace(',', '')

                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_SW1["BW"] = value.replace(',', '')
                    #print("FIO_SW1 test result: " ,FIO_SW1)

            # search the string in line
            elif line.find('FIO_SR1') > 0:
                if line.find(err_str) > 0 :
                    #find the string index in line
                    indexStr = line.find(err_str)
                    #cut out the string and get the value for string
                    value = re.sub("\D","",line[indexStr+len(err_str): indexStr+len(err_str) + 4])
                    #fill it into current test case result dict
                    FIO_SR1["err"] = value.replace(',', '')

                if line.find(IOPS_str) > 0:
                    indexStr = line.find(IOPS_str)
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    FIO_SR1["IOPS"] = value.replace(',', '')

                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_SR1["BW"] = value.replace(',', '')
                    #print("FIO_SR1 test result: ", FIO_SR1)

            elif line.find('FIO_SW32') > 0:
                if line.find(err_str) > 0 :
                    indexStr = line.find(err_str)
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str)+4])
                    FIO_SW32["err"] = value.replace(',', '')

                if line.find(IOPS_str) > 0:
                    indexStr = line.find(IOPS_str)
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    FIO_SW32["IOPS"] = value.replace(',', '')

                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_SW32["BW"] = value.replace(',', '')
                    #print("FIO_SW32 test result: ", FIO_SW32)

            elif line.find('FIO_SR32') > 0:
                if line.find(err_str) > 0 :
                    indexStr = line.find(err_str)
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str) + 4])
                    FIO_SR32["err"] = value.replace(',', '')

                if line.find(IOPS_str) > 0:
                    indexStr = line.find(IOPS_str)
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    FIO_SR32["IOPS"] = value.replace(',', '')

                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_SR32["BW"] = value.replace(',', '')
                    #print("FIO_SR32 test result: ", FIO_SR32)

            elif line.find('FIO_RW1') > 0:
                if line.find(err_str) > 0 :
                    indexStr = line.find(err_str)
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str) + 4])
                    FIO_RW1["err"] = value.replace(',', '')

                if line.find(IOPS_str) > 0:
                    indexStr = line.find(IOPS_str)
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    FIO_RW1["IOPS"] = value.replace(',', '')

                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_RW1["BW"] = value.replace(',', '')
                    #print("FIO_RW1 test result: ", FIO_RW1)

            elif line.find('FIO_RR1') > 0:
                if line.find(err_str) > 0 :
                    indexStr = line.find(err_str)
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str) + 4])
                    FIO_RR1["err"] = value.replace(',', '')

                if line.find(IOPS_str) > 0:
                    indexStr = line.find(IOPS_str)
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    FIO_RR1["IOPS"] = value.replace(',', '')

                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_RR1["BW"] = value.replace(',', '')
                    #print("FIO_RR1 test result: ", FIO_RR1)

            elif line.find('FIO_RW32') > 0:
                if line.find(err_str) > 0 :
                    indexStr = line.find(err_str)
                    value = re.sub("\D","",line[indexStr+len(err_str)-1:indexStr+len(err_str) + 4])
                    FIO_RW32["err"] = value.replace(',', '')

                if line.find(IOPS_str) > 0:
                    indexStr = line.find(IOPS_str)
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    FIO_RW32["IOPS"] = value.replace(',', '')

                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_RW32["BW"] = value.replace(',', '')
                    #print("FIO_RW32 test result: ", FIO_RW32)

            elif line.find('FIO_RR32') > 0:
                if line.find(err_str) > 0 :
                    indexStr = line.find(err_str)
                    value = re.sub("\D","",line[indexStr+len(err_str):indexStr+len(err_str) + 4])
                    FIO_RR32["err"] = value.replace(',', '')

                if line.find(IOPS_str) > 0:
                    indexStr = line.find(IOPS_str)
                    value = line[indexStr + len(IOPS_str):indexStr + len(IOPS_str) + 5]
                    FIO_RR32["IOPS"] = value.replace(',', '')
                    indexStr = line.find(BW_str)
                    value = line[indexStr + len(BW_str):indexStr + len(BW_str) + 8]
                    FIO_RR32["BW"] = value.replace(',', '')
                    #print("FIO_RR32 test result: ", FIO_RR32)
            else:
                pass
        else:
            break

def get_performance_value(str):
    value = float(''.join(re.findall(r'\-*\d+(?:\.\d+)?', str)))
    return value

def performance_value_parse(dict):
    BWValueString = dict['BW'].upper()
    #print(BWValueString)
    IOPSValueString = dict['IOPS'].upper()
    #print(IOPSValueString)
    # Parse BW test result, basis: Mib/s 
    if BWValueString.find('K') > 0:
        value = get_performance_value(BWValueString)
        BWValueList.append(value / 1024.0)
    # Mib/s 
    elif BWValueString.find('M') > 0:
        value = get_performance_value(BWValueString)
        BWValueList.append(value)

    elif BWValueString.find('G') > 0:
        value = get_performance_value(BWValueString)
        BWValueList.append(value * 1024.0)

    else:
        # Here is the 'Bit/s' case.
        value = get_performance_value(BWValueString)
        BWValueList.append(value / 1024.0 / 1024.0)
    #print("the BWValuelist is:", BWValueList)

    # Parse IOPS test result, Basis: Kib/s
    if IOPSValueString.find('K') > 0:
        value = get_performance_value(IOPSValueString)
        IOPSValueList.append(value)

    elif IOPSValueString.find('M') > 0:
        value = get_performance_value(IOPSValueString)
        IOPSValueList.append(value * 1024.0)

    elif BWValueString.find('G') > 0:
        value = get_performance_value(IOPSValueString)
        IOPSValueList.append(value * 1024.0 * 1024.0)

    else:
        # Here is the 'Bit/s' case.
        value = get_performance_value(IOPSValueString)
        IOPSValueList.append(value / 1024.0)
    #print(" the IOPSValuelist is :", IOPSValueList)

# sort the valuelist and get the max value
def getmaxvalue(valuelist):
    # sort value list
    valuelist.sort()

    return (valuelist[-1] * 1.5)

def drawBWchart():
    maxvalue = getmaxvalue(BWValueList)
    fig = plt.figure(figsize=(9, 6))
    X = np.arange(len(BWValueList)) + 1
    # plt.bar(X, -Y2, width=width, facecolor='#ff9999', edgecolor='white')
    plt.bar(X, BWValueList, width=0.5, label=(('BW(Mib/s)')),facecolor='lightskyblue', edgecolor='white')
    #plt.bar(X + 0.35, IOPSValueList, width=0.35, label=(('IOPS(k)')),facecolor='yellowgreen', edgecolor='white')
    plt.legend()
    plt.ylabel("Performance(Mib/s)")
    plt.xlabel('Test case')
    plt.ylim(0, maxvalue)
    plt.title('FIO test Result')
    plt.xticks((1, 2, 3, 4, 5, 6, 7 , 8), \
               ('FIO_SR1', 'FIO_SW1', 'FIO_SR32', 'FIO_SW32', 'FIO_RR1', 'FIO_RW1', 'FIO_RR32', 'FIO_RW32'))
    # add text
    #print(BWValueList)
    for x, y in zip(X, BWValueList):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom')
    fig.savefig(resultfilename+'PerformanceBWTestResult.png')
    print("the PerformanceBWTestResult picture had saved! ")

def drawIOPSchart():
    maxvalue = getmaxvalue(IOPSValueList)
    fig = plt.figure(figsize=(9, 6))
    X = np.arange(len(IOPSValueList)) + 1

    # plt.bar(X, -Y2, width=width, facecolor='#ff9999', edgecolor='white')
    plt.bar(X, IOPSValueList, width=0.5, label=(('IOPS(k)')),facecolor='yellowgreen', edgecolor='white')
    plt.legend()
    plt.ylabel("Performance(kb/s)")
    plt.xlabel('Test case')
    plt.ylim(0, maxvalue)
    plt.title('FIO test Result')
    plt.xticks((1, 2, 3, 4, 5, 6, 7 , 8), \
               ('FIO_SR1', 'FIO_SW1', 'FIO_SR32', 'FIO_SW32', 'FIO_RR1', 'FIO_RW1', 'FIO_RR32', 'FIO_RW32'))
    # add text
    for x, y in zip(X, IOPSValueList):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom')
    fig.savefig(resultfilename + 'PerformanceIOPSTestResult.png')
    print("the PerformanceIOPSTestResult picture had saved! ")

def main():
    # open the test result
    fo = open(resultfilename + 'Performace_Test_Result.txt', 'r')
    result_fill(fo)
    for i in range(len(FIOTestList)):
        #print(FIOTestList[i])
        performance_value_parse(FIOTestList[i])

    drawBWchart()
    drawIOPSchart()
    print("The Performance Test result had deal with finished!,All the test finished.")

if __name__ == '__main__':
    main()
