from prodtest import ProduceTestCase

class ManyTargetsTest(ProduceTestCase):

    """
    A test where the dependency graph has a large number of nodes (4096).
    Although Produce creates a thread for each target, it only creates up to N
    threads per subtarget where N is the number of jobs (64 in the below
    example). So it does not hit the thread limit.
    """

    def test_manytargets(self):
        self.produce(**{'-j': '64'})
