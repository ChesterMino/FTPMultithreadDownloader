#!/usr/bin/env python
__author__ = 'dtamaskovic'

from ftplib import FTP
from ftplib import all_errors
from collections import namedtuple
import csv
import os
import sys
import time
import threading


def getIP():

    table = []
    count = 1
    with open('C:\\intellian_log\\ip.csv', 'rb') as csvfile:
        tempreader = csv.reader(csvfile)
        for row in tempreader:

            line=row[0]
            l=line.split(";")
            name=l[0]
            ipadd=l[1]
            table.append( [count, name, ipadd])
            #print (count, name, ipadd)
            count += 1
        return table
            #download(name, ipadd)


def download(t, counter):

    row = t[counter]
    #r=row.split(",")
    ipadd=str(row[2])
    name=str(row[1])
    order=row[0]
    newpath = r'C:\\intellian_log\\'+name+''
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    port=21
    password='intellian'

    os.chdir("c:/intellian_log/test_log/") #changes the active dir - this is where downloaded files will be saved to

    try:
        ftp = FTP(ipadd)

        try:
            ftp.login('root', 'intellian')

        except:
            ftp.login('intellian', '12345678')

        print "File List:"
        files = ftp.dir()

        directory ='/tmp/nand/log' #dir i want to download files from, can be changed or left for user input
        filematch = '*20151204.*' # a match for any file in this case, can be changed or left for user to input

        ftp.cwd(directory)

        print 'Directory changed.'

        filenames = ftp.nlst(filematch)
        print filenames

        for filename in filenames: # Loop - looking for matching files


            if filename not in os.listdir('C:\\intellian_log\\'+name+'\\'):
                local_filename = os.path.join('C:\\intellian_log\\'+name+'\\', filename)
                print('Downloading file : %s', filename , ' from vessel: 5s', name)
                file = open(local_filename, 'wb')
                ftp.retrbinary('RETR '+ filename, file.write)

                file.close()

        ftp.quit()

    except all_errors as e:

        print ('FTP connection unavailable, check if remote is online')

        path = 'C:\\intellian_log\\'+name+'\\'

        if not os.path.exists(path):
            os.makedirs(path)

        filename = name+'_ftp_error.txt'
        with open(os.path.join(path, filename), 'wb') as temp_file:
            temp_file.write('Error while downloading log files. Check if remote is online.')
        return False

    return True

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        download (t, self.counter)
        print "Exiting " + self.name



t = getIP()

counter=len(t)-1


for i in counter:

    thread1 = myThread(1,"Thread-1", i)
    thread2 = myThread(2,"Thread-2", i+1)
    thread3 = myThread(3,"Thread-3", i+2)
    thread4 = myThread(3,"Thread-4", i+3)
    i += 4


thread1.start()
thread2.start()
thread3.start()
thread4.start()

#thread2.start()
#download(t, counter)
#while counter is not 0:

"""
for i in range(0,counter+1,1):

    thread.start_new_thread(download,(t[i],))
    thread.start_new_thread(download,(t[counter-1],))
    thread.start_new_thread(download,(t[counter-2],))
    thread.start_new_thread(download,(t[counter-3],))
    i +=1
    print i
"""