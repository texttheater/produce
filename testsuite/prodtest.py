import os
import subprocess
import time
import unittest

def dict2opts(d):
   """
   Turns a dictionary into a list of strings representing command-line
   options. Keys of the dictionary should already be in option format,
   i.e. with leading hyphens. Values are arguments of options. None
   values should be used for options without arguments. Options with
   multiple arguments are not supported.
   """
   result = []
   for k, v in d.items():
       result.append(k)
       if v != None:
           result.append(v)
   return result

class ProduceTestCase(unittest.TestCase):

    """
    To be subclassed by Produce tests. The setUp method makes a copy of the
    directory with the same name as the test module and cd's there. The test
    methods of the subclass are expected to take it from there. Some methods
    for special assertions and one for running commands are provided.
    """

    def setUp(self):
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

    def produce(self, *args, **kwargs):
        # TODO provide an API that throws exceptions rather than exiting,
        # and test that
        self.runCommand(['produce'] + dict2opts(kwargs) + list(args))

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
