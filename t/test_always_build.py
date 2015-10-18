from prodtest import ProduceTestCase

class AlwaysBuildTest(ProduceTestCase):

    def test_always_build(self):
        f = lambda: self.produce('a')
        self.assertDirectoryContents(('produce.ini', 'c'))
        self.assertUpdates((), f, ('a', 'b'), ('c',))
        self.assertUpdates((), f, (), ('a', 'b', 'c'))
        f = lambda: self.produce('a', **{'-b': None})
        self.assertUpdates((), f, ('a',), ('b', 'c'))
        f = lambda: self.produce('a', **{'-B': None})
        self.assertUpdates((), f, ('a', 'b'), ('c',))
