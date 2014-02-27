import prodtest

class DepTest(prodtest.ProduceTestCase):

    def test_full(self):
        self.assertOriginalState()
        self.produce('a')
        self.assertState(['a', 'b', 'c', 'd', 'e'], [])
        self.produce('vacuum')
        self.assertOriginalState()
        self.produce('b')
        self.assertState(['b', 'd', 'e'], ['c', 'a'])
        bmtime = self.mtime('b')
        self.sleep()
        self.produce('a')
        self.assertState(['a', 'b', 'c', 'd', 'e'], [])
        self.assertEqual(self.mtime('b'), bmtime) # b was not rebuilt
        self.touch('d')
        self.sleep()
        self.produce('a')
        self.assertNewerThan('a', 'd') # a was rebuilt
        self.assertNewerThan('b', 'd') # b was rebuilt
        self.assertNewerThan('d', 'c') # c was not rebuilt
        self.sleep()
        self.touch('c')
        self.produce('a')
        self.assertNewerThan('a', 'c') # a was rebuilt
        self.assertNewerThan('c', 'b') # b was not rebuilt
        self.assertNewerThan('c', 'd') # d was not rebuilt
        self.assertNewerThan('c', 'e') # e was not rebuilt

    def assertOriginalState(self):
        self.assertState(['d', 'e'], ['a', 'b', 'c'])
        
