import sys
import logging
import datetime

import publayer

# SET PYTHONPATH=C:\gis\geodatabase-taxmap-pub\src\py

if __name__ == "__main__":

    url          = sys.argv[1]
    layer        = sys.argv[2]

    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info('started {0} at {1}'.format(layer
                                           ,datetime.datetime.now()))

    layermgr = publayer.Nycmaps(url)

    logger.info('completed {0} at {1}'.format(layer
                                             ,datetime.datetime.now()))

