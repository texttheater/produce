import prodtest
import time

class ParallelNoDepsTest(prodtest.ProduceTestCase):

    def test(self):
        # First, three targets with no dependencies. Should take ~9s to run
        # sequentially, ~5s with four threads.
        with self.assertTakesMoreThan(0.9):
            self.produce(**{'-f': 'nodeps.ini'})
        with self.assertTakesLessThan(0.6):
            self.produce(**{'-f': 'nodeps.ini', '-j': '4'})
        # Now, three targets where one depends on the two others. Should take
        # ~6s to run sequentially, ~4s with four threads.
        with self.assertTakesMoreThan(0.6):
            self.produce(**{'-f': 'deps.ini'})
        with self.assertTakesLessThan(0.5):
            self.produce(**{'-f': 'deps.ini', '-j': '4'})
