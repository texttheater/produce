import os
import prodtest

class EvalTest(prodtest.ProduceTestCase):

    def test(self):
        self.assertDirectoryContents(['produce.ini', '.gitignore'])
        self.produce()
        self.assertDirectoryContents(['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6',
                'a7', 'produce.ini', '.gitignore'])
