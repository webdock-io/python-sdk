import unittest
import os
from webdock.webdock import Webdock

wd = Webdock(os.environ.get('WEBDOCK_API_TOKEN'))

class TestWebdock(unittest.TestCase):
    # Test ping
    def test_ping(self):
        res = wd.ping()
        self.assertEqual(200, res.get('status'))
    
    # Test server listing
    def test_servers(self):
        res = wd.servers()
        self.assertEqual(200, res.get('status'))
    
    # Test server
    def test_server(self):
        with self.assertRaises(Exception):
            wd.get_server('a-random-server')

if __name__ == '__main__':
    unittest.main()