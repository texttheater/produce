import asyncio
import atexit
import os
import produce
import subprocess
import time
import unittest

def close_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return
    loop.close()

# Close event loop at exit to avoid errors/warnings.
# Is there a nicer way??
atexit.register(close_event_loop)

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
        produce.produce(dict2opts(kwargs) + list(args),
                        asyncio.get_event_loop())

    def assertFileExists(self, path):
        self.assertTrue(os.path.exists(path))

    def assertFileDoesNotExist(self, path):
        self.assertFalse(os.path.exists(path))

    def assertState(self, existentFiles, nonExistentFiles):
        for f in existentFiles:
            self.assertFileExists(f)
        for f in nonExistentFiles:
            self.assertFileDoesNotExist(f)

    def assertNewer(self, newFile, oldFile):
        self.assertGreater(self.mtime(newFile), self.mtime(oldFile))

    def assertNewerEqual(self, newFile, oldFile):
        self.assertGreaterEqual(self.mtime(newFile), self.mtime(oldFile))

    def assertUpdates(self, changed, function, updated, notUpdated):
        """
        Touches the files in changed, runs function and asserts that doing so
        created the files in updated or updated them, and that it did not
        update the files in notUpdated.
        """
        for f in changed:
            self.sleep(0.1)
            self.touch(f)
        times = {}
        for f in updated + notUpdated:
            times[f] = self.qmtime(f)
        self.sleep()
        function()
        for f in updated:
            self.assertGreater(self.qmtime(f), times[f])
        for f in notUpdated:
            self.assertLessEqual(self.qmtime(f), times[f])

    def assertFileContents(self, fileName, expectedContents):
        with open(fileName) as f:
            actualContents = f.read()
        self.assertEqual(expectedContents, actualContents)

    def mtime(self, path):
        return os.stat(path).st_mtime

    def qmtime(self, path):
        """
        Returns the modification time of the file at path, or 0 if it doesn't
        exist.
        """
        try:
            return self.mtime(path)
        except FileNotFoundError:
            return 0

    def runCommand(self, command):
        exitcode = subprocess.call(command)
        self.assertEqual(exitcode, 0)

    def touch(self, path):
        self.runCommand(['touch', path])

    def sleep(self, seconds=1):
        """
        Wait a short while in order to make sure mtime changes.
        """
        time.sleep(seconds)

    def createFile(self, name, contents):
        with open(name, 'w', encoding='UTF-8') as f:
            f.write(contents)

    def removeFile(self, name):
        os.unlink(name)
