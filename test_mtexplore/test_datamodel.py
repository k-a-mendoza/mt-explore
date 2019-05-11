import unittest
from mtexplore.model.database_model import Cycler
import pandas as pd

df = pd.DataFrame(columns=['major','minor'],data=[[1,2],[1,3],[2,1],[2,2]])

class CyclerTesting(unittest.TestCase):
    def test_minor(self):
        cycler = Cycler(df,'major','minor')
        minor = cycler.next_minor()
        self.assertTrue(minor['minor'],3)
        minor = cycler.next_minor()
        self.assertTrue(minor['minor'], 2)

    def test_two_minors(self):
        cycler = Cycler(df,'major','minor')
        cycler.next_minor()
        minor = cycler.next_minor()
        self.assertTrue(minor['minor'], 2)

    def test_major(self):
        cycler = Cycler(df, 'major', 'minor')
        major = cycler.next_major()
        self.assertEqual(major['minor'], 1)


if __name__ == '__main__':
    unittest.main()
