import os
import unittest
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock import Webdock

load_dotenv()


class TestLocations(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))

    def test_1_list_locations(self):
        """Test 1: List all available locations"""
        locations = self.client.locations.list()
        self.assertIsInstance(locations.get("body"), list, "Locations list should be of type list")
        
        if locations.get("body"):
            location = locations.get("body")[0]
            self.assertIn("id", location, "Location should have id field")
            self.assertIn("name", location, "Location should have name field")
            self.assertIn("city", location, "Location should have city field")
            self.assertIn("country", location, "Location should have country field")
            self.assertIn("description", location, "Location should have description field")
            self.assertIn("icon", location, "Location should have icon field")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestLocations.test_1_list_locations)

    runner = unittest.TextTestRunner(verbosity=2, stream=True)
    runner.run(suite)
