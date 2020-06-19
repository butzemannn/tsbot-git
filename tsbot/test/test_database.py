import unittest

# import local file
from tsbot.io.database import exec_query


class MyTestCase(unittest.TestCase):
    def test_exec_query(self):

        print(exec_query("SELECT version();"))
        # print(exec_query("CREATE TABLE test(Test int);"))
        print(exec_query("SELECT * FROM active_clients;"))


if __name__ == '__main__':
    unittest.main()
