import prodtest

class CondTest(prodtest.ProduceTestCase):

    def test(self):
        self.assertDirectoryContents(['produce.ini', '.gitignore'])
        self.produce()
        self.assertDirectoryContents(['hello.txt', 'bye.txt', 'produce.ini',
                '.gitignore'])
        self.assertFileContents('hello.txt', 'Hello, world!\n')
        self.assertFileContents('bye.txt', 'Hasta la vista, world!\n')
