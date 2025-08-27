import os
import unittest
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock.webdock import Webdock

load_dotenv()


class TestProfiles(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))

    def test_1_list_profiles_default(self):
        """Test 1: List profiles with default parameters"""
        profiles = self.client.profiles.list()
        self.assertIsInstance(profiles.get("body"), list, "Profiles list should be of type list")
        
        if profiles.get("body"):
            profile = profiles.get("body")[0]
            self.assertIn("slug", profile, "Profile should have slug field")
            self.assertIn("name", profile, "Profile should have name field")
            self.assertIn("ram", profile, "Profile should have ram field")
            self.assertIn("disk", profile, "Profile should have disk field")
            self.assertIn("cpu", profile, "Profile should have cpu field")
            self.assertIn("price", profile, "Profile should have price field")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestProfiles.test_1_list_profiles_default)
    runner = unittest.TextTestRunner(verbosity=2, stream=True)
    runner.run(suite)
