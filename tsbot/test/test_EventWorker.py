import unittest
from tsbot.onlinetime.EventHandler import EventHandler


class MyTestCase(unittest.TestCase):
    def test_EventWorker(self):
        handler = EventHandler()
        handler.run()


if __name__ == '__main__':
    unittest.main()
