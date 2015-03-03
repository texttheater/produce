import os
import prodtest

class SeqexTest(prodtest.ProduceTestCase):

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        self.produce('test.txt')
        self.assertDirectoryContents(['produce.ini', 'test.txt', '0.txt',
                '1.txt', '2.txt', '3.txt'])
