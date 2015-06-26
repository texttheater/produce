from prodtest import ProduceTestCase

class DepfileTest(ProduceTestCase):

    def test_depfile(self):
        self.assertDirectoryContents(('produce.ini', 'CREDITS', 'Makefile',
                'fib.c', 'fib.h', 'sayfib.c'))
        self.produce('sayfib')
        self.assertDirectoryContents(('produce.ini', 'CREDITS', 'Makefile',
                'fib.c', 'fib.h', 'sayfib.c', 'fib.o', 'sayfib', 'sayfib.d'))
        time_object = self.mtime('fib.o')
        time_executable = self.mtime('sayfib')
        time_depfile = self.mtime('sayfib.d')
        self.sleep()
        # Touching the header file makes the executable out of date because of
        # the dependency listed only in the depfile:
        self.touch('fib.h')
        self.produce('sayfib')
        self.assertGreater(self.mtime('sayfib'), time_executable)
        self.assertEqual(self.mtime('fib.o'), time_object)
        self.assertEqual(self.mtime('sayfib.d'), time_depfile)
        time_executable = self.mtime('sayfib')
        self.sleep()
        # Touching the source file also makes the depfile out of date:
        self.touch('sayfib.c')
        self.produce('sayfib')
        self.assertGreater(self.mtime('sayfib'), time_executable)
        self.assertEqual(self.mtime('fib.o'), time_object)
        self.assertGreater(self.mtime('sayfib.d'), time_depfile)
