from prodtest import ProduceTestCase
from produce import ProduceError

class BracesTest2(ProduceTestCase):

    """
    Tests using } in Python expressions.
    """

    def test_braces2(self):
        with self.assertRaisesRegex(ProduceError,
                r'no rule to produce 1/1\.aux'):
            self.produce('test.pdf')
