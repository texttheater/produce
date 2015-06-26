import prodtest
import subprocess

class SignalTest(prodtest.ProduceTestCase):

    """
    Tests that a Produce process sent SIGTERM cleans up its act before
    croaking.
    """

    def test(self):
        self.assertDirectoryContents(['produce.ini'])
        process = subprocess.Popen(['../../produce'])
        self.sleep(2)
        process.terminate()
        process.wait()
        self.assertDirectoryContents(['produce.ini', 'output.txt~'])
