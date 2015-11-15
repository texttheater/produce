import logging
import prodtest
import produce

class PretendUpToDateTest4(prodtest.ProduceTestCase):

    def test(self):
        self.assertDirectoryContents(['produce.ini', 'additional.txt'])
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('9.txt')
        self.assertEqual(len(l.output), 20)
        self.touch('additional.txt')
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('9.txt')
        self.assertEqual(len(l.output), 18)
        self.touch('additional.txt')
        with self.assertLogs(logger='produce', level='INFO') as l:
            self.produce('9.txt', **{'-u': '7.txt'})
        self.assertEqual(len(l.output), 4)
