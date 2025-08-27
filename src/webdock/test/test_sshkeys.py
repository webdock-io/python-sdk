import os
import unittest
from dotenv import load_dotenv
from requests import RequestException
from typing import TYPE_CHECKING
from webdock.webdock import Webdock

import time

load_dotenv()


class TestSSHKeys(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        TestSSHKeys.client = Webdock(os.getenv("TOKEN"))
        TestSSHKeys.test_key_id = None

    def setUp(self):
        """Set up test data by creating an SSH key"""
        try:
            # Create a test SSH key
            ssh_key = TestSSHKeys.client.sshkeys.create(
                name=f"test-key-{int(time.time())}",
                publicKey="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC test@example.com"
            )
            TestSSHKeys.test_key_id = ssh_key.get("body").get("id")
        except Exception as e:
            print(f"Setup failed: {e}")
            TestSSHKeys.test_key_id = None

    def tearDown(self):
        """Clean up test data"""
        if TestSSHKeys.test_key_id:
            try:
                TestSSHKeys.client.sshkeys.delete(id=TestSSHKeys.test_key_id)
            except Exception:
                pass


    def test_1_create_ssh_key(self):
        """Test 2: Create SSH key"""
        key_name = f"new-key-{int(time.time())}"
        ssh_key = TestSSHKeys.client.sshkeys.create(
            name=key_name,
            publicKey="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC newtest@example.com"
        )
 
        TestSSHKeys.test_key_id = ssh_key.get("body").get("id")


    def test_2_list_ssh_keys(self):
        """Test 1: List SSH keys"""
        keys = TestSSHKeys.client.sshkeys.list()
        
        self.assertIsInstance(keys.get("body"), list, "SSH keys list should be of type list")

    
    def test_3_delete_ssh_keys(self):
        try:
            TestSSHKeys.client.sshkeys.delete(id=TestSSHKeys.test_key_id)
        except RequestException as e:
            TestSSHKeys.fail(f"Failed to delete SSH key: {e}")

         



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestSSHKeys.setUp)
    suite.addTest(TestSSHKeys.test_1_create_ssh_key)
    suite.addTest(TestSSHKeys.test_2_list_ssh_keys)
    suite.addTest(TestSSHKeys.test_3_delete_ssh_keys)
    suite.addTest(TestSSHKeys.tearDown)

    runner = unittest.TextTestRunner(verbosity=2, stream=True)
    runner.run(suite)
