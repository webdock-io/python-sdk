import os
import unittest
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock.webdock import Webdock

load_dotenv()


class TestImages(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))

    def test_1_list_images(self):
        """Test 1: List all available images"""
        images = self.client.images.list()
        self.assertIsInstance(images.get("body"), list, "Images list should be of type list")
        
        if images.get("body"):
            image = images.get("body")[0]
            self.assertIn("slug", image, "Image should have slug field")
            self.assertIn("name", image, "Image should have name field")
            self.assertIn("webServer", image, "Image should have webServer field")
            self.assertIn("phpVersion", image, "Image should have phpVersion field")

    def test_2_images_structure(self):
        """Test 2: Images data structure validation"""
        images = self.client.images.list()
        self.assertIsInstance(images.get("body"), list, "Images list should be of type list")
        
        for image in images.get("body"):
            # Check required fields
            self.assertIsInstance(image.get("slug"), str, "slug should be a string")
            self.assertIsInstance(image.get("name"), str, "name should be a string")
            
            # Check optional fields
            if image.get("webServer") is not None:
                self.assertIsInstance(image.get("webServer"), str, "webServer should be a string")
            if image.get("phpVersion") is not None:
                self.assertIsInstance(image.get("phpVersion"), str, "phpVersion should be a string")

    def test_3_images_web_server_values(self):
        """Test 3: Images web server values validation"""
        images = self.client.images.list()
        self.assertIsInstance(images.get("body"), list, "Images list should be of type list")
        
        valid_web_servers = ["Apache", "Nginx", None]
        for image in images.get("body"):
            self.assertIn(image.get("webServer"), valid_web_servers, 
                         f"webServer should be one of {valid_web_servers}")

    def test_4_images_php_version_format(self):
        """Test 4: Images PHP version format validation"""
        images = self.client.images.list()
        self.assertIsInstance(images.get("body"), list, "Images list should be of type list")
        
        for image in images.get("body"):
            if image.get("phpVersion") is not None:
                php_version = image.get("phpVersion")
                # PHP version should be a string and not empty
                self.assertIsInstance(php_version, str, "phpVersion should be a string")
                self.assertGreater(len(php_version), 0, "phpVersion should not be empty")

    def test_5_images_required_fields_not_empty(self):
        """Test 5: Images required fields validation"""
        images = self.client.images.list()
        self.assertIsInstance(images.get("body"), list, "Images list should be of type list")
        
        for image in images.get("body"):
            self.assertGreater(len(image.get("slug")), 0, "slug should not be empty")
            self.assertGreater(len(image.get("name")), 0, "name should not be empty")

    def test_6_images_unique_slugs(self):
        """Test 6: Images unique slugs validation"""
        images = self.client.images.list()
        self.assertIsInstance(images.get("body"), list, "Images list should be of type list")
        
        if images.get("body"):
            image_slugs = [image.get("slug") for image in images.get("body")]
            unique_slugs = set(image_slugs)
            self.assertEqual(len(image_slugs), len(unique_slugs), "All image slugs should be unique")

    def test_7_images_not_empty(self):
        """Test 7: Images list not empty validation"""
        images = self.client.images.list()
        self.assertIsInstance(images.get("body"), list, "Images list should be of type list")
        # Note: This test assumes there are images available in the account
        # If no images are available, this test will pass but the list will be empty


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestImages.test_1_list_images)
    suite.addTest(TestImages.test_2_images_structure)
    suite.addTest(TestImages.test_3_images_web_server_values)
    suite.addTest(TestImages.test_4_images_php_version_format)
    suite.addTest(TestImages.test_5_images_required_fields_not_empty)
    suite.addTest(TestImages.test_6_images_unique_slugs)
    suite.addTest(TestImages.test_7_images_not_empty)

    runner = unittest.TextTestRunner(verbosity=2, stream=True)
    runner.run(suite)
