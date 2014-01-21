import os
import subprocess
import unittest

class ProduceTestCase(unittest.TestCase):

    """
    To be subclassed by produce tests. The setUp method makes a copy of the
    directory with the same name as the test module and cd's there. The test
    methods of the subclass are expected to take it from there. Some methods
    for special assertions and one for running commands are provided.
    """

    def setUp(self):
        # TODO use absolute paths based on testsuite directory?
        self.workdir = self.__module__ + '.working'
        try:
            self.runCommand(['rm', '-rf', self.workdir])
            self.runCommand(['cp', '-r', self.__module__, self.workdir])
        except Exception as e:
            self.skipTest('setup failed')
        os.chdir(self.workdir)

    def produce(self, **args):
        subprocess.call(['produce'] + args)

    def assertFileExists(self, path):
        self.assertTrue(os.path.exists(path))

    def assertFileDoesNotExist(self, path):
        self.assertFalse(os.path.exists(path))

    def assertNewerThan(self, newFile, oldFile):
        self.assertTrue(self.mtime(newFile) > self.mtime(oldFile))

    def mtime(self, path):
        return os.stat(path).st_mtime

    def runCommand(self, command):
        exitcode = subprocess.call(command)
        self.assertEqual(exitcode, 0)
