import prodtest


class ParallelismTest(prodtest.ProduceTestCase):

    def test_parallelism(self):
        # control: no declared parallelism
        # recipes run in parallel
        with self.assertTakesLessThan(0.3):
            self.produce('a', **{'-j': '2'})
        # treatment: declared parallelism
        # recipes run in sequence
        with self.assertTakesMoreThan(0.3):
            self.produce('d', **{'-j': '2'})
        # Make sure running with less parallelism than the recipe "needs" still
        # works:
        with self.assertTakesLessThan(0.4):
            self.produce('d', **{'-j': '1', '-B': None})
