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
        # Pretend T is up to date, only S is rebuilt:
        self.assertUpdates(('U', 'V'), pretending, ('S',), ('T', 'U', 'V'))
        # Normal again: now T is rebuilt, and so is S
        self.assertUpdates((), normal, ('S', 'T'), ('U', 'V'))
