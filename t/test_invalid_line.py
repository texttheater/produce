import prodtest
import produce
import time

class InvalidLineTest(prodtest.ProduceTestCase):

    """
    Tests that an invalid line in produce.ini causes an error.
    """

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        with self.assertRaisesRegex(produce.ProduceError,
                r'invalid line at produce.ini:2'):
            self.produce('a')
