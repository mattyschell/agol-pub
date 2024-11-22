import unittest
import os
from pathlib import Path

import organization
import publisher

class PublishTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # this is a dummy item created under the nycmaps test account
        # we could write a creation method
        # but doubtful we will ever create items from code
        self.testitemid = "a8d31a8f63b74b5f893cc675ea7419f0"

        self.testuser  = os.environ['NYCMAPSUSER']
        self.testcreds = os.environ['NYCMAPCREDS']
        self.tempdir = Path(os.environ['TEMP'])
        
        self.org = organization.nycmaps(self.testuser
                                       ,self.testcreds)
        
        self.pubgdb = publisher.pubitem(self.org
                                       ,self.testitemid)

        self.testdatadir = os.path.join(os.path.dirname(os.path.abspath(__file__))
                                       ,'testdata')
        
        self.testgdb = os.path.join(self.testdatadir
                                   ,'sample.gdb')
        
        self.testemptygdb = os.path.join(self.testdatadir
                                        ,'emptysample'
                                        ,'sample.gdb')
        
        self.testemptydiffnamegdb = os.path.join(self.testdatadir
                                                ,'emptysample'
                                                ,'emptysamplewithdiffname.gdb')
        
        self.localgdb = publisher.localgdb(self.testgdb)

        self.emptylocalgdb = publisher.localgdb(self.testemptygdb)

        self.emptydiffnamelocalgdb = publisher.localgdb(self.testemptydiffnamegdb)

    @classmethod
    def tearDownClass(self):

        if os.path.isfile(self.localgdb.zipped):
            os.remove(self.localgdb.zipped)

    def test_adescribe(self):

        try:
            self.pubgdb.describe()
        except Exception as e:
            self.fail("decribe raised {0}".format(e))

    def test_blocalgdbzip(self):

        self.localgdb.zip(self.tempdir)

        self.assertTrue(os.path.isfile(self.localgdb.zipped))

        self.localgdb.clean()

        self.assertFalse(os.path.isfile(self.localgdb.zipped))

    def test_clocalgdbrenamezip(self):

        self.localgdb.renamezip(self.tempdir
                               ,'renamesample.gdb')

        self.assertTrue(os.path.isfile(self.localgdb.zipped))

        self.localgdb.clean()

        self.assertFalse(os.path.isfile(self.localgdb.zipped))

        self.assertFalse(os.path.isfile(self.localgdb.renamed))

    def test_dreplaceitem(self):

        self.localgdb.zip(self.tempdir)

        self.assertTrue(self.pubgdb.replace(self.localgdb.zipped))

        self.localgdb.clean()

    def test_edownload(self):

        self.pubgdb.download(self.tempdir)

        self.assertTrue(os.path.isfile(os.path.join(self.tempdir
                                                   ,'sample.gdb.zip')))
        
    def test_fdownloadandreplace(self):

        # download samplegdb.zip with stuff in it
        # replace with empty samplegdb.zip
        # download empty samplegdb.zip
        # test that the file sizes tell us this is working

        # download sample.gdb.zip and get its size
        self.pubgdb.download(self.tempdir)
        big = os.path.getsize(os.path.join(self.tempdir
                                          ,'sample.gdb.zip'))
        self.localgdb.clean()

        # zip up emptygdb and publish it
        self.emptylocalgdb.zip(self.tempdir)
        self.assertTrue(self.pubgdb.replace(self.emptylocalgdb.zipped))
        self.emptylocalgdb.clean()

        # download empty samplegdb.zip and get its size
        self.pubgdb.download(self.tempdir)
        small = os.path.getsize(os.path.join(self.tempdir
                                            ,'sample.gdb.zip'))
        self.emptylocalgdb.clean()

        # re-publish the original non-empty samplegdb.zip
        self.localgdb.zip(self.tempdir)
        self.assertTrue(self.pubgdb.replace(self.localgdb.zipped))
        self.localgdb.clean()

        self.assertTrue(big > small)

    def test_gdownloadandreplacediffname(self):

        # download samplegdb.zip with stuff in it
        # replace with emptysamplewithdiffname 
        # renamed as samplegdb.zip
        # download empty samplegdb.zip
        # test that the file sizes tell us this is working

        # download sample.gdb.zip and get its size
        self.pubgdb.download(self.tempdir)
        big = os.path.getsize(os.path.join(self.tempdir
                                          ,'sample.gdb.zip'))
        self.localgdb.clean()

        # zip up emptygdb and publish it
        self.emptydiffnamelocalgdb.renamezip(self.tempdir
                                            ,'sample.gdb')
        self.assertTrue(self.pubgdb.replace(self.emptydiffnamelocalgdb.zipped))
        self.emptydiffnamelocalgdb.clean()

        # download empty samplegdb.zip and get its size
        self.pubgdb.download(self.tempdir)
        small = os.path.getsize(os.path.join(self.tempdir
                                            ,'sample.gdb.zip'))
        self.emptylocalgdb.clean()

        # re-publish the original non-empty samplegdb.zip
        self.localgdb.zip(self.tempdir)
        self.assertTrue(self.pubgdb.replace(self.localgdb.zipped))
        self.localgdb.clean()

        self.assertTrue(big > small)


if __name__ == '__main__':
    unittest.main()
