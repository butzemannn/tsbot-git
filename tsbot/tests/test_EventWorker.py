import unittest
from tsbot.online_time.Events import Events


class MyTestCase(unittest.TestCase):
    def test_EventWorker(self):
        handler = Events()
        handler.run()


if __name__ == '__main__':
    unittest.main()
