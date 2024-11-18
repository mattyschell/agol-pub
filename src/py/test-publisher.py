import unittest
import os

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
        self.tempdir = os.environ['TEMP']
        
        self.org = organization.nycmaps(self.testuser
                                       ,self.testcreds)
        
        self.pubgdb = publisher.pubitem(self.org
                                        ,self.testitemid)

        self.testdatadir = os.path.join(os.path.dirname(os.path.abspath(__file__))
                                       ,'testdata')
        
        self.testgdb = os.path.join(self.testdatadir
                                   ,'sample.gdb')
        
        self.localgdb = publisher.localgdb(self.testgdb)

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

    def test_creplaceitem(self):

        self.localgdb.zip(self.tempdir)

        self.pubgdb.replace(self.localgdb.zipped)




if __name__ == '__main__':
    unittest.main()
