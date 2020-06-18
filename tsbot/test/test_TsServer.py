import unittest

from tsbot.io.TsServer import TsServer


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_TsServer():
        ts = TsServer()
        print(ts.exec_query("clientlist"))
        # ts.exec_query("clientpoke", {"clid": "20318", "msg": "Test"})
        ts.close_connection()


if __name__ == '__main__':
    unittest.main()
