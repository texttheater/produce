import os
import subprocess
import time
import unittest

class ProduceTestCase(unittest.TestCase):

    """
    To be subclassed by Produce tests. The setUp method makes a copy of the
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

    def tearDown(self):
        os.chdir('..')

    def assertDirectoryContents(self, filelist, directory='.'):
        self.assertEqual(set(filelist), set(os.listdir(directory)))

    def produce(self, *args):
        self.runCommand(['produce'] + list(args))

    def assertFileExists(self, path):
        self.assertTrue(os.path.exists(path))

    def assertFileDoesNotExist(self, path):
        self.assertFalse(os.path.exists(path))

    def assertState(self, existentFiles, nonExistentFiles):
        for f in existentFiles:
            self.assertFileExists(f)
        for f in nonExistentFiles:
            self.assertFileDoesNotExist(f)

    def assertNewerThan(self, newFile, oldFile):
        self.assertTrue(self.mtime(newFile) > self.mtime(oldFile))

    def mtime(self, path):
        return os.stat(path).st_mtime

    def runCommand(self, command):
        exitcode = subprocess.call(command)
        self.assertEqual(exitcode, 0)

    def touch(self, path):
        os.utime(path, None)

    def sleep(self, seconds=2):
        """
        Wait a short while in order to make sure mtime changes.
        """
        time.sleep(seconds)
