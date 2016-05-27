from prodtest import ProduceTestCase

class AlwaysBuildTest(ProduceTestCase):

    def test_always_build(self):
        self.assertDirectoryContents(('produce.ini',))
        f = lambda: self.produce('a')
        self.assertUpdates((), f, ('a', 'b'), ())
        self.assertUpdates((), f, (), ('a', 'b'))
        f = lambda: self.produce('a', **{'-b': None})
        self.assertUpdates((), f, ('a'), ('b'))
        f = lambda: self.produce('a', 'b', **{'-b': None})
        self.assertUpdates((), f, ('a', 'b'), ())
