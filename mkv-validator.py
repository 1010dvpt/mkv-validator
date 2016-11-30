#!/usr/bin/env python
#
# mkv-validator.py
#
# MKV validator wrapper - recursively validate integrity of mkv files
# using mkvalidator.exe storing the results in a log file. 
#
# Copyright 2016 Denton Davenport
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# mkvalidator.exe is licensed to matroska.org under BSD license
#    https://www.matroska.org/downloads/mkvalidator.htm
# 
# this script expects the 'mkvalidator.exe' to be in the same directory
# mkv_results.log writes out entire log in same directory
#_

import os
import sys
import re
import subprocess
import fnmatch
import argparse
import inspect
import time
import datetime

### global values
pwd = os.getcwd()
script = inspect.stack()[0][1]
option = ''
logfileout = pwd + '\\mkv_results.log'
mkvalexe = pwd + '\\mkvalidator.exe'

### main program
def main():
    parseOptions()
    logFile()
    fileList(src)
    for mkvs in filelist:
        sys.stdout.write('\nChecking: {}\n'.format(mkvs))
        sys.stdout.flush()
        try:
            mkval(mkvs, option)
            validator(mkvs)
        except KeyboardInterrupt: break

### parse the options
def parseOptions():
    global src, option
    parser = argparse.ArgumentParser(description='example: python {} -o no-warn -s E:\\\\mkvs\\\\movies'.format(script), formatter_class=SmartFormatter)
    parser.add_argument('-o', '--options', type=str,
    help='F|no-warn   only output errors, no warnings\n'
        'live      only output errors/warnings relevant to live streams\n'
        'details   show details for valid files\n'
        'divx      assume the file is using DivX specific extensions\n'
        'quiet     don\'t ouput progress and file info\n',
    action='store', required=False)
    parser.add_argument('-s', '--source', type=str, help='F|E:\\\\mkvs\\\\movies\n'
        'E:/mkvs/movies\n'
        'E:/mkvs/\"Best Movies\"',
    action='store', required=True)
    args = parser.parse_args()
    if args.source:
        src = args.source    
    if args.options:
        option = '--' + args.options

### validate the output
def validator(mkvs):
    with open(logfileout, 'r') as verify:
        lastline = verify.readlines()[len(verify.readlines())-1]
        regxlastline = re.findall(r'\\r(\w{11}\s\d\.\d\.\d|[\w\.-]+):\s([\w\.].+?)\\r\\r\\n[\'\"],\s?', lastline)#(O_(O
        verify.close()
        for line in regxlastline:
            sys.stdout.write('{}\n'.format(': '.join(line)))
            sys.stdout.flush()

### make a list of files to check
def fileList(src):
    global filelist
    filelist = []
    for root, dirnames, filename in os.walk(src):
        for filename in fnmatch.filter(filename, '*.mkv'):
            filelist.append(os.path.join(root, filename))

### check the mkvs
def mkval(checkthismkv, option):
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%Y/%m/%d %H:%M:%S]')
    redirectstdout = sys.stdout
    mkvalcheck = subprocess.Popen([mkvalexe, option, checkthismkv], stderr=subprocess.PIPE)
    if mkvalcheck.stderr:
        with open(logfileout, 'a') as logfile:
            sys.stdout = logfile
            print('{} - Title: {} {}'.format(ts, checkthismkv, mkvalcheck.stderr.readlines()))
            sys.stdout = redirectstdout
            logfile.close()

### create log file
def logFile():
    if not os.path.isfile(logfileout):
        with open(logfileout, 'w') as f:
            f.close()

### help the help output       
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('F|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

if __name__ == '__main__':
    main()
