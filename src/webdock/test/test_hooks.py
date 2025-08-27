import time
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock.webdock import Webdock
from requests import RequestException
import unittest
import os

load_dotenv()

 
class TestHooks(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        TestHooks.test_server_slug = ""
        TestHooks.hook_id = None
        TestHooks.client = Webdock(os.getenv("TOKEN"))

    def test_1_create_server(self):
        """Test 2: Create server"""
        try:
            server = TestHooks.client.servers.create(
                name=f"temp-{int(time.time())}",
                locationId="dk",
                profileSlug="webdockepyc-bit",
                imageSlug="webdock-ubuntu-jammy-cloud",
                slug=f"temp-{int(time.time())}",
            )
            TestHooks.test_server_slug = server.get("body").get("slug")
            while True:
                server_wait = TestHooks.client.operation.fetch(server.get("headers").get("x_callback_id"))
                if server_wait.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
        except RequestException as e:
            self.fail(f"Failed to create server: {e}")

    def test_2_create_hook(self):
        try:
            created_hook = TestHooks.client.hooks.create(callbackUrl=f"http://apitest.vps.webdock.cloud?ss={int(time.time())}")
            TestHooks.hook_id = created_hook.get("body").get("id")
            TestHooks.assertIsNotNone(TestHooks.hook_id, "Hook ID should not be None")
        except RequestException as e:
            self.fail(f"Failed to create hook: {e}")

    def test_3_get_hook(self):
        try:
            created_hook = TestHooks.client.hooks.getById(id=TestHooks.hook_id)
            TestHooks.assertIsNotNone(created_hook.get("body").get("id"), "Hook ID should not be None")
        except RequestException as e:
            self.fail(f"Failed to get hook: {e}")

    def test_4_delete_hook(self):
        try:
            TestHooks.client.hooks.deleteById(id=TestHooks.hook_id)
        except RequestException as e:
            self.fail(f"Failed to delete hook: {e}")

    def test_5_delete_server(self):
        try:
            delete_server = TestHooks.client.servers.delete(serverSlug=TestHooks.test_server_slug)
            while True:
                delete_server_wait = TestHooks.client.operation.fetch(delete_server.get("headers").get("x_callback_id"))
                if delete_server_wait.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
        except RequestException as e:
            self.fail(f"Failed to delete server: {e}")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestHooks.test_1_create_server)
    suite.addTest(TestHooks.test_2_create_hook)
    suite.addTest(TestHooks.test_3_get_hook)
    suite.addTest(TestHooks.test_4_delete_hook)
    suite.addTest(TestHooks.test_5_delete_server)

    runner = unittest.TextTestRunner(verbosity=2,stream=True)
    runner.run(suite)
