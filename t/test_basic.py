import prodtest
import time

class BasicTest(prodtest.ProduceTestCase):

    def test(self):
        self.assertDirectoryContents(('produce.ini',))
        self.produce('a')
        self.assertDirectoryContents(('produce.ini', 'a', 'b', 'c'))
