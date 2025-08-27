import time
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock import Webdock
import unittest
import os

load_dotenv()

 
class TestServer(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.test_server_slug = ""
        self.client = Webdock(os.getenv("TOKEN"))

    def test_1_list_server(self):
        """Test 1: List servers"""
        account = self.client.servers.list()
        self.assertIsInstance(account.get("body"), list, "Server list should be of type list")

    def test_2_create_server(self):
        """Test 2: Create server"""
        server = self.client.servers.create(
            name=f"temp-{int(time.time())}",
            locationId="dk",
            profileSlug="webdockepyc-bit",
            imageSlug="webdock-ubuntu-jammy-cloud",
            slug=f"temp-{int(time.time())}",
        )
  
        TestServer.test_server_slug = server.get("body").get("slug")
        while True:
            server_wait = self.client.operation.fetch(server.get("headers").get("x_callback_id"))
            if server_wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)
    
 

    def test_3_get_server(self):
        """Test 3: Get server"""
        # apitest
        get_server = self.client.servers.getBySlug(serverSlug=TestServer.test_server_slug)
        self.assertEqual(get_server.get("body").get("slug"), TestServer.test_server_slug, "Server slug should match")
 

    def test_4_reinstall_server(self):
        """Test 4: Reinstall server"""
        reinstall_server = self.client.servers.reinstall(
            imageSlug="webdock-almalinux-9-cloud",
            serverSlug=TestServer.test_server_slug
        )
        
        while True:
            reinstall_server_wait = self.client.operation.fetch(reinstall_server.get("headers").get("x_callback_id"))
            if reinstall_server_wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)

    def test_5_resize_server(self):
        resize_server = self.client.servers.resize(
            serverSlug=TestServer.test_server_slug,
            profileSlug="webdockepyc-premium"
        )
        while True:
            resize_server_wait = self.client.operation.fetch(resize_server.get("headers").get("x_callback_id"))
            if resize_server_wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)
    def test_6_delete_server(self):
        delete_server = self.client.servers.delete(serverSlug=TestServer.test_server_slug)
 
        while True:
            delete_server_wait = self.client.operation.fetch(delete_server.get("headers").get("x_callback_id"))
            if delete_server_wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestServer.test_1_list_server)
    suite.addTest(TestServer.test_2_create_server)
    suite.addTest(TestServer.test_3_get_server)
    suite.addTest(TestServer.test_4_reinstall_server)
    suite.addTest(TestServer.test_5_resize_server)
    suite.addTest(TestServer.test_6_delete_server)


    runner = unittest.TextTestRunner(verbosity=2,stream=True)
    runner.run(suite)