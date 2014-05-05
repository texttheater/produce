import os

from prodtest import ProduceTestCase

class ShellTest(ProduceTestCase):

    """
    Tests using a Perl rather than a Bash recipe.
    """

    def test_shell(self):
        self.produce('hello.txt')
        self.assertFileContents('hello.txt', 'Hello, world!\n')
