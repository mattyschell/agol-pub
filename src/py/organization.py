try:
    print('slowly importing {0}'.format('arcgis'))
    from arcgis import gis
except ImportError as e: 
    raise ImportError("Failed to import arcgis. Check that you are calling from ArcGIS Pro python") from e

import os


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

        source = gis.GIS(url
                        ,user
                        ,creds
                        ,proxy=self.proxy)
        
        self.token = source.session.auth.token

    def describe(self):

        for var, value in self.__dict__.items(): 
            print(f'{var}: {value}')
        
