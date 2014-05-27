from prodtest import ProduceTestCase

class PythonTest(ProduceTestCase):

    """
    Tests using a Python recipe where indentation is important.
    """

    def test_python(self):
        self.produce('test')
