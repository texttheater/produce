from prodtest import ProduceTestCase

class PretendUpToDate3Test(ProduceTestCase):

    def test_pretend_up_to_date_3(self):
        # T
        # |
        # U
        # |
        # V
        normal = lambda: self.produce('T')
        pretending = lambda: self.produce('T', **{'-u': 'U', '-dd': None})
        pretending_B = lambda: self.produce('T', **{'-u': 'U', '-B': None, '-dd': None})
        self.assertDirectoryContents(('produce.ini',))
        self.assertUpdates((), normal, ('T', 'U', 'V'), ())
        # Weirdness grade 0: some file changes, so everything that depends on
        # it is rebuilt.
        self.assertUpdates('V', normal, ('T', 'U'), ('V',))
        # Weirdness grade 1: V changes, but we pretend U is up to date, so
        # nothing at all happens.
        self.assertUpdates('V', pretending, (), ('T', 'U', 'V'))
        # Make everything up-to-date again:
        self.assertUpdates((), normal, ('T', 'U'), ('V',))
        # Weirdness grade 2: U changes, then V changes, we pretend U is up to
        # date, T is rebuilt:
        self.assertUpdates(('U', 'V'), pretending, ('T',), ('U', 'V'))
        # Imagine we now delete U.
        self.removeFile('U')
        # If we produce normally again, we have to take into account that V has
        # changes that T doesn't reflect yet. This does indeed happen: because
        # U doesn't exist, it is rebuilt, and then T has to be rebuilt.
        self.assertUpdates((), normal, ('T', 'U'), ('V',))
        # Weirdness grade 3: same as weirdness grade 2, but we use the -B
        # option. The behavior should be the same.
        self.assertUpdates(('U', 'V'), pretending_B, ('T',), ('U', 'V'))
        self.removeFile('U')
        self.assertUpdates((), normal, ('T', 'U'), ('V',))
