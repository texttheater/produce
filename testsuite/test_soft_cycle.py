from prodtest import ProduceTestCase
from produce import ProduceError

class SoftCycleTest(ProduceTestCase):

    def test_soft_cycle_allowed(self):
        """
        c.txt depends on a.txt, presumably to indicate that you have to build
        a.txt in order to get c.txt (c.txt is a side output of the instantiated
        rule for a.txt). That's fine because the instantiated rule for b.txt
        doesn't have its own recipe, so there's no clash.
        """
        self.assertDirectoryContents(('produce.ini',))
        self.produce('b.txt')
        self.assertDirectoryContents(('produce.ini', 'a.txt', 'b.txt', 'c.txt'))

    def test_soft_cycle_disallowed(self):
        """
        c.txt depends on a.txt, but the instantiated rule for a.txt builds
        c.txt as a side output and the one for c.txt also has its own recipe.
        That's a clash, we croak.
        """
        self.assertDirectoryContents(('produce.ini',))
        with self.assertRaisesRegex(ProduceError, r'cyclic dependency'):
            self.produce('c.txt')
        self.assertDirectoryContents(('produce.ini',))
