import unittest

from tsbot.tsbot import run

class MyTestCase(unittest.TestCase):

    @staticmethod
    def test_all():
        run()


if __name__ == '__main__':
    unittest.main()
