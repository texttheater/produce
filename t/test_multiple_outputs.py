import logging
import prodtest

class MultipleOutputsTest(prodtest.ProduceTestCase):

    """
    Tests the handling of recipes with multiple outputs.
    """

    def test_without(self):
        """
        Without the outputs attribute, the recipe is run twice, once for each
        target, thus two INFO messages are generated:
        """
        self.assertDirectoryContents(['produce.ini', 'Makefile'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('a.txt', 'b.txt')
        self.assertEqual(len(l.output), 2)
        self.assertDirectoryContents(['produce.ini', 'Makefile', 'a.txt', 'b.txt'])

    def test_with(self):
        """
        With the outputs attribute, the recipe is run only once:
        """
        self.assertDirectoryContents(['produce.ini', 'Makefile'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('c.txt', 'd.txt')
        self.assertEqual(len(l.output), 1)
        self.assertDirectoryContents(['produce.ini', 'Makefile', 'c.txt', 'd.txt'])
