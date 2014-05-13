import os

from prodtest import ProduceTestCase

class BracesTest(ProduceTestCase):

    """
    Tests using } in Python expressions.
    """

    def test_braces(self):
        self.produce('test.out')
        self.assertFileContents('test.out', 'Hello, world!\n')
