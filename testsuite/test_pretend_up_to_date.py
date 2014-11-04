from prodtest import ProduceTestCase

class PretendUpToDateTest(ProduceTestCase):

    def setUp(self):
        ProduceTestCase.setUp(self)
        self.produce('a')
        self.atime = self.mtime('a')
        self.btime = self.mtime('b')
        self.ctime = self.mtime('c')
        self.dtime = self.mtime('d')

    def test_baseline_new_ingredient(self):
        self.sleep()
        self.touch('c')
        self.produce('a')
        self.assertGreater(self.mtime('a'), self.atime)
        self.assertGreater(self.mtime('b'), self.btime)
        self.assertGreater(self.mtime('c'), self.ctime)
        self.assertEqual(self.mtime('d'), self.dtime)

    def test_baseline_new_intermedidate(self):
        self.sleep()
        self.touch('b')
        self.produce('a')
        self.assertGreater(self.mtime('a'), self.atime)
        self.assertGreater(self.mtime('b'), self.btime)
        self.assertEqual(self.mtime('c'), self.ctime)
        self.assertEqual(self.mtime('d'), self.dtime)

    def test_pretend_new_ingredient(self):
        self.sleep()
        self.touch('c')
        self.produce('a', **{'-u': 'b'})
        self.assertEqual(self.mtime('a'), self.atime)
        self.assertEqual(self.mtime('b'), self.btime)
        self.assertGreater(self.mtime('c'), self.ctime)
        self.assertEqual(self.mtime('d'), self.dtime)

    def test_pretend_new_intermedidate(self):
        self.sleep()
        self.touch('b')
        self.btime = self.mtime('b')
        self.sleep()
        self.produce('a', **{'-u': 'b'})
        self.assertGreater(self.mtime('a'), self.atime)
        self.assertEqual(self.mtime('b'), self.btime)
        self.assertEqual(self.mtime('c'), self.ctime)
        self.assertEqual(self.mtime('d'), self.dtime)

    def test_pretend_new_ingredient_and_intermediate(self):
        self.sleep()
        self.touch('b')
        self.btime = self.mtime('b')
        self.sleep()
        self.touch('c')
        self.ctime = self.mtime('c')
        self.produce('a', **{'-u': 'b'})
        self.assertGreater(self.mtime('a'), self.atime)
        self.assertEqual(self.mtime('b'), self.btime) # b was not reproduced
        self.assertEqual(self.mtime('c'), self.ctime)
        self.assertEqual(self.mtime('d'), self.dtime)
