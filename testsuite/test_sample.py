import prodtest

class SampleTest(prodtest.ProduceTestCase):

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        self.produce('hello.txt')
        self.assertDirectoryContents(['produce.ini', 'hello.txt'])
