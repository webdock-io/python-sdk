import unittest
import os
from oldwebdock import webdock

# This server should be created first
server_slug = 'pythontest1'

# This is random server slug that should not exist
bad_serverslug = 'a-random-server-that-should-not-exist'

wd = webdock.Webdock(os.environ.get('WEBDOCK_API_TOKEN'))

class TestWebdock(unittest.TestCase):
    # Test ping
    def test_ping(self):
        res = wd.ping()
        self.assertEqual(200, res.get('status'))
    
    # Test server listing
    def test_servers(self):
        res = wd.servers()
        self.assertEqual(200, res.get('status'))
    
    # Test non-existent server
    def test_bad_server(self):
        with self.assertRaises(Exception):
            wd.get_server(bad_serverslug)
    
    # Test existing server
    def test_good_server(self):
        res = wd.get_server(server_slug)
        self.assertEqual(200, res.get('status'))
    
    # Test shell user creation
    def test_create_shell_user(self):
        pass
        # res = wd.create_shelluser(server_slug, username='theuser', password='MySecurePassword?123#', group='sudo', shell='/bin/bash', publicKeys=[])
        # self.assertEqual(200, res.get('status'))
    
    # Test shell user listing
    def test_shell_users(self):
        pass
        # res = wd.get_shellusers(server_slug)
        # self.assertEqual(200, res.get('status'))
    
    # Test shell users for non-existent server
    def test_bad_shell_users(self):
        pass
        # with self.assertRaises(Exception):
            # wd.get_shellusers(bad_serverslug)
        
    # Test get scripts
    def test_get_scripts(self):
        res = wd.get_pubscripts()
        self.assertEqual(200, res.get('status'))

    # Test get good server scripts
    def test_get_badserverscripts(self):
        with self.assertRaises(Exception):
            wd.get_serverscripts(bad_serverslug)
    
    # Test get bad server scripts
    def test_get_goodserverscripts(self):
        res = wd.get_serverscripts(server_slug)
        self.assertEqual(200, res.get('status'))

if __name__ == '__main__':
    unittest.main()