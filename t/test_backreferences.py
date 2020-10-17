import prodtest
import produce

class BackreferenceTest(prodtest.ProduceTestCase):

    """
    When a variable name occurs in a Produce pattern more than once.
    """

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        self.produce('data/fastText/en/cc.en.300.bin.gz')
        self.assertDirectoryContents(['cc.en.300.bin.gz'],
                directory='data/fastText/en')
        self.produce('data/fastText/fr/cc.fr.300.bin.gz')
        self.assertDirectoryContents(['cc.fr.300.bin.gz'],
                directory='data/fastText/fr')
        with self.assertRaises(produce.ProduceError):
            self.produce('data/fastText/fr/cc.en.300.bin.gz')
        with self.assertRaises(produce.ProduceError):
            self.produce('data/fastText/en/cc.fr.300.bin.gz')
