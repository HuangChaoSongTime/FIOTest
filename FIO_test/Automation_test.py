#!/usr/bin/env python
# coding:utf-8
"""
#Test Description:
# filename: Automation_test.py
# author: Huang Chaosong
# date: 2017.12.15
# verison: v1.0

#Function:
    1. get the parameters from user then to auto change runtime value and size value.
    2. run FIO test.
    3. handle FIO test result.
    4. run IOMeter test.
    5. handle IOMeter test result.
    6. run BurnIntest tools.
    7. handle the whole test process result.
    8. finished

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
"""
import sys
import getopt
import Verify_test
import Performance_test
import IOmeter_test
import os
import sys
import burnIn_test

# FIO test case directory.
search_path = r"C:\\Users\\test\\Desktop\\FIO\\FIO_Test\\"
# search string for to change value
set_string = ['runtime=', 'size=']

# replace the old value
def alter(file, old_value, new_value):
    os.chdir(search_path)
    file_data =""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_value in line:
                line = line.replace(old_value, new_value+'\n')
            file_data += line
    with open(file, "w", encoding="utf-8") as  f:
        print(file_data)
        f.write(file_data)

# search and set the run time value
def setruntime(para):
    os.chdir(search_path)
    for filename in os.listdir(search_path):
        print(filename)
        with open(filename, 'r', encoding="utf-8") as f:
            for line in f:
                if set_string[0] in line:
                    pos = line.index(set_string[0])
                    old_value = line[pos+len(set_string[0]):]
                    print("old_value:",old_value)
                    alter(filename, old_value, para)

# search and set the size value
def setsize(size):
    os.chdir(search_path)
    for filename in os.listdir(search_path):
        print(filename)
        with open(filename, 'r', encoding="utf-8") as f:
            for line in f:
                if set_string[1] in line:
                    pos = line.index(set_string[1])
                    old_value = line[pos+len(set_string[1]):]
                    print("old_value:",old_value)
                    alter(filename, old_value, size)

# help menu
def usage():
    print("Usage:%s [-t|-s] [--help] args...." % sys.argv[0])
    print("-t: used for set time. such as: -t60 -> set runtime as 60s ")
    print("-s: used for set size. such as: -t500m -> set size as 500m ")
    print("--help: used for help function. ")

def main():
    # TBD
    Performance_test.main()
    Verify_test.main()
    IOmeter_test.main()
    burnIn_test.main()

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:c:", ["help", "output="])

        # check all param
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit(1)
            elif opt in ("-t", "--time"):
                setruntime(arg)
            elif opt in ("-s", "--size"):
                setsize(arg)
            else:
                print("%s  ==> %s" % (opt, arg))

    except getopt.GetoptError:
        print("You had input an error parameters, Please retry!")
        usage()
        sys.exit(1)

    main()
