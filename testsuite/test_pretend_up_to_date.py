from prodtest import ProduceTestCase

class PretendUpToDateTest(ProduceTestCase):

    def test_pretend_up_to_date(self):
        normal = lambda: self.produce('a')
        pretending = lambda: self.produce('a', **{'-u': 'b'})
        self.assertDirectoryContents(('produce.ini',))
        self.assertUpdates((), normal, ('a', 'b', 'c', 'd'), ())
        self.assertUpdates(('c',), normal, ('a', 'b'), ('c', 'd'))
        self.assertUpdates(('c',), pretending, (), ('a', 'b', 'c', 'd'))
        self.assertUpdates((), normal, ('a', 'b'), ('c', 'd'))
        self.assertUpdates(('b',), normal, ('a',), ('b', 'c', 'd'))
        self.assertUpdates(('b',), pretending, ('a',), ('b', 'c', 'd'))

