import prodtest
import subprocess

class DiamondTest(prodtest.ProduceTestCase):

    """
    Basic test for correct handling of diamonds in dependency graphs. The
    challenge here is not to deadlock.
    """

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        self.produce('a')
        self.assertDirectoryContents(['produce.ini', 'a', 'b', 'c', 'd', 'e'])
