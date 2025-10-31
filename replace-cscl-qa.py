import sys
import time
import logging
import os
import zipfile
import shutil
print('importing arcpy')
import arcpy
print('finished importing arcpy')

import organization
import publisher


def iszip(pzipfile):

    if pzipfile.endswith('.zip'):
        return True
    else:
        return False
    
def isreasonablesize(pzipfile
                    ,pexpectedmb
                    ,pvariance):
    
    sizemb = os.path.getsize(pzipfile) / (1024 * 1024)
    
    if (abs(int(pexpectedmb) - sizemb) / int(pexpectedmb) * 100) > int(pvariance):
        return False
    else:
        return True
    
def isgdbinzip(pzipfile
              ,pname
              ,pworkdir):
    
    # check gdbname after unzip
    testgdb = publisher.localgdb(os.path.join(pworkdir
                                             ,pname))
    
    if os.path.exists(testgdb.gdb):
       testgdb.clean()    

    with zipfile.ZipFile(pzipfile, 'r') as zip_ref: 
        zip_ref.extractall(pworkdir)
    
    if not os.path.exists(testgdb.gdb):
        return False
    else:
        testgdb.clean()
        return True
    
def isvalidgdb(pzipfile
              ,pname
              ,pworkdir):
    
    # check the uzipped gdb a workspace        
    testgdb = publisher.localgdb(os.path.join(pworkdir
                                             ,pname))
    
    if os.path.exists(testgdb.gdb):
       testgdb.clean() 

    with zipfile.ZipFile(pzipfile, 'r') as zip_ref: 
        zip_ref.extractall(pworkdir)

    desc = arcpy.Describe(testgdb.gdb)
    testgdb.clean() 

    if  desc.dataType == 'Workspace' \
    and desc.workspaceType == 'LocalDatabase':
        return True
    else:
        return False

def main(downloadedzip
        ,expectedname
        ,workdir
        ,expectedmb
        ,expectedmbbvariannce=25):

    qareport = ""

    # check that we downloaded a .zip
    # for this one we kick back early
    if not iszip(downloadedzip):
        qareport += '{0} download {1} doesnt appear to be '.format(os.linesep
                                                                  ,downloadedzip)
        qareport += 'a zip file{2}'.format(os.linesep)
        return qareport

    if not isreasonablesize(downloadedzip
                           ,expectedmb
                           ,expectedmbbvariannce):

        qareport += '{0} downloaded zip file size is '.format(os.linesep)
        qareport += 'suspiciously different from expected {0} MB {1}'.format(expectedmb
                                                                            ,os.linesep)
                     
    # check gdbname after unzip
    if not isgdbinzip(downloadedzip
                     ,expectedname
                     ,workdir):
        
        qareport += '{0} unzipping downloaded {1}'.format(os.linesep,downloadedzip)
        qareport += 'does not produce {0}{1}'.format(expectedname, os.linesep)
                                                                             
    if not isvalidgdb(downloadedzip
                     ,expectedname
                     ,workdir):
        
        qareport += '{0} unzipping downloaded {1}'.format(os.linesep,downloadedzip)
        qareport += 'does not produce a valid gdb {0}'.format(os.linesep)
        
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
    
    pubgdb.clean()

    if len(retqareport) > 4:

        # len 4 allows for a pair of sloppy CRLFs
        # QA does not notify. It QAs 
        qalogger.error('ERROR: Please review {0}'.format(os.linesep))
        qalogger.error(retqareport)
        sys.exit(1)

    else:

        sys.exit(0)