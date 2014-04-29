import os

from prodtest import ProduceTestCase

class IntermediateTest(ProduceTestCase):

    """
    Making sure that a target is not rebuilt just because an intermediate file
    does not exist.
    """

    def test_intermediate(self):
        self.assertOriginalState()
        self.produce('a')
        self.assertState(['a', 'b', 'c'], [])
        amtime = self.mtime('a')
        os.unlink('b')
        self.assertState(['a', 'c'], ['b'])
        self.sleep()
        self.produce('a')
        self.assertState(['a', 'c'], ['b']) # b was not rebuilt
        self.assertEqual(self.mtime('a'), amtime) # and a was not modified
        self.touch('c')
        self.produce('a')
        self.assertGreater(self.mtime('a'), amtime) # a was rebuilt

    def assertOriginalState(self):
        self.assertState(['c'], ['a', 'b'])
        
