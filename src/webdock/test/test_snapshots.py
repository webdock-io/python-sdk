import os
import unittest
import time
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock import Webdock

load_dotenv()


class TestSnapshots(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))
        self.test_server_slug = None
        self.test_snapshot_id = None

    def setUp(self):
        """Set up test data by creating a server and snapshot"""
        try:
            # Create a temporary server
            server = self.client.servers.create(
                name=f"test-snap-{int(time.time())}",
                locationId="dk",
                profileSlug="webdockepyc-bit",
                imageSlug="webdock-ubuntu-jammy-cloud",
                slug=f"test-snap-{int(time.time())}",
            )
            self.test_server_slug = server.get("body").get("slug")
            
            # Wait for server to be ready
            while True:
                server_status = self.client.operation.fetch(server.get("headers").get("x_callback_id"))
                if server_status.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
            
            # Create a test snapshot
            snapshot = self.client.snapshots.create(
                serverSlug=self.test_server_slug,
                name=f"test-snapshot-{int(time.time())}"
            )
            
            # Wait for snapshot creation to complete
            while True:
                snapshot_status = self.client.operation.fetch(snapshot.get("headers").get("x_callback_id"))
                if snapshot_status.get("body")[0].get("status") == "finished":
                    break
                time.sleep(5)
            
            # Get the snapshot ID from the list
            snapshots = self.client.snapshots.list(serverSlug=self.test_server_slug)
            for snap in snapshots.get("body"):
                if snap.get("name") == snapshot.get("body").get("name"):
                    self.test_snapshot_id = snap.get("id")
                    break
                    
        except Exception as e:
            print(f"Setup failed: {e}")
            self.test_server_slug = None
            self.test_snapshot_id = None

    def tearDown(self):
        """Clean up test data"""
        if self.test_server_slug:
            try:
                # Delete the test server (this will also delete the snapshots)
                self.client.servers.delete(serverSlug=self.test_server_slug)
                
                # Wait for deletion to complete
                time.sleep(5)
            except Exception:
                pass

    def test_list_snapshots(self):
        """Test listing snapshots for a server"""
        if not self.test_server_slug:
            self.skipTest("No test server available")
        
        snapshots = self.client.snapshots.list(serverSlug=self.test_server_slug)
        self.assertIsInstance(snapshots.get("body"), list, "Snapshots list should be of type list")
        
        if snapshots.get("body"):
            snapshot = snapshots.get("body")[0]
            if snapshot:
                self.assertIn("id", snapshot, "Snapshot should have id field")
                self.assertIn("name", snapshot, "Snapshot should have name field")
                self.assertIn("date", snapshot, "Snapshot should have date field")
                self.assertIn("type", snapshot, "Snapshot should have type field")
                self.assertIn("virtualization", snapshot, "Snapshot should have virtualization field")
                self.assertIn("completed", snapshot, "Snapshot should have completed field")
                self.assertIn("deletable", snapshot, "Snapshot should have deletable field")

    def test_create_snapshot(self):
        """Test creating a snapshot"""
        if not self.test_server_slug:
            self.skipTest("No test server available")
        
        snapshot_name = f"new-snapshot-{int(time.time())}"
        snapshot = self.client.snapshots.create(
            serverSlug=self.test_server_slug,
            name=snapshot_name
        )
        TestSnapshots.test_snapshot_id = snapshot.get("body").get("id")
        self.assertIn("body", snapshot, "Response should have body field")
        self.assertIn("headers", snapshot, "Response should have headers field")
        self.assertIn("x_callback_id", snapshot.get("headers"), "Response should have x_callback_id header")
        while True:
            wait = self.client.operation.fetch(snapshot.get("headers").get("x_callback_id"))
            if wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)


    def test_delete_snapshot(self):
        """Test deleting a snapshot"""
        if not self.test_server_slug or not self.test_snapshot_id:
            self.skipTest("No test snapshot available")
        
        delete_response = self.client.snapshots.delete(
            serverSlug=self.test_server_slug,
            snapshotId=self.test_snapshot_id
        )
        
        self.assertIn("body", delete_response, "Response should have body field")
        self.assertIn("headers", delete_response, "Response should have headers field")
        self.assertIn("x_callback_id", delete_response.get("headers"), "Response should have x_callback_id header")
        while True:
            wait = self.client.operation.fetch(delete_response.get("headers").get("x_callback_id"))
            if wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)


    def test_restore_snapshot(self):
        """Test restoring a snapshot"""
        if not self.test_server_slug or not self.test_snapshot_id:
            self.skipTest("No test snapshot available")
        
        restore_response = self.client.snapshots.restore(
            serverSlug=self.test_server_slug,
            snapshotId=self.test_snapshot_id
        )
        
        self.assertIn("body", restore_response, "Response should have body field")
        self.assertIn("headers", restore_response, "Response should have headers field")
        self.assertIn("x_callback_id", restore_response.get("headers"), "Response should have x_callback_id header")

        while True:
            wait = self.client.operation.fetch(restore_response.get("headers").get("x_callback_id"))
            if wait.get("body")[0].get("status") == "finished":
                break
            time.sleep(5)


if __name__ == '__main__':
    tests = unittest.TestSuite()
    tests.addTest(TestSnapshots.setUp)
    tests.addTest(TestSnapshots.test_create_snapshot)
    tests.addTest(TestSnapshots.test_list_snapshots)
    tests.addTest(TestSnapshots.test_restore_snapshot)
    tests.addTest(TestSnapshots.test_delete_snapshot)
    tests.addTest(TestSnapshots.tearDown)
    unittest.runner.TextTestRunner(verbosity=2, stream=True).run(tests)
