from prodtest import ProduceTestCase
from produce import ProduceError

text1 = 'Hello, world!\n'
text2 = 'Goodbye, world!\n'

class RenameOnErrorTest(ProduceTestCase):

    def test_rename_on_error(self):
        self.assertDirectoryContents(('produce.ini',))
        with self.assertRaisesRegex(ProduceError, r'recipe failed'):
            self.produce('hello.txt')
        self.assertDirectoryContents(('produce.ini', 'hello.txt~'))
        self.assertFileContents('hello.txt~', '')
        self.createFile('ghost1.txt', text1)
        with self.assertRaisesRegex(ProduceError, r'recipe failed'):
            self.produce('hello.txt')
        self.assertDirectoryContents(('produce.ini', 'ghost1.txt',
                'hello.txt~'))
        self.assertFileContents('hello.txt~', text1)
        self.createFile('ghost2.txt', text2)
        self.produce('hello.txt')
        self.assertDirectoryContents(('produce.ini', 'ghost1.txt',
                'ghost2.txt', 'hello.txt'))
        self.assertFileContents('hello.txt', text1 + text2)
