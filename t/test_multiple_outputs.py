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
            self.produce('a.txt', 'b.txt', **{'-j': '3'})
        self.assertEqual(len(l.output), 4)
        self.assertDirectoryContents(['produce.ini', 'Makefile', 'a.txt', 'b.txt'])

    def test_with(self):
        """
        With the outputs attribute, the recipe is run only once:
        """
        self.assertDirectoryContents(['produce.ini', 'Makefile'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('c.txt', 'd.txt', **{'-j': '3'})
        self.assertEqual(len(l.output), 2)
        self.assertDirectoryContents(['produce.ini', 'Makefile', 'c.txt', 'd.txt'])

    def test_with_2(self):
        """
        Same, but using the out. prefix instead of the outputs attribute.
        """
        self.assertDirectoryContents(['produce.ini', 'Makefile'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('e.txt', 'f.txt', **{'-j': '3'})
        self.assertEqual(len(l.output), 2)
        self.assertDirectoryContents(['produce.ini', 'Makefile', 'e.txt', 'f.txt'])

    def test_with_3(self):
        """
        Same, mixing out. and outputs.
        """
        self.assertDirectoryContents(['produce.ini', 'Makefile'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('g.txt', 'h.txt', 'i.txt', **{'-j': '3'})
        self.assertEqual(len(l.output), 2)
        self.assertDirectoryContents(['produce.ini', 'Makefile', 'g.txt', 'h.txt', 'i.txt'])
