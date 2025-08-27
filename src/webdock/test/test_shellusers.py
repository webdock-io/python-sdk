import os
import unittest
import time
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock.webdock import Webdock

load_dotenv()


class TestShellUsers(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))
        self.test_server_slug = None
        self.test_user_id = None

    def setUp(self):
        """Set up test data by creating a server and shell user"""
        try:
            # Create a temporary server
            server = self.client.servers.create(
                name=f"test-shell-{int(time.time())}",
                locationId="dk",
                profileSlug="webdockepyc-bit",
                imageSlug="webdock-ubuntu-jammy-cloud",
                slug=f"test-shell-{int(time.time())}",
            )
            self.test_server_slug = server.get("body").get("slug")
            
            # Wait for server to be ready
            while True:
                server_status = self.client.operation.fetch(server.get("headers").get("x_callback_id"))
                if server_status.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
            
            # Create a test shell user
            shell_user = self.client.shellUsers.create(
                serverSlug=self.test_server_slug,
                username=f"testuser{int(time.time())}",
                password="TestPassword123",
                group="sudo",
                shell="/bin/bash"
            )
            
            # Wait for user creation to complete
            while True:
                user_status = self.client.operation.fetch(shell_user.get("headers").get("x_callback_id"))
                if user_status.get("body")[0].get("status") == "finished":
                    break
                time.sleep(2)
            
            # Get the user ID from the list
            users = self.client.shellUsers.list(serverSlug=self.test_server_slug)
            for user in users.get("body"):
                if user.get("username") == shell_user.get("body").get("username"):
                    self.test_user_id = user.get("id")
                    break
                    
        except Exception as e:
            print(f"Setup failed: {e}")
            self.test_server_slug = None
            self.test_user_id = None

    def tearDown(self):
        """Clean up test data"""
        if self.test_server_slug:
            try:
                # Delete the test server (this will also delete the shell users)
                self.client.servers.delete(serverSlug=self.test_server_slug)
                
                # Wait for deletion to complete
                time.sleep(5)
            except Exception:
                pass

    def test_list_shell_users(self):
        """Test listing shell users for a server"""
        if not self.test_server_slug:
            self.skipTest("No test server available")

        users = self.client.shellUsers.list(serverSlug=self.test_server_slug)
        self.assertIsInstance(users.get("body"), list, "Shell users list should be of type list")

        if users.get("body"):
            user = users.get("body")[0]
            if user:
                self.assertIn("id", user, "Shell user should have id field")
                self.assertIn("username", user, "Shell user should have username field")
                self.assertIn("group", user, "Shell user should have group field")
                self.assertIn("shell", user, "Shell user should have shell field")
                self.assertIn("created", user, "Shell user should have created field")
                self.assertIn("updated", user, "Shell user should have updated field")
                self.assertIn("publicKeys", user, "Shell user should have publicKeys field")

    def test_create_shell_user(self):
        """Test creating a shell user"""
        if not self.test_server_slug:
            self.skipTest("No test server available")
        
        username = f"newuser-{int(time.time())}"
        shell_user = self.client.shellUsers.create(
            serverSlug=self.test_server_slug,
            username=username,
            password="NewPassword123",
            group="sudo",
            shell="/bin/bash"
        )
        

        self.assertIn("body", shell_user, "Response should have body field")
        self.assertIn("headers", shell_user, "Response should have headers field")
        self.assertIn("x_callback_id", shell_user.get("headers"), "Response should have x_callback_id header")
        TestShellUsers.test_user_id = shell_user.get("body").get("id")
        while True:
            wait = self.client.operation.fetch(shell_user.get("headers").get("x_callback_id"))
            if wait.get("body")[0].get("status") == "finished":
                break
            if wait.get("body")[0].get("status") == "error":
                self.fail
                break
            time.sleep(5)


    def test_delete_shell_user(self):
        """Test deleting a shell user"""
        if not self.test_server_slug or not self.test_user_id:
            self.skipTest("No test user available")
        
        delete_response = self.client.shellUsers.delete(
            serverSlug=self.test_server_slug,
            userId=TestShellUsers.test_user_id
        )
        
        self.assertIn("body", delete_response, "Response should have body field")
        self.assertIn("headers", delete_response, "Response should have headers field")
        self.assertIn("x_callback_id", delete_response.get("headers"), "Response should have x_callback_id header")
        while True:
            wait = self.client.operation.fetch(delete_response.get("headers").get("x_callback_id"))
            if wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)
            
    def test_edit_shell_user(self):

 
        edit_response = self.client.shellUsers.edit(
            slug=TestShellUsers.test_server_slug,
            id=TestShellUsers.test_user_id,
            keys=[]
        )
        
        self.assertIn("body", edit_response, "Response should have body field")
        self.assertIn("headers", edit_response, "Response should have headers field")
        while True:
            wait = self.client.operation.fetch(edit_response.get("headers").get("x_callback_id"))
            if wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)

 

if __name__ == '__main__':
    tests = unittest.TestSuite()
    tests.addTest(TestShellUsers.setUp)
    tests.addTest(TestShellUsers.test_create_shell_user)
    tests.addTest(TestShellUsers.test_list_shell_users)
    tests.addTest(TestShellUsers.test_edit_shell_user)
    tests.addTest(TestShellUsers.test_delete_shell_user)
    tests.addTest(TestShellUsers.tearDown)

    unittest.runner.TextTestRunner(verbosity=2, stream=True).run(tests)
