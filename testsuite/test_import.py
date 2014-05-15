import prodtest

class CondTest(prodtest.ProduceTestCase):

    def test(self):
        self.assertFileDoesNotExist('ch1/hello.txt')
        self.produce('ch1/hello.txt')
        self.assertFileExists('ch1/hello.txt')
