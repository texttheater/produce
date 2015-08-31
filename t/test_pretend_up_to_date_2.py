from prodtest import ProduceTestCase

class PretendUpToDate2Test(ProduceTestCase):

    def test_pretend_up_to_date2(self):
        normal = lambda: self.produce('S')
        pretending = lambda: self.produce('S', **{'-u': 'T'})
        self.assertDirectoryContents(('produce.ini',))
        self.assertUpdates((), normal, ('S', 'T', 'U', 'V'), ())
        self.assertUpdates(('U', 'V'), normal, ('S', 'T'), ('U', 'V'))
        self.assertUpdates(('U', 'V'), pretending, ('S',), ('T', 'U', 'V'))
        self.assertUpdates((), normal, ('S', 'T'), ('U', 'V'))
