from prodtest import ProduceTestCase

class PretendUpToDatePatternTest(ProduceTestCase):

    def test_pretend_up_to_date(self):
        #    a1
        #    |
        #    b1
        #  /   \
        # c1   d1
        normal = lambda: self.produce('a1')
        pretending = lambda: self.produce('a1', **{'-u': 'b%{i}'})
        self.assertDirectoryContents(('produce.ini',))
        self.assertUpdates((), normal, ('a1', 'b1', 'c1', 'd1'), ())
        self.assertUpdates(('c1',), normal, ('a1', 'b1'), ('c1', 'd1'))
        self.assertUpdates(('c1',), pretending, (), ('a1', 'b1', 'c1', 'd1'))
        self.assertUpdates((), normal, ('a1', 'b1'), ('c1', 'd1'))
        self.assertUpdates(('b1',), normal, ('a1',), ('b1', 'c1', 'd1'))
        self.assertUpdates(('b1',), pretending, ('a1',), ('b1', 'c1', 'd1'))
