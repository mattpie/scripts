#!/usr/bin/python

"""
A time tracker. I wanted to see how much time I was
devoting to a task, so I built this to keep track 
of how much time I spent on it.
"""


import sys
import os
import time
import pickle
import argparse
from datetime import datetime, date, timedelta


"""
writes/appends to temp time file
"""
def writeTempTime(object, filename):
    try:
        with open(filename, 'ab+')as f:
            pickle.dump(object, f, pickle.HIGHEST_PROTOCOL)
    except IOError:
        print 'error writing time'
        sys.exit()

        
"""
writes/overwrites time file
"""
def writeNewData(object, filename):
    try:
        with open(filename, 'wb+')as f:
            pickle.dump(object, f, pickle.HIGHEST_PROTOCOL)
    except IOError:
        print 'error writing time'
        sys.exit()

        
"""
adds up and returns all unsaved times
"""
def getTimes(filename):
    times = [] # will store times in a list
    
    with open(filename, 'rb')as f:
        while True:
            try:
                times.append(pickle.load(f))
            except (EOFError, pickle.UnpicklingError):
                break
            
    # check to see if a stop has been issued last
    # if not time is still being added, alert and return
    if len(times) % 2 != 0:
        return 'Time is currently being recorded'
        
    # find the difference of every second time with the time before it    
    i = 0
    total = times[i + 1] - times[i]
    i += 2
    
    # add those differences up until you've reached the end of the
    # list of times
    while i < len(times):
        try:
            total += times[i + 1] - times[i]
            i += 2
        except IndexError:
            break
    
    return total

    
"""
reads and returns the total time currently saved
"""    
def getOldTimes(filename):
    try:
        with open(filename, 'rb')as f:
            oldTime = pickle.load(f)
    except IOError:
            print 'error reading file'
            sys.exit()
    
    return oldTime

    
def main():
    # files holding time info
    TMPFILE = 'timetracker.pkl'
    TIMEFILE = 'times.pkl'

    # set parser and arguments
    parser = argparse.ArgumentParser(description='Track time')
    parser.add_argument('option', choices=['start', 'stop', 'view', 'save'])
    
    # grab argument
    arg = vars(parser.parse_args())

    # start timer
    if (arg['option'] == 'start'):
        writeTempTime(datetime.now(), TMPFILE)
        print 'timer started'
            
    # stop timer
    if (arg['option'] == 'stop'):
        writeTempTime(datetime.now(), TMPFILE)
        print 'timer stopped'
        
    # print times on both files
    if arg['option'] == 'view':
        if os.path.exists(TMPFILE):
            print getTimes(TMPFILE)
        print getOldTimes(TIMEFILE)
        

    if arg['option'] == 'save':
        if not os.path.exists(TMPFILE):
            print 'no data to save'
            sys.exit()
        # get times saved in both time files
        times = getTimes(TMPFILE)
        oldTimes = getOldTimes(TIMEFILE)
        
        # add times
        newTime = times + oldTimes
        
        # times is a str (info message) if a stop wasn't issued after a start
        # don't save in this case
        if type(times) is str:
            print times
            print 'cannot save until timer is stopped'
        else:
            writeNewData(newTime, TIMEFILE)
            try:
                os.remove(TMPFILE)
            except IOError:
                print 'error removing tmp file'
            print 'saved'
            
if __name__ == '__main__': main()
