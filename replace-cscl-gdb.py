# calling bat must
# set AGOLPUB=D:\gis\agol-pub\src\py
# set PYTHONPATH=%PYTHONPATH%;%AGOLPUB%
# set NYCMAPSUSER=xxxx.xxx.xxx
# set NYCMAPSCREDS=xxxxxx
# set TARGETLOGDIR=D:\gis\geodatabase-scripts\logs\replace_cscl_gdb\

import organization
import publisher

import sys
import time
import logging
import os

if __name__ == '__main__':

    srcgdb        = sys.argv[1] # D:\csclwhatever\dbname.gdb
    targetgdbname = sys.argv[2] # cscl.gdb
    targetitemid  = sys.argv[3] # aabcdefghijklmnopqrstuvwxyz0
    tempdir       = sys.argv[4] # D:\temp

    retval = 1

    timestr = time.strftime("%Y%m%d-%H%M%S")

    try:

        org = organization.nycmaps(os.environ['NYCMAPSUSER']
                                  ,os.environ['NYCMAPCREDS'])
        filegdb = publisher.localgdb(srcgdb)
    
    except Exception as e:
        raise ValueError("Failure {0} in instantiation".format(e)) 
    
    # replace-cscl-20241121-114410.log
    # replace-cscl_pub-20241121-114410.log
    targetlog = os.path.join(os.environ['TARGETLOGDIR'] 
                            ,'replace-{0}-{1}.log'.format(targetgdbname.replace('.', '-')
                                                         ,timestr))

    logging.basicConfig(filename=targetlog
                       ,level=logging.INFO)
    
    logging.info('renaming {0} to {1} and zipping it'.format(filegdb.gdb
                                                            ,targetgdbname))

    pubgdb = publisher.pubitem(org
                              ,targetitemid)
    
    filegdb.renamezip(tempdir
                     ,targetgdbname)

    logging.info('replacing nycmaps item with id {0}'.format(targetitemid))

    try:
        retval = pubgdb.replace(filegdb.zipped)
        filegdb.clean()
        logging.info('Successfully replaced {0}'.format(targetgdbname))
        retval = 0
    except:
        filegdb.clean()
        logging.error('Failure replacing {0}'.format(targetgdbname))
        retval = 1

    exit(retval)
