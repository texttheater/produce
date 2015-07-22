import logging
import prodtest
import produce

class DudedepErrorTest(prodtest.ProduceTestCase):

    """
    Tests that duplicate dependencies do not lead to redundant recipe
    execution.
    """

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            with self.assertRaises(produce.ProduceError):
                self.produce()
        levels = [record.levelno for record in l.records]
        self.assertEqual(levels, [logging.INFO, logging.ERROR]) # for b, which fails
        self.assertDirectoryContents(['produce.ini'])
