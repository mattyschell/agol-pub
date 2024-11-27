import sys
import time
import logging
import os

import organization
import publisher

def main(zippedgdb
        ,expectedname
        ,expectedmb=250):

    qareport = ""

    #checks here

    return qareport 

def qalogging(logfile
             ,level=logging.INFO):
    
    qalogger = logging.getLogger(__name__)
    qalogger.setLevel(level)
    filehandler = logging.FileHandler(logfile)
    qalogger.addHandler(filehandler)

    return qalogger

if __name__ == '__main__':

    pitemid  = sys.argv[1] # 1abcdefghijklmnopqrstuvwxyz0
    pgdbname = sys.argv[2] # cscl.gdb
    ptempdir = sys.argv[3] # D:\temp
    pzipmb   = sys.argv[4] # 500 

    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    # qa-replace-cscl-gdb-20241121-114410.log
    # qa-replace-cscl_pub-gdb-20241121-114410.log
    targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                            ,'{0}-replace-{1}-{2}.log'.format('qa'
                                                             ,pgdbname.replace('.', '-')
                                                             ,timestr))
    
    qalogger = qalogging(targetlog)

    org = organization.nycmaps(os.environ['NYCMAPSUSER']
                              ,os.environ['NYCMAPCREDS'])
        
    pubgdb = publisher.pubitem(org
                              ,pitemid)
    
    # D:\temp\cscl.gdb.zip
    zipped = pubgdb.download(ptempdir)
    
    retqareport = main(zipped
                      ,pzipmb)

    if len(retqareport) > 4:

        #4 allows for a pair of sloppy CRLFs
        #QA does not notify. It QAs 
        qalogger.error(retqareport)