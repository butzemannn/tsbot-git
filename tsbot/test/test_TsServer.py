import unittest

from tsbot.io.TsServer import TsServer


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_TsServer():
        ts = TsServer()
        print(ts.exec_query("clientlist", "times")[0])
        # ts.exec_query("clientpoke", {"identifier": "20318", "msg": "Test"})
        #ts.close_connection()

    def test_TsServerEvent(self):
        ts = TsServer()
        ts.exec_query("servernotifyregister", {"event": "server"})
        event = ts.wait_for_event(60)
        print(event[0])


if __name__ == '__main__':
    unittest.main()
