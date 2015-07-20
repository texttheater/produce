import logging
import prodtest

class DudedepSuccessTest(prodtest.ProduceTestCase):

    """
    Tests that duplicate dependencies do not lead to redundant recipe
    execution.
    """

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce()
        self.assertEqual(len(l.output), 6) # start, complete for a, b, y
        self.assertDirectoryContents(['produce.ini', 'a', 'b', 'y'])
