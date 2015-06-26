import prodtest
import time

class ParallelNoDepsTest(prodtest.ProduceTestCase):

    def test(self):
        # First, three targets with no dependencies. Should take ~9s to run
        # sequentially, ~5s with four threads.
        start = time.time()
        self.produce(**{'-f': 'nodeps.ini'})
        stop = time.time()
        # The "Equal" is for systems where precision is only a second. Do these
        # still exist? Gosh, I hope not.
        self.assertGreaterEqual(stop - start, 9)
        start = time.time()
        self.produce(**{'-f': 'nodeps.ini', '-j': '4'})
        stop = time.time()
        self.assertLessEqual(stop - start, 6)
        # Now, three targets where one depends on the two others. Should take
        # ~6s to run sequentially, ~4s with four threads.
        start = time.time()
        self.produce(**{'-f': 'deps.ini'})
        stop = time.time()
        self.assertGreaterEqual(stop - start, 6)
        start = time.time()
        self.produce(**{'-f': 'deps.ini', '-j': '4'})
        stop = time.time()
        self.assertLessEqual(stop - start, 5)
