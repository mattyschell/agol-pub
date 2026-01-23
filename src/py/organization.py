try:
    print('importing {0}'.format('arcgis'))
    from arcgis.gis import GIS
    print('completed importing {0}'.format('arcgis'))
except ImportError as e: 
    raise ImportError("Failed to import arcgis. Check that you are calling from ArcGIS Pro python") from e

import os
import publisher
from pprint import pformat

# probably just one class here for now

class nycmaps(object):

    def __init__(self
                ,user 
                ,creds
                ,url="https://nyc.maps.arcgis.com/"):

        self.user  = user
        self.creds = creds
        self.url   = url

        if 'PROXY' in os.environ:
            self.proxy = {
                'http':  os.environ['PROXY']
               ,'https': os.environ['PROXY']
            }

        self.gis = GIS(url
                      ,user
                      ,creds
                      ,proxy=self.proxy)
        
        self.token = self.gis.session.auth.token

    def describe(self):
    
        items = {k: v for k, v in self.__dict__.items() if k != "creds"}
        width = max(len(k) for k in items)

        for var, value in items.items(): 
            print('{0} : {1}'.format(var.ljust(width)
                                    ,value))        
