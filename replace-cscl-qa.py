import sys
import time
import logging
import os
import zipfile

import organization
import publisher

def main(downloadedzip
        ,expectedname
        ,workdir
        ,expectedmb
        ,expectedmbbvariannce=25):

    qareport = ""

    # check that we downloaded a .zip
    # for this one we kick back early
    if not downloadedzip.endswith('.zip'):
        qareport += '{0} download {1} doesnt appear to be '.format(os.linesep
                                                                  ,downloadedzip)
        qareport += 'a zip file{2}'.format(os.linesep)
        return qareport

    # check size of zip
    sizemb = os.path.getsize(downloadedzip) / (1024 * 1024)

    if (abs(int(expectedmb) - sizemb) / int(expectedmb) * 100) > int(expectedmbbvariannce):
        
        qareport += '{0} zip file size {1} is '.format(os.linesep, sizemb)
        qareport += 'suspiciously different from expected {0}{1}'.format(expectedmb,os.linesep)
                     
    # check gdbname after unzip
    if os.path.exists(os.path.join(workdir, expectedname)):
        os.remove(os.path.join(workdir, expectedname))    

    with zipfile.ZipFile(downloadedzip, 'r') as zip_ref: 
        zip_ref.extractall(workdir)

    if not os.path.exists(os.path.join(workdir, expectedname)):
        qareport += 'unzipping {0} does not produce {1}{2}'.format(downloadedzip
                                                                  ,expectedname
                                                                  ,os.linesep)

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
    pubgdb.download(ptempdir)
    
    retqareport = main(pubgdb.zipped
                      ,pgdbname
                      ,ptempdir
                      ,pzipmb)
    
    #pubgdb.clean()

    if len(retqareport) > 4:


        # len 4 allows for a pair of sloppy CRLFs
        # QA does not notify. It QAs 
        qalogger.error(retqareport)