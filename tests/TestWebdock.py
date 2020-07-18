import unittest
import os
from webdock.webdock import Webdock

# This server should be created first
server_slug = 'pythontest1'

wd = Webdock(os.environ.get('WEBDOCK_API_TOKEN'))

class TestWebdock(unittest.TestCase):
    # Test ping
    def test_ping(self):
        res = wd.ping()
        self.assertEqual(418, res.get('status'))
    
    # Test server listing
    def test_servers(self):
        res = wd.servers()
        self.assertEqual(200, res.get('status'))
    
    # Test non-existent server
    def test_bad_server(self):
        with self.assertRaises(Exception):
            wd.get_server('a-random-server-that-should-not-exist')
    
    # Test existing server
    def test_good_server(self):
        res = wd.get_server(server_slug)
        self.assertEqual(200, res.get('status'))


if __name__ == '__main__':
    unittest.main()