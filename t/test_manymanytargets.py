from prodtest import ProduceTestCase

class ManyManyTargetsTest(ProduceTestCase):

    """
    A test where the dependency graph has a very large number of nodes (16384).
    Should not hit the thread limit.
    """

    def test_manytargets(self):
        self.produce()
