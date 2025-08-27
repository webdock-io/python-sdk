import time
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock import Webdock
from requests import RequestException
import unittest
import os

load_dotenv()

 
class TestScripts(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        TestScripts.test_server_slug = ""
        TestScripts.account_script_id = None
        TestScripts.client = Webdock(os.getenv("TOKEN"))

    def test_1_create_server(self):
        """Test 2: Create server"""
        try:
            server = TestScripts.client.servers.create(
                name=f"temp-{int(time.time())}",
                locationId="dk",
                profileSlug="webdockepyc-bit",
                imageSlug="webdock-ubuntu-jammy-cloud",
                slug=f"temp-{int(time.time())}",
            )
            TestScripts.test_server_slug = server.get("body").get("slug")
            while True:
                server_wait = TestScripts.client.operation.fetch(server.get("headers").get("x_callback_id"))
                if server_wait.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
        except RequestException as e:
            TestScripts.fail(f"Failed to create server: {e}")

    def test_2_create_account_script(self):
        """Test 2: Create script"""
        try:
            new_script = TestScripts.client.scripts.createAccountScript(
                name=f"temp-script-{int(time.time())}",
                content="#!/bin/bash\necho Hello World",
                filename="hello.sh",
            )
            TestScripts.account_script_id = new_script.get("body").get("id")
        except RequestException as e:
            self.fail(f"Failed to create script: {e}")

    def test_3_get_script(self):
        """Test 3: Get script"""
        try:
            script = TestScripts.client.scripts.getAccountScriptById(scriptId=TestScripts.account_script_id)
            self.assertEqual(script.get("body").get("id"), TestScripts.account_script_id, "Script ID should match")
        except RequestException as e:
            self.fail(f"Failed to get script: {e}")

    def test_4_deploy_script(self):
        """Test 4: Deploy script"""
        try:
            deploy_script = TestScripts.client.scripts.deployAccountScriptOnServer(
                scriptId=TestScripts.account_script_id,
                serverSlug=TestScripts.test_server_slug,
                executeImmediately=True,
                makeScriptExecutable=True,
                path="/root/hello.sh"
            )
            TestScripts.test_script_id_on_server = deploy_script.get("body").get("id")
            while True:
                deploy_script_wait = TestScripts.client.operation.fetch(deploy_script.get("headers").get("x_callback_id"))
                if deploy_script_wait.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
        except RequestException as e:
            TestScripts.fail(f"Failed to deploy script: {e}")

    def test_5_delete_server_script(self):
        """Test 5: Delete script"""
        try:
            deploy_script = TestScripts.client.scripts.deleteScriptFromServer(
                serverSlug=TestScripts.test_server_slug,
                scriptId=TestScripts.test_script_id_on_server
            )
            while True:
                deploy_script_wait = TestScripts.client.operation.fetch(deploy_script.get("headers").get("x_callback_id"))
                if deploy_script_wait.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
        except RequestException as e:
            TestScripts.fail(f"Failed to delete script: {e}")


    def test_6_delete_account_script(self):
        """Test 6: Delete account script"""
        try:
            TestScripts.client.scripts.deleteAccountScript(id=TestScripts.account_script_id)
        except RequestException as e:
            TestScripts.fail(f"Failed to delete script: {e}")
 

    def test_7_delete_server(self):
        try:
            delete_server = TestScripts.client.servers.delete(serverSlug=TestScripts.test_server_slug)
            while True:
                delete_server_wait = TestScripts.client.operation.fetch(delete_server.get("headers").get("x_callback_id"))
                if delete_server_wait.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
        except RequestException as e:
            TestScripts.fail(f"Failed to delete server: {e}")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestScripts.test_1_create_server)
    suite.addTest(TestScripts.test_2_create_account_script)
    suite.addTest(TestScripts.test_3_get_script)
    suite.addTest(TestScripts.test_4_deploy_script)
    suite.addTest(TestScripts.test_5_delete_server_script)
    suite.addTest(TestScripts.test_6_delete_account_script)
    suite.addTest(TestScripts.test_7_delete_server)

    runner = unittest.TextTestRunner(verbosity=2,stream=True)
    runner.run(suite)
