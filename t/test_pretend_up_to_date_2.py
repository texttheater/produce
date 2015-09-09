from prodtest import ProduceTestCase

class PretendUpToDate2Test(ProduceTestCase):

    def test_pretend_up_to_date_2(self):
        #     S
        #    / \
        #   T   V
        #  /
        # U
        normal = lambda: self.produce('S')
        pretending = lambda: self.produce('S', **{'-u': 'T'})
        self.assertDirectoryContents(('produce.ini',))
        self.assertUpdates((), normal, ('S', 'T', 'U', 'V'), ())
        self.assertUpdates(('U', 'V'), normal, ('S', 'T'), ('U', 'V'))
        # Updates S, but also touches U in order not to forget that T, and
        # therefore S, is out of date, even if T is deleted in the meantime:
        self.assertUpdates(('U', 'V'), pretending, ('S', 'U'), ('T', 'V'))
        self.assertUpdates((), normal, ('S', 'T'), ('U', 'V'))
