import prodtest
import produce
import time

class KillTest(prodtest.ProduceTestCase):

    """
    Tests that a single recipe failing causes immediate abort and cleanup.
    """

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        with self.assertRaises(produce.ProduceError):
            self.produce(**{'-j': '3'})
        now = time.time()
        self.assertDirectoryContents(['produce.ini', 'b.txt~', 'c.txt~'])
        btime = self.mtime('b.txt~')
        ctime = self.mtime('c.txt~')
        bage = now - btime
        cage = now - ctime
        self.assertGreater(bage, 1)
        self.assertLess(bage, 3)
        self.assertGreater(cage, 0)
        self.assertLess(cage, 1)
