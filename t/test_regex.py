import os
import prodtest

class RegexTest(prodtest.ProduceTestCase):

    def test(self):
        self.assertDirectoryContents(['README', 'produce.ini', '.gitignore'])
        self.produce('out/gmb.dev.out')
        self.assertDirectoryContents(['gmb.dev.out', 'gmb.train.model'],
                directory='out')
