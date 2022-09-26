from arcgis import gis
import os

class Nycmaps(object):

    def __init__(self
                ,url):

        self.url = url

        os.environ['HTTPS_PROXY'] = os.environ['PROXY']
        source = gis.GIS(url)